import config as conf
import functions.margin as marg
import transfer as tr
import time


def rebalance_margin(margin_diff=0.03, safe_stop=20000):
    message = []

    if margin_diff < 0.01:
        raise Exception("Margin diff should not be less than 0.01.")

    if margin_diff > 0.1:
        raise Exception("Margin diff should not be greater than 0.1.")

    for pair in conf.WALLET_PAIRS:
        time.sleep(5)

        wallet1 = pair[0]
        wallet2 = pair[1]
        status = ""
        # Get wallet data for each wallet in the pair
        for w in conf.WALLETS:
            if w['wallet_name'] == wallet1:
                margin1, equity1 = marg.get_account(w['wallet_name'],
                                                    conf.HOST,
                                                    w['data'],
                                                    conf.PARAMETERS)
            elif w['wallet_name'] == wallet2:
                margin2, equity2 = marg.get_account(w['wallet_name'],
                                                    conf.HOST,
                                                    w['data'],
                                                    conf.PARAMETERS)
            else:
                continue

        # Check margin usage difference
        if abs(margin1 - margin2) > margin_diff:
            if margin1 > margin2:
                # Then send funds from wallet2 to wallet1
                amount_to_send = round((equity2 - equity1) / 2, 2)

                if amount_to_send > safe_stop:
                    raise Exception("Limit for transfer reached (20k USDC). Please check accounts manually.")

                status = tr.transfer(wallet2, wallet1, amount_to_send)
                print(f"Pair {wallet1} and {wallet2} rebalanced. {amount_to_send} transferred ({status}).")
                message.append(f"{wallet1} - {wallet2} - {str(amount_to_send)} rebalanced ({status}).")

            elif margin2 > margin1:
                # Then send funds from wallet1 to wallet2
                amount_to_send = round((equity1 - equity2) / 2, 2)

                if amount_to_send > safe_stop:
                    raise Exception("Limit for transfer reached (10k USDC). Please check accounts manually.")

                status = tr.transfer(wallet1, wallet2, amount_to_send)
                print(f"Pair {wallet1} and {wallet2} rebalanced. "
                      f"{amount_to_send} transferred.")
                message.append(f"{wallet1} - {wallet2} - {str(amount_to_send)} rebalanced ({status}).")

            else:
                raise Exception("Invalid option picked while rebalancing wallets.")

        else:
            print(f"Pair {wallet1} and {wallet2} has "
                  f"the diff of {round(abs(margin1 - margin2), 2)}. No need to rebalance.")
            message.append(f"{wallet1} - {wallet2} - no need to rebalance.")

    return message
