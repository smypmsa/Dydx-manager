import config as conf

from dydx3 import Client
from dydx3.constants import POSITION_STATUS_OPEN
from dydx3.constants import MARKET_BTC_USD
from dydx3.constants import MARKET_ETH_USD


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def calculate_margin(p):
    size = abs(float(p['size']))

    if p['market'] == MARKET_ETH_USD:
        if size < conf.MARKET_ETH['baseline_position_size']:
            return size * conf.IMR
        elif size >= conf.MARKET_ETH['baseline_position_size']:
            return size * (conf.IMR + conf.MARKET_ETH['imf']
                           * ((size - conf.MARKET_ETH['baseline_position_size'])
                              // conf.MARKET_ETH['incremental_position_size']))
        else:
            raise Exception('Invalid position size')

    if p['market'] == MARKET_BTC_USD:
        if size < conf.MARKET_BTC['baseline_position_size']:
            return size * conf.IMR
        elif size >= conf.MARKET_BTC['baseline_position_size']:
            return size * (conf.IMR + conf.MARKET_BTC['imf']
                           * ((size - conf.MARKET_BTC['baseline_position_size'])
                              // conf.MARKET_BTC['incremental_position_size']))
        else:
            raise Exception('Invalid position size')


def get_account(wallet_name: str, host: str, wallet_credentials: dict, parameters: dict):
    # Create a wallet object
    client = Client(
        host=host,
        api_key_credentials=wallet_credentials['API_CREDENTIALS'],
        stark_private_key=wallet_credentials['STARK_PRIVATE_KEY'],
        stark_public_key=wallet_credentials['STARK_PUBLIC_KEY'],
        stark_public_key_y_coordinate=wallet_credentials['STARK_PUBLIC_KEY_Y_COORDINATE'],
        default_ethereum_address=wallet_credentials['DEFAULT_ETHEREUM_ADDRESS'],
    )

    # Get details on account (wallet)
    acc = client.private.get_account().data['account']
    positions = client.private.get_positions(status=POSITION_STATUS_OPEN).data['positions']
    equity = round(float(acc['equity']), 2)

    # Get oracle prices to calculate required margin
    price_eth = float(client.public.get_markets(market=MARKET_ETH_USD).data['markets'][MARKET_ETH_USD]['oraclePrice'])
    price_btc = float(client.public.get_markets(market=MARKET_BTC_USD).data['markets'][MARKET_BTC_USD]['oraclePrice'])

    # Calculate margin usage
    # Assuming we use only two markets: ETH and BTC
    pos_sum = sum([calculate_margin(p) * price_eth
                   if p['market'] == MARKET_ETH_USD
                   else calculate_margin(p) * price_btc
                   for p in positions])

    margin_usage = round(1 - (equity - pos_sum) / equity, 2)

    # Print results
    if margin_usage > 0.7:
        print(f"{bcolors.WARNING}{wallet_name} - {margin_usage} - {equity}{bcolors.ENDC}")
    else:
        print(f"{bcolors.OKGREEN}{wallet_name} - {margin_usage} - {equity}{bcolors.ENDC}")

    return margin_usage, equity
