import time
import threading
import functions.orders as dydx
import config as conf

from dydx3 import Client
from dydx3.constants import ORDER_SIDE_SELL
from dydx3.constants import ORDER_SIDE_BUY


def burn_fee(wallet_name: str, host: str, wallet_credentials: dict, parameters: dict):
    # Create a wallet object
    client = Client(
        host=host,
        api_key_credentials=wallet_credentials['API_CREDENTIALS'],
        stark_private_key=wallet_credentials['STARK_PRIVATE_KEY'],
        stark_public_key=wallet_credentials['STARK_PUBLIC_KEY'],
        stark_public_key_y_coordinate=wallet_credentials['STARK_PUBLIC_KEY_Y_COORDINATE'],
        default_ethereum_address=wallet_credentials['DEFAULT_ETHEREUM_ADDRESS'],
    )

    # Set up default parameters
    current_number_of_placed_orders = 0
    placed_order = ""

    # Run the main loop
    while current_number_of_placed_orders < parameters['ORDERS_LIMIT']:
        if placed_order:
            if placed_order.data['order']['side'] == ORDER_SIDE_SELL:
                placed_order = dydx.create_market_order(client=client,
                                                        side=ORDER_SIDE_BUY,
                                                        size=parameters['POSITION_SIZE'])
            elif placed_order.data['order']['side'] == ORDER_SIDE_BUY:
                placed_order = dydx.create_market_order(client=client,
                                                        side=ORDER_SIDE_SELL,
                                                        size=parameters['POSITION_SIZE'])
            else:
                raise NameError('Invalid order. Program has been stopped.')
        else:
            placed_order = dydx.create_market_order(client=client,
                                                    side=ORDER_SIDE_SELL,
                                                    size=parameters['POSITION_SIZE'])

        # Update counter
        current_number_of_placed_orders += 1

        # Print the details of placed order
        t = time.localtime()
        print('{}: order {} out of {} placed {} at {}'.format(
            wallet_name,
            current_number_of_placed_orders,
            parameters['ORDERS_LIMIT'],
            placed_order.data['order']['side'],
            time.strftime("%H:%M:%S", t)),
        )

        # Just an additional pause for resilience
        time.sleep(2)

        # Wait until all orders filled and go to the next order
        while dydx.get_number_of_opened_orders(client) != 0:
            time.sleep(3)

    print("{}: done!".format(
        wallet_name,
    ))


def burn_fee_all():
    # Threads array
    threads = []

    for wallet in conf.WALLETS:
        if wallet['wallet_name'] in conf.SKIP_WALLETS:
            continue
        thread = threading.Thread(target=burn_fee, args=(wallet['wallet_name'],
                                                         conf.HOST,
                                                         wallet['data'],
                                                         conf.PARAMETERS))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
