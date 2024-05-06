import pandas as pd
import numpy as np
import asyncio
from datetime import datetime
from volstreet.utils.core import parse_symbol, custom_round
from volstreet import config
from volstreet.utils import notifier, filter_orderbook_by_time
from volstreet.angel_interface.interface import (
    fetch_quotes,
    fetch_book,
    lookup_and_return,
)
from volstreet.trade_interface import execute_orders, cancel_pending_orders
from volstreet.strategies.tools import filter_orders_by_strategy


def get_current_state_of_strategy(
    orderbook: list,
    index: str,
    order_tag: str,
    with_pnl: bool = True,
) -> pd.DataFrame:
    """
    Returns the present state of a strategy. This is qty, tokens, and symbols for a given order tag.
    Active quantity is increased for 'BUY' transactions and decreased for 'SELL' transactions.

    :param orderbook: List of orderbook entries.
    :param index: The index to search for.
    :param order_tag: The order tag to search for.
    :param with_pnl: Whether to include PnL in the output.
    :return: A list dataframe with the following columns:
        - tradingsymbol: The symbol of the contract.
        - symboltoken: The token of the contract.
        - lotsize: The lot size of the contract.
        - netqty: The net quantity of the contract.
        - active_lots: The number of active lots.
        - underlying: The underlying of the contract.
        - expiry: The expiry of the contract.
        - strike: The strike of the contract.
        - option_type: The option type of the contract.
    """

    # Filtering orders and making a dataframe
    filtered_orders = filter_orders_by_strategy(orderbook, order_tag, index)
    if not filtered_orders:
        return pd.DataFrame()
    df = pd.DataFrame(filtered_orders)

    # Converting data types
    df["filledshares"] = df["filledshares"].astype(int)
    df["lotsize"] = df["lotsize"].astype(int)

    # Converting filledshares to a signed number
    df["filledshares"] = df["filledshares"] * np.where(
        df.transactiontype == "BUY", 1, -1
    )

    # Filtering out incomplete orders
    df = df[df["status"] == "complete"]

    if df.empty:
        return pd.DataFrame()

    grouped = df.groupby("tradingsymbol")
    state = (
        grouped.agg({"filledshares": "sum", "symboltoken": "first", "lotsize": "first"})
        .reset_index()
        .rename(columns={"filledshares": "netqty"})
    )

    state["active_lots"] = state["netqty"] // state["lotsize"]
    state[["underlying", "expiry", "strike", "option_type"]] = (
        state["tradingsymbol"].apply(parse_symbol).to_list()
    )

    if with_pnl:
        state["net_value"] = grouped.apply(
            lambda x: np.dot(x["filledshares"], x["averageprice"]), include_groups=False
        ).values
        ltp_data = fetch_quotes([tok for tok in state.symboltoken], structure="dict")
        ltp_data = {k: v["ltp"] for k, v in ltp_data.items()}
        state["ltp"] = state["symboltoken"].apply(ltp_data.get)
        state["outstanding_value"] = state["netqty"] * state["ltp"]
        state["pnl"] = state["outstanding_value"] - state["net_value"]
    return state


def prepare_exit_params(
    positions: list[dict],
    max_lot_multiplier: int = 30,
    ltp_missing: bool = True,
) -> list[dict]:
    positions = [position for position in positions if position["netqty"]]
    order_params_list = []
    if ltp_missing:
        prices = fetch_quotes(
            [position["symboltoken"] for position in positions],
            structure="dict",
            from_source=True,
        )
        positions = [
            {**position, "ltp": prices[position["symboltoken"]]["ltp"]}
            for position in positions
        ]
    for position in positions:
        net_qty = int(position["netqty"])
        lot_size = int(position["lotsize"])
        max_order_qty = max_lot_multiplier * lot_size

        if net_qty == 0:
            continue
        action = "SELL" if net_qty > 0 else "BUY"
        total_qty = abs(net_qty)

        execution_price = (
            float(position["ltp"]) * (1 - config.LIMIT_PRICE_BUFFER)
            if action == "SELL"
            else float(position["ltp"]) * (1 + config.LIMIT_PRICE_BUFFER)
        )
        execution_price = custom_round(execution_price)

        while total_qty > 0:
            order_qty = min(total_qty, max_order_qty)
            params = {
                "variety": "NORMAL",
                "ordertype": "LIMIT",
                "price": max(execution_price, 0.05),
                "tradingsymbol": position["tradingsymbol"],
                "symboltoken": position["symboltoken"],
                "transactiontype": action,
                "exchange": config.token_exchange_dict[position["symboltoken"]],
                "producttype": "CARRYFORWARD",
                "duration": "DAY",
                "quantity": int(order_qty),
                "ordertag": "Error induced exit",
            }
            order_params_list.append(params)
            total_qty -= order_qty

    return order_params_list


def exit_positions(execution_time: datetime, index: str, identifier: str):
    order_book = fetch_book("orderbook", from_api=True)
    order_book = filter_orderbook_by_time(order_book, start_time=execution_time)
    pending_orders = lookup_and_return(
        order_book, ["ordertag", "status"], [identifier, "open"], "orderid"
    )
    if pending_orders:
        cancel_pending_orders(pending_orders, variety="NORMAL")
    active_positions = get_current_state_of_strategy(
        order_book, index, identifier, with_pnl=False
    )

    if active_positions.empty:
        notifier(
            f"No positions at all for strategy {identifier}",
            webhook_url=config.ERROR_NOTIFICATION_SETTINGS["url"],
        )
        return

    active_positions = active_positions.to_dict(orient="records")
    exit_params = prepare_exit_params(active_positions, ltp_missing=True)
    if not exit_params:
        notifier(
            f"No ACTIVE positions for strategy {identifier}",
            webhook_url=config.ERROR_NOTIFICATION_SETTINGS["url"],
        )
        return
    asyncio.run(execute_orders(exit_params))
