#!/usr/bin/env python

import json
import math
import statistics as stats


def create_Summary(row):
    """Generate purchase summary"""
    receipt_lines = row.get("receiptLines")
    
    # Generate item information
    _items = []
    for record in receipt_lines:
        _item = {
            "purchase_time": row.get("purchaseDateTimeString"),
            "merchant_name": row.get("merchant").get("merchantId"),
            "item_name": record.get("name"),
            "count": record.get("count"),
            "price": record.get("itemPrice").get("amount"),
            "vat": record.get("itemPrice").get("vat"),
            "total_price": record.get("totalPrice").get("amount"),
            "total_vat": record.get("totalPrice").get("vat"),
            "category": record.get("category")
        }
        _items.append(_item)
    
    # -- Get prices
    prices = [
        record.get("itemPrice").get("amount")
        for record in receipt_lines
    ]
    # -- Generate price information
    average_price = stats.mean(prices)
    n_items = len(prices)
    max_price = max(prices)
    min_price = min(prices)
    
    # -- Generate output information
    output = {
        "row_id": row.get("id"),
        "purchase_time": row.get("purchaseDateTimeString"),
        "total_cost": row.get("price").get("amount"),
        "merchant_id": row.get("merchant").get("merchantId"),
        "number_items": n_items,
        "average_item_price": average_price,
        "min_item_price": min_price,
        "max_item_price": max_price
    }
    return output, _items


def load_StoreboxData(path: str):
    """Load storebox data from path
    
    Parameters
    ---------
    path : str : path to the JSON file
    
    RETURNS
    -------
    tuple(dict, dict) : dictionary of summaries and items
    """
    with open(path, "r") as inputf:
        try:
            contents = json.load(inputf)
        except Exception as e:
            raise e("Has to be valid json.")
    # --
    summary_list = []
    items_list = []
    for row in contents:
        summary, _items = create_Summary(row)
        summary_list.append(summary)
        items_list.append(_items)
    
    # --
    all_items = [row for sublist in items_list for row in sublist]
    return summary_list, all_items
