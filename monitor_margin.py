import config as conf
import functions.margin as marg
import rebalance_margin as rebalance
from datetime import datetime, timedelta
import time
import telebot


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


def monitor_margin(hours=8, frequency=15, rebalance_required=False):
    # Set up tg bot
    bot = telebot.TeleBot(conf.BOT_ID)

    start_time = datetime.now()
    end_time = start_time + timedelta(hours=hours)

    while datetime.now() <= end_time:

        message1 = []
        print('--------------')
        message1.append('--------------')

        cur_time = datetime.now()
        message1.append(cur_time.strftime("%H:%M:%S"))
        print(cur_time.strftime("%H:%M:%S"))

        for wallet in conf.WALLETS:
            if wallet['wallet_name'] in conf.SKIP_WALLETS:
                # Skip
                continue
            else:
                margin, equity = marg.get_account(wallet['wallet_name'],
                                                  conf.HOST,
                                                  wallet['data'],
                                                  conf.PARAMETERS)
            message1.append(wallet['wallet_name'] + " - " + str(margin) + " - " + str(equity))

        status = bot.send_message(chat_id=conf.INTERNAL_CHATID_DYDX,
                                  text="\n".join(message1),
                                  disable_notification=True)

        if rebalance_required:
            message2 = []
            print('--------------')
            message2.append('--------------')
            message2 = rebalance.rebalance_margin()
            status = bot.send_message(chat_id=conf.INTERNAL_CHATID_DYDX,
                                      text="\n".join(message2),
                                      disable_notification=True)

        time.sleep(60 * frequency)

