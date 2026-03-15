#!/usr/bin/env python3
"""
App Store Connect In-App Purchase & Subscription Manager

CLI tool for managing IAPs and auto-renewable subscriptions via the
App Store Connect REST API. Covers operations not available through
the MCP server.

Requires: PyJWT, cryptography (auto-installed into a venv)

Auth config is read from environment variables:
  APP_STORE_CONNECT_KEY_ID
  APP_STORE_CONNECT_ISSUER_ID
  APP_STORE_CONNECT_P8_PATH
"""

import sys
import os
import json
import time
import urllib.request
import ssl
import argparse

def get_auth_config():
    key_id = os.environ.get("APP_STORE_CONNECT_KEY_ID")
    issuer_id = os.environ.get("APP_STORE_CONNECT_ISSUER_ID")
    p8_path = os.environ.get("APP_STORE_CONNECT_P8_PATH")

    if not all([key_id, issuer_id, p8_path]):
        # Fallback: read from ~/.appstoreconnect/ convention
        asc_dir = os.path.expanduser("~/.appstoreconnect")
        if os.path.isdir(asc_dir):
            p8_files = [f for f in os.listdir(asc_dir) if f.endswith(".p8")]
            if p8_files:
                p8_path = p8_path or os.path.join(asc_dir, p8_files[0])
                # Extract key ID from filename like AuthKey_XXXXXXXXXX.p8
                if not key_id and p8_files[0].startswith("AuthKey_"):
                    key_id = p8_files[0].replace("AuthKey_", "").replace(".p8", "")

        config_path = os.path.expanduser("~/.appstoreconnect/config.json")
        if os.path.isfile(config_path):
            with open(config_path) as f:
                config = json.load(f)
                key_id = key_id or config.get("keyId")
                issuer_id = issuer_id or config.get("issuerId")
                p8_path = p8_path or config.get("p8Path")

    if not all([key_id, issuer_id, p8_path]):
        print("Error: Missing auth config. Set APP_STORE_CONNECT_KEY_ID, APP_STORE_CONNECT_ISSUER_ID, APP_STORE_CONNECT_P8_PATH", file=sys.stderr)
        sys.exit(1)

    return key_id, issuer_id, p8_path


def generate_token(key_id, issuer_id, p8_path):
    import jwt
    with open(p8_path, "r") as f:
        private_key = f.read()
    now = int(time.time())
    payload = {"iss": issuer_id, "iat": now, "exp": now + 1200, "aud": "appstoreconnect-v1"}
    return jwt.encode(payload, private_key, algorithm="ES256", headers={"kid": key_id})


def api_call(token, method, path, body=None):
    url = f"https://api.appstoreconnect.apple.com{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }, method=method)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP {e.code} for {method} {path}:", file=sys.stderr)
        try:
            print(json.dumps(json.loads(error_body), indent=2), file=sys.stderr)
        except json.JSONDecodeError:
            print(error_body, file=sys.stderr)
        return None


# ── Commands ──────────────────────────────────────────────────────────

def cmd_list(token, args):
    """List all in-app purchases for an app."""
    result = api_call(token, "GET", f"/v1/apps/{args.app_id}/inAppPurchasesV2?limit=200")
    if result:
        iaps = result.get("data", [])
        if not iaps:
            print("No in-app purchases found.")
            return
        for iap in iaps:
            attrs = iap["attributes"]
            print(f"  {iap['id']}  {attrs['productId']}  [{attrs['inAppPurchaseType']}]  state={attrs['state']}  name={attrs['name']}")


def cmd_get(token, args):
    """Get details of a specific IAP."""
    result = api_call(token, "GET", f"/v2/inAppPurchases/{args.iap_id}?include=inAppPurchaseLocalizations")
    if result:
        print(json.dumps(result, indent=2))


def cmd_create(token, args):
    """Create a new in-app purchase."""
    body = {
        "data": {
            "type": "inAppPurchases",
            "attributes": {
                "name": args.name,
                "productId": args.product_id,
                "inAppPurchaseType": args.type.upper()
            },
            "relationships": {
                "app": {
                    "data": {"type": "apps", "id": args.app_id}
                }
            }
        }
    }
    result = api_call(token, "POST", "/v2/inAppPurchases", body)
    if result:
        iap = result["data"]
        print(f"Created IAP: {iap['id']}")
        print(f"  Product ID: {iap['attributes']['productId']}")
        print(f"  Type: {iap['attributes']['inAppPurchaseType']}")
        print(f"  State: {iap['attributes']['state']}")
        return iap["id"]


def cmd_add_localization(token, args):
    """Add a localization to an IAP."""
    if len(args.description) > 55:
        print(f"Warning: description is {len(args.description)} chars, max is 55 for non-consumables. Truncating.", file=sys.stderr)
        args.description = args.description[:55]

    body = {
        "data": {
            "type": "inAppPurchaseLocalizations",
            "attributes": {
                "name": args.name,
                "description": args.description,
                "locale": args.locale
            },
            "relationships": {
                "inAppPurchaseV2": {
                    "data": {"type": "inAppPurchases", "id": args.iap_id}
                }
            }
        }
    }
    result = api_call(token, "POST", "/v1/inAppPurchaseLocalizations", body)
    if result:
        loc = result["data"]
        print(f"Added localization: {loc['attributes']['locale']} -> {loc['attributes']['name']}")
        print(f"  State: {loc['attributes']['state']}")


def cmd_set_price(token, args):
    """Set the price for an IAP by finding the matching price point."""
    target_price = float(args.price)
    territory = args.territory

    # Find matching price point
    result = api_call(token, "GET",
        f"/v2/inAppPurchases/{args.iap_id}/pricePoints?filter[territory]={territory}&limit=200")
    if not result:
        return

    price_point_id = None
    for pp in result.get("data", []):
        cp = pp.get("attributes", {}).get("customerPrice")
        if cp and abs(float(cp) - target_price) < 0.01:
            price_point_id = pp["id"]
            print(f"Found price point: ${cp} ({territory}) -> {price_point_id[:30]}...")
            break

    if not price_point_id:
        print(f"No price point found for ${target_price} in {territory}", file=sys.stderr)
        # Show available prices
        for pp in result.get("data", [])[:10]:
            cp = pp.get("attributes", {}).get("customerPrice", "?")
            print(f"  Available: ${cp}", file=sys.stderr)
        return

    body = {
        "data": {
            "type": "inAppPurchasePriceSchedules",
            "relationships": {
                "inAppPurchase": {
                    "data": {"type": "inAppPurchases", "id": args.iap_id}
                },
                "baseTerritory": {
                    "data": {"type": "territories", "id": territory}
                },
                "manualPrices": {
                    "data": [{"type": "inAppPurchasePrices", "id": "${price1}"}]
                }
            }
        },
        "included": [{
            "type": "inAppPurchasePrices",
            "id": "${price1}",
            "relationships": {
                "inAppPurchasePricePoint": {
                    "data": {"type": "inAppPurchasePricePoints", "id": price_point_id}
                }
            }
        }]
    }
    result = api_call(token, "POST", "/v1/inAppPurchasePriceSchedules", body)
    if result:
        print(f"Price set to ${target_price} ({territory})")


def cmd_delete(token, args):
    """Delete an IAP (only works if not yet submitted)."""
    result = api_call(token, "DELETE", f"/v2/inAppPurchases/{args.iap_id}")
    if result is not None:
        print(f"Deleted IAP: {args.iap_id}")
    else:
        # DELETE returns empty body on success (204)
        print(f"Delete request sent for IAP: {args.iap_id}")


# ── Subscription Commands ────────────────────────────────────────────

def cmd_list_groups(token, args):
    """List subscription groups for an app."""
    result = api_call(token, "GET", f"/v1/apps/{args.app_id}/subscriptionGroups?limit=200")
    if result:
        groups = result.get("data", [])
        if not groups:
            print("No subscription groups found.")
            return
        for g in groups:
            attrs = g["attributes"]
            print(f"  {g['id']}  {attrs['referenceName']}")


def cmd_create_group(token, args):
    """Create a subscription group."""
    body = {
        "data": {
            "type": "subscriptionGroups",
            "attributes": {
                "referenceName": args.name
            },
            "relationships": {
                "app": {
                    "data": {"type": "apps", "id": args.app_id}
                }
            }
        }
    }
    result = api_call(token, "POST", "/v1/subscriptionGroups", body)
    if result:
        group = result["data"]
        print(f"Created subscription group: {group['id']}")
        print(f"  Name: {group['attributes']['referenceName']}")
        return group["id"]


def cmd_list_subs(token, args):
    """List subscriptions in a group."""
    result = api_call(token, "GET", f"/v1/subscriptionGroups/{args.group_id}/subscriptions?limit=200")
    if result:
        subs = result.get("data", [])
        if not subs:
            print("No subscriptions found in group.")
            return
        for s in subs:
            attrs = s["attributes"]
            print(f"  {s['id']}  {attrs['productId']}  period={attrs.get('subscriptionPeriod', '?')}  state={attrs.get('state', '?')}  name={attrs['name']}")


def cmd_create_sub(token, args):
    """Create an auto-renewable subscription."""
    body = {
        "data": {
            "type": "subscriptions",
            "attributes": {
                "name": args.name,
                "productId": args.product_id,
                "subscriptionPeriod": args.period,
                "reviewNote": args.review_note or ""
            },
            "relationships": {
                "group": {
                    "data": {"type": "subscriptionGroups", "id": args.group_id}
                }
            }
        }
    }
    # Remove empty reviewNote
    if not body["data"]["attributes"]["reviewNote"]:
        del body["data"]["attributes"]["reviewNote"]

    result = api_call(token, "POST", "/v1/subscriptions", body)
    if result:
        sub = result["data"]
        print(f"Created subscription: {sub['id']}")
        print(f"  Product ID: {sub['attributes']['productId']}")
        print(f"  Period: {sub['attributes'].get('subscriptionPeriod', '?')}")
        print(f"  State: {sub['attributes'].get('state', '?')}")
        return sub["id"]


def cmd_get_sub(token, args):
    """Get subscription details with localizations."""
    result = api_call(token, "GET", f"/v1/subscriptions/{args.sub_id}?include=subscriptionLocalizations")
    if result:
        print(json.dumps(result, indent=2))


def cmd_add_sub_localization(token, args):
    """Add a localization to a subscription."""
    body = {
        "data": {
            "type": "subscriptionLocalizations",
            "attributes": {
                "name": args.name,
                "description": args.description,
                "locale": args.locale
            },
            "relationships": {
                "subscription": {
                    "data": {"type": "subscriptions", "id": args.sub_id}
                }
            }
        }
    }
    result = api_call(token, "POST", "/v1/subscriptionLocalizations", body)
    if result:
        loc = result["data"]
        print(f"Added localization: {loc['attributes']['locale']} -> {loc['attributes']['name']}")
        print(f"  State: {loc['attributes'].get('state', '?')}")


def cmd_set_sub_price(token, args):
    """Set the price for a subscription."""
    target_price = float(args.price)
    territory = args.territory

    # Find matching price point (paginate through all)
    price_point_id = None
    url = f"/v1/subscriptions/{args.sub_id}/pricePoints?filter[territory]={territory}&limit=200"
    all_points = []
    while url:
        result = api_call(token, "GET", url)
        if not result:
            return
        for pp in result.get("data", []):
            all_points.append(pp)
            cp = pp.get("attributes", {}).get("customerPrice")
            if cp and abs(float(cp) - target_price) < 0.01:
                price_point_id = pp["id"]
                print(f"Found price point: ${cp} ({territory}) -> {price_point_id[:30]}...")
                break
        if price_point_id:
            break
        # Follow pagination
        next_link = result.get("links", {}).get("next")
        if next_link:
            url = next_link.replace("https://api.appstoreconnect.apple.com", "")
        else:
            break

    if not price_point_id:
        print(f"No price point found for ${target_price} in {territory}", file=sys.stderr)
        for pp in all_points[:10]:
            cp = pp.get("attributes", {}).get("customerPrice", "?")
            print(f"  Available: ${cp}", file=sys.stderr)
        return

    body = {
        "data": {
            "type": "subscriptionPrices",
            "attributes": {
                "startDate": None,
                "preserveCurrentPrice": False
            },
            "relationships": {
                "subscription": {
                    "data": {"type": "subscriptions", "id": args.sub_id}
                },
                "territory": {
                    "data": {"type": "territories", "id": territory}
                },
                "subscriptionPricePoint": {
                    "data": {"type": "subscriptionPricePoints", "id": price_point_id}
                }
            }
        }
    }
    result = api_call(token, "POST", "/v1/subscriptionPrices", body)
    if result:
        print(f"Price set to ${target_price} ({territory})")
    else:
        print("Hint: If you get a 500 error, check that the 'Paid Applications' agreement is signed in App Store Connect > Agreements, Tax, and Banking.", file=sys.stderr)


def cmd_add_intro_offer(token, args):
    """Add an introductory offer to a subscription."""
    body = {
        "data": {
            "type": "subscriptionIntroductoryOffers",
            "attributes": {
                "duration": args.duration,
                "offerMode": args.mode,
                "numberOfPeriods": int(args.periods),
            },
            "relationships": {
                "subscription": {
                    "data": {"type": "subscriptions", "id": args.sub_id}
                },
                "territory": {
                    "data": {"type": "territories", "id": args.territory}
                }
            }
        }
    }
    # Add optional subscription price point for PAY_AS_YOU_GO / PAY_UP_FRONT
    if args.price_point_id:
        body["data"]["relationships"]["subscriptionPricePoint"] = {
            "data": {"type": "subscriptionPricePoints", "id": args.price_point_id}
        }
    if args.start_date:
        body["data"]["attributes"]["startDate"] = args.start_date
    if args.end_date:
        body["data"]["attributes"]["endDate"] = args.end_date

    result = api_call(token, "POST", "/v1/subscriptionIntroductoryOffers", body)
    if result:
        offer = result["data"]
        attrs = offer["attributes"]
        print(f"Created introductory offer: {offer['id']}")
        print(f"  Mode: {attrs['offerMode']}  Duration: {attrs['duration']}  Periods: {attrs['numberOfPeriods']}")
    else:
        print("Hint: If you get a 500 error, check that the 'Paid Applications' agreement is signed.", file=sys.stderr)


def cmd_list_intro_offers(token, args):
    """List introductory offers for a subscription."""
    result = api_call(token, "GET", f"/v1/subscriptions/{args.sub_id}/introductoryOffers?limit=200")
    if result:
        offers = result.get("data", [])
        if not offers:
            print("No introductory offers found.")
            return
        for o in offers:
            attrs = o["attributes"]
            print(f"  {o['id']}  mode={attrs['offerMode']}  duration={attrs['duration']}  periods={attrs['numberOfPeriods']}")


def cmd_list_sub_price_points(token, args):
    """List price points for a subscription (to find IDs for intro offers)."""
    target_price = float(args.price) if args.price else None
    territory = args.territory
    url = f"/v1/subscriptions/{args.sub_id}/pricePoints?filter[territory]={territory}&limit=200"
    all_points = []
    while url:
        result = api_call(token, "GET", url)
        if not result:
            return
        for pp in result.get("data", []):
            cp = pp.get("attributes", {}).get("customerPrice")
            if target_price and cp and abs(float(cp) - target_price) < 0.01:
                print(f"  MATCH: ${cp} -> {pp['id']}")
                return
            all_points.append(pp)
        next_link = result.get("links", {}).get("next")
        if next_link:
            url = next_link.replace("https://api.appstoreconnect.apple.com", "")
        else:
            break
    if target_price:
        print(f"No price point found for ${target_price} in {territory}", file=sys.stderr)
    # Show some available prices
    for pp in all_points[:20]:
        cp = pp.get("attributes", {}).get("customerPrice", "?")
        print(f"  ${cp} -> {pp['id'][:40]}...")


# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="App Store Connect IAP Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = subparsers.add_parser("list", help="List IAPs for an app")
    p_list.add_argument("app_id", help="App Store Connect app ID")

    # get
    p_get = subparsers.add_parser("get", help="Get IAP details")
    p_get.add_argument("iap_id", help="IAP ID")

    # create
    p_create = subparsers.add_parser("create", help="Create a new IAP")
    p_create.add_argument("app_id", help="App ID")
    p_create.add_argument("product_id", help="Product ID (e.g. com.example.premium)")
    p_create.add_argument("name", help="Reference name")
    p_create.add_argument("--type", default="NON_CONSUMABLE",
        choices=["NON_CONSUMABLE", "CONSUMABLE", "NON_RENEWING_SUBSCRIPTION"],
        help="IAP type (default: NON_CONSUMABLE)")

    # add-localization
    p_loc = subparsers.add_parser("add-localization", help="Add localization to IAP")
    p_loc.add_argument("iap_id", help="IAP ID")
    p_loc.add_argument("locale", help="Locale code (e.g. en-US, de-DE)")
    p_loc.add_argument("name", help="Display name")
    p_loc.add_argument("description", help="Description (max 55 chars for non-consumables)")

    # set-price
    p_price = subparsers.add_parser("set-price", help="Set price for IAP")
    p_price.add_argument("iap_id", help="IAP ID")
    p_price.add_argument("price", help="Price in USD (e.g. 9.99)")
    p_price.add_argument("--territory", default="USA", help="Base territory (default: USA)")

    # delete
    p_del = subparsers.add_parser("delete", help="Delete an IAP")
    p_del.add_argument("iap_id", help="IAP ID")

    # ── Subscription commands ──

    # list-groups
    p_lg = subparsers.add_parser("list-groups", help="List subscription groups for an app")
    p_lg.add_argument("app_id", help="App Store Connect app ID")

    # create-group
    p_cg = subparsers.add_parser("create-group", help="Create a subscription group")
    p_cg.add_argument("app_id", help="App ID")
    p_cg.add_argument("name", help="Reference name for the group")

    # list-subs
    p_ls = subparsers.add_parser("list-subs", help="List subscriptions in a group")
    p_ls.add_argument("group_id", help="Subscription group ID")

    # create-sub
    p_cs = subparsers.add_parser("create-sub", help="Create an auto-renewable subscription")
    p_cs.add_argument("group_id", help="Subscription group ID")
    p_cs.add_argument("product_id", help="Product ID (e.g. com.example.monthly)")
    p_cs.add_argument("name", help="Reference name")
    p_cs.add_argument("--period", required=True,
        choices=["ONE_WEEK", "ONE_MONTH", "TWO_MONTHS", "THREE_MONTHS", "SIX_MONTHS", "ONE_YEAR"],
        help="Subscription period")
    p_cs.add_argument("--review-note", dest="review_note", default=None,
        help="Optional review note for App Store review")

    # get-sub
    p_gs = subparsers.add_parser("get-sub", help="Get subscription details")
    p_gs.add_argument("sub_id", help="Subscription ID")

    # add-sub-localization
    p_sl = subparsers.add_parser("add-sub-localization", help="Add localization to a subscription")
    p_sl.add_argument("sub_id", help="Subscription ID")
    p_sl.add_argument("locale", help="Locale code (e.g. en-US, de-DE)")
    p_sl.add_argument("name", help="Display name")
    p_sl.add_argument("description", help="Description")

    # set-sub-price
    p_sp = subparsers.add_parser("set-sub-price", help="Set price for a subscription")
    p_sp.add_argument("sub_id", help="Subscription ID")
    p_sp.add_argument("price", help="Price in USD (e.g. 4.99)")
    p_sp.add_argument("--territory", default="USA", help="Territory (default: USA)")

    # add-intro-offer
    p_io = subparsers.add_parser("add-intro-offer", help="Add introductory offer to a subscription")
    p_io.add_argument("sub_id", help="Subscription ID")
    p_io.add_argument("--mode", required=True,
        choices=["FREE_TRIAL", "PAY_AS_YOU_GO", "PAY_UP_FRONT"],
        help="Offer mode")
    p_io.add_argument("--duration", required=True,
        choices=["THREE_DAYS", "ONE_WEEK", "TWO_WEEKS", "ONE_MONTH", "TWO_MONTHS",
                 "THREE_MONTHS", "SIX_MONTHS", "ONE_YEAR"],
        help="Duration of each period")
    p_io.add_argument("--periods", required=True, help="Number of periods")
    p_io.add_argument("--price-point-id", dest="price_point_id", default=None,
        help="Price point ID (for PAY_AS_YOU_GO/PAY_UP_FRONT; use list-price-points to find)")
    p_io.add_argument("--territory", default="USA", help="Territory (default: USA)")
    p_io.add_argument("--start-date", dest="start_date", default=None, help="Start date (YYYY-MM-DD)")
    p_io.add_argument("--end-date", dest="end_date", default=None, help="End date (YYYY-MM-DD)")

    # list-intro-offers
    p_lio = subparsers.add_parser("list-intro-offers", help="List introductory offers for a subscription")
    p_lio.add_argument("sub_id", help="Subscription ID")

    # list-price-points
    p_lpp = subparsers.add_parser("list-price-points", help="List/find price points for a subscription")
    p_lpp.add_argument("sub_id", help="Subscription ID")
    p_lpp.add_argument("--price", default=None, help="Find specific price (e.g. 6.99)")
    p_lpp.add_argument("--territory", default="USA", help="Territory (default: USA)")

    args = parser.parse_args()

    key_id, issuer_id, p8_path = get_auth_config()
    token = generate_token(key_id, issuer_id, p8_path)

    commands = {
        "list": cmd_list,
        "get": cmd_get,
        "create": cmd_create,
        "add-localization": cmd_add_localization,
        "set-price": cmd_set_price,
        "delete": cmd_delete,
        "list-groups": cmd_list_groups,
        "create-group": cmd_create_group,
        "list-subs": cmd_list_subs,
        "create-sub": cmd_create_sub,
        "get-sub": cmd_get_sub,
        "add-sub-localization": cmd_add_sub_localization,
        "set-sub-price": cmd_set_sub_price,
        "add-intro-offer": cmd_add_intro_offer,
        "list-intro-offers": cmd_list_intro_offers,
        "list-price-points": cmd_list_sub_price_points,
    }
    commands[args.command](token, args)


if __name__ == "__main__":
    main()
