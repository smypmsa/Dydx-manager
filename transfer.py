import config as conf
from dydx3 import Client


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


def transfer(from_wallet_name, to_wallet_name, amount):
    if amount > 40000 or amount < 0:
        raise Exception('Invalid amount. Must be between 0 and 30 000.')

    # TODO: update these loops
    for w in conf.WALLETS:
        if w['wallet_name'] == from_wallet_name:
            sender_client = Client(
                host=conf.HOST,
                api_key_credentials=w['data']['API_CREDENTIALS'],
                stark_private_key=w['data']['STARK_PRIVATE_KEY'],
                stark_public_key=w['data']['STARK_PUBLIC_KEY'],
                stark_public_key_y_coordinate=w['data']['STARK_PUBLIC_KEY_Y_COORDINATE'],
                default_ethereum_address=w['data']['DEFAULT_ETHEREUM_ADDRESS'],
            )

            sender_acc = sender_client.private.get_account()
            sender_pos = sender_acc.data['account']['positionId']
            break

    for w in conf.WALLETS:
        if w['wallet_name'] == to_wallet_name:
            receiver_client = Client(
                host=conf.HOST,
                api_key_credentials=w['data']['API_CREDENTIALS'],
                stark_private_key=w['data']['STARK_PRIVATE_KEY'],
                stark_public_key=w['data']['STARK_PUBLIC_KEY'],
                stark_public_key_y_coordinate=w['data']['STARK_PUBLIC_KEY_Y_COORDINATE'],
                default_ethereum_address=w['data']['DEFAULT_ETHEREUM_ADDRESS'],
            )

            receiver_acc = receiver_client.private.get_account()
            receiver_pos = receiver_acc.data['account']['positionId']
            receiver_id = receiver_acc.data['account']['id']
            receiver_stark = receiver_acc.data['account']['starkKey']
            break

    # TODO: generate expiration
    status_transfer = sender_client.private.create_transfer(str(amount),
                                                            sender_position_id=sender_pos,
                                                            receiver_position_id=receiver_pos,
                                                            receiver_account_id=receiver_id,
                                                            receiver_public_key=receiver_stark,
                                                            expiration='2023-05-29T22:49:31.588Z')

    last_transfer = sender_client.private.get_transfers(limit=1).data['transfers'][0]

    # Print results
    if last_transfer['status'] != 'CONFIRMED':
        print(f"{bcolors.WARNING}Transaction {last_transfer['status']}{bcolors.ENDC}")
    else:
        print(f"{bcolors.OKGREEN}Transaction {last_transfer['status']}{bcolors.ENDC}")

    return last_transfer['status']
