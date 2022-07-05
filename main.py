import burn_fee as burn
import monitor_margin as monitor
import transfer as tr
import rebalance_margin as rebalance

menu_options = {
    1: 'Monitor and rebalance (default values)',
    2: 'Burn fee',
    3: 'Transfer (L2)',
    4: 'Rebalance wallets (L2)',
    0: 'Exit',
}


def print_menu():
    print("--------------\nUnofficial dYdX helper\n--------------")
    print("What you'd like to do today?\n--------------")
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def option1(h, m, rebalance_required):
    rebalance_flag = False

    if rebalance_required == 'yes':
        rebalance_flag = True
        print('Rebalance activated.')

    if rebalance_flag == False:
        print('Rebalance not acitvated.')

    monitor.monitor_margin(hours=h, frequency=m, rebalance_required=rebalance_flag)


def option2():
    burn.burn_fee_all()


def option3(sender_name, receiver_name, amount_usdc):
    tr.transfer(sender_name, receiver_name, amount_usdc)


def option4(margin_diff, safe_stop):
    rebalance.rebalance_margin(margin_diff=margin_diff, safe_stop=safe_stop)


if __name__ == '__main__':
    while True:
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        # Check what choice was entered and act accordingly
        if option == 1:
            hours = int(input('How many hours should monitoring be performed? Enter a number: '))
            mins = int(input('How often should check be performed? Enter a number (minutes): '))
            rebalance_req = str(input('Is rebalancing required? Enter Yes/No: ')).lower()
            print("OK. Let's do it!")
            option1(h=hours, m=mins, rebalance_required=rebalance_req)
        elif option == 2:
            print("Let's burn them all!")
            option2()
        elif option == 3:
            print("Let's get into details!")
            sender = str(input('Who is the sender? Enter a wallet name: '))
            receiver = str(input('Who is the receiver? Enter a wallet name: '))
            amount = int(input('What amount of USDC would you like to transfer? Enter a number: '))
            option3(sender_name=sender, receiver_name=receiver, amount_usdc=amount)
        elif option == 4:
            print("Let's rebalance them all!")
            diff = float(input('What margin diff should we consider for rebalancing? Enter a float number: '))
            max_stop = int(input('What is the limit for transfer (max amount which the '
                                  'script can send)? Enter a number: '))
            option4(margin_diff=diff, safe_stop=max_stop)
        elif option == 0:
            print('Bye!')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 2')
