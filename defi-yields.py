#!/usr/bin/env python3
"""
defi-yields.py — DeFi yield aggregator CLI

Compare APY across major DeFi protocols: Aave, Compound, Curve,
Uniswap, Lido, and more. Tracks best yields for Bitcoin-adjacent assets.

Pure Python 3.7+, zero dependencies. Data from DeFi APIs.

Usage:
    python defi-yields.py                          # All protocols
    python defi-yields.py --aave                     # Aave only
    python defi-yields.py --compound                 # Compound only
    python defi-yields.py --best                     # Top yields only
    python defi-yields.py --json                       # JSON output

Support: https://github.com/yourusername/defi-yields
BTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9
"""

import sys
import json
import urllib.request
from datetime import datetime


# DeFi yield sources - using DeFiLlama API
# https://defillama.com/docs/api

def fetch_json(url):
    """Fetch JSON from URL"""
    req = urllib.request.Request(url, headers={"User-Agent": "defi-yields/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}


def get_defillama_yields():
    """Get yields from DeFiLlama"""
    data = fetch_json("https://yields.llama.fi/yields")
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    return []


def get_aave_yields():
    """Get yields from Aave"""
    yields = get_defillama_yields()
    return [y for y in yields if y.get("project") == "Aave"]


def get_compound_yields():
    """Get yields from Compound"""
    yields = get_defillama_yields()
    return [y for y in yields if y.get("project") == "Compound"]


def get_lido_yields():
    """Get yields from Lido"""
    yields = get_defillama_yields()
    return [y for y in yields if y.get("project") == "Lido"]


def get_all_yields():
    """Get yields from all protocols"""
    all_data = get_defillama_yields()
    all_yields = []

    for item in all_data[:50]:  # Get top 50 yields
        all_yields.append({
            "protocol": item.get("project", "N/A"),
            "asset": item.get("symbol", "N/A"),
            "apy": item.get("apy", 0),
            "type": item.get("category", "N/A"),
            "chain": item.get("chain", "N/A"),
            "tvl": item.get("tvl", 0),
        })

    # Sort by APY descending
    all_yields.sort(key=lambda x: x.get("apy", 0), reverse=True)
    return all_yields


def display_table(yields, show_best_only=False):
    """Display yields in a table"""
    if not yields:
        print("\n  ⚠️  No yield data available right now\n")
        return

    if show_best_only:
        yields = yields[:10]

    print(f"\n  ╔══════════════════════════════════════════════════════════════╗")
    print("  ║              💰 DEFI YIELD AGGREGATOR                      ║")
    print("  ╚══════════════════════════════════════════════════════════════╝")
    print(f"  Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    header = f"  {'PROTOCOL':<12} {'ASSET':<10} {'APY':>10} {'TYPE':<10}"
    sep = "  " + "─" * 42
    print(header)
    print(sep)

    for y in yields:
        protocol = y.get("protocol", "N/A")[:12]
        asset = y.get("asset", "N/A")[:10]
        apy = y.get("apy", 0)
        ytype = y.get("type", "N/A")[:10]
        print(f"  {protocol:<12} {asset:<10} {apy:>9.2f}% {ytype:<10}")

    print(f"\n  💡 Best APY: {yields[0]['apy']:.2f}% ({yields[0]['asset']} on {yields[0]['protocol']})")
    print(f"  💰 BTC Tips: 1KPUa9Njq86NJwmwqVmdjZ4oC8eHrXKqf9")
    print(f"  📦 Source: https://github.com/yourusername/defi-yields\n")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if not args:
        # Default: show all yields
        yields = get_all_yields()
        display_table(yields)
        return

    if "json" in [a.lower() for a in args]:
        yields = get_all_yields()
        print(json.dumps(yields, indent=2))
    elif "best" in [a.lower() for a in args]:
        yields = get_all_yields()
        display_table(yields, show_best_only=True)
    elif "aave" in [a.lower() for a in args]:
        yields = get_all_yields()
        aave_yields = [y for y in yields if y["protocol"] == "Aave"]
        display_table(aave_yields)
    elif "compound" in [a.lower() for a in args]:
        yields = get_all_yields()
        compound_yields = [y for y in yields if y["protocol"] == "Compound"]
        display_table(compound_yields)
    else:
        yields = get_all_yields()
        display_table(yields)


if __name__ == "__main__":
    main()
