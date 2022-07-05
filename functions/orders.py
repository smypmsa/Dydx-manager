import config as conf

from dydx3 import Client

from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import ORDER_SIDE_SELL
from dydx3.constants import ORDER_SIDE_BUY
from dydx3.constants import ORDER_TYPE_MARKET
from dydx3.constants import ORDER_STATUS_OPEN
from dydx3.constants import TIME_IN_FORCE_IOC


def create_market_order(client: Client, side: str, size: str):
    account_response = client.private.get_account()
    position_id = account_response.data['account']['positionId']

    # TODO: add getting prices from the orderbook
    # TODO: take out market argument into the config file
    price = conf.SELL_MIN_PRICE if side == ORDER_SIDE_SELL else conf.BUY_MAX_PRICE
    placed_order = client.private.create_order(
        position_id=position_id,
        market=MARKET_BTC_USD,
        side=side,
        order_type=ORDER_TYPE_MARKET,
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=100613988637,
        time_in_force=TIME_IN_FORCE_IOC)
    return placed_order


def get_number_of_opened_orders(client: Client):
    all_orders = client.private.get_orders(
        market=MARKET_BTC_USD,
        status=ORDER_STATUS_OPEN,
        limit=5)
    return len(all_orders.data['orders'])

# TODO: def get positions
# TODO: calculate fees paid / estimated rewards
