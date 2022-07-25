from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError, Ed25519SecretSeedInvalidError
import argparse
from sys import exit
from textwrap import dedent


server = Server(horizon_url="https://horizon.stellar.org")


def get_nodes_adresses(path):
    node_addresses = []
    with open(path) as file:
        for line in file:
            node_addresses.append(line.rstrip())
    return node_addresses


def top_up_account(source_key, destination_id):
    # First, check to make sure that the destination account exists.
    # You could skip this, but if the account does not exist, you will be charged
    # the transaction fee when the transaction fails.
    try:
        server.load_account(destination_id)
    except NotFoundError:
        # If the account is not found, surface an error message for logging.
        raise Exception("The destination account does not exist!")

    # If there was no error, load up-to-date information on your account.
    source_account = server.load_account(source_key.public_key)

    # Let's fetch base_fee from network
    base_fee = 100

    # Start building the transaction.
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
            # Because Stellar allows transaction in many currencies, you must specify the asset type.
            # Here we are sending Lumens.
            .append_payment_op(destination=destination_id, asset=Asset.native(), amount="5")
            # A memo allows you to add your own metadata to a transaction. It's
            # optional and does not affect how Stellar treats the transaction.
            .add_text_memo("Top up")
            .build()
    )

    # Sign the transaction to prove you are actually the person sending it.
    transaction.sign(source_key)

    try:
        # And finally, send it off to Stellar!
        response = server.submit_transaction(transaction)
        print(f"Response: {response}")
    except (BadRequestError, BadResponseError) as err:
        print(f"Something went wrong!\n{err}")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=dedent('''\
                                     Check wallets balance and top up it
                                     -----------------------------------
                                     Usage examples:
                                     python3 check_balance.py --node-file ./node_addresses --top-up-balance no --needed-balance 5 --min-balance 2 SAEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                                     '''))

    parser.add_argument('seed', help='Stellar seed of the source account')
    parser.add_argument('--node-file', default="/root/torplus_tools/providers/node_addresses", type=str, help='Path to the file with nodes adresses')
    parser.add_argument('--top-up-balance', default="no", type=str, help='Top up balance on node. If yes will be toped up for each node. If no will just show balane.')
    parser.add_argument('--needed-balance', default="5", type=int, help='How mach you would like to have XLM on balance.')
    parser.add_argument('--min-balance', default="2", type=int, help='Skip balance topping up if node already has minimal balance')
    args = parser.parse_args()

    try:
        source_key = Keypair.from_secret(args.seed)
    except (BadRequestError, BadResponseError, Ed25519SecretSeedInvalidError) as err:
        print(f"Something went wrong!\n{err}")
        exit()

    if args.min_balance < 2:
        print("Min. balance for funding a new account is 2")
        exit()


    for address in get_nodes_adresses(args.node_file):
        account_data_balances = server.load_account(account_id=address).raw_data
        for balance in account_data_balances["balances"]:
            if balance["asset_type"] == "native":
                str_native_balance = balance["balance"]
                native_balance = int(round(float(str_native_balance)))
                BALANCE_TO_TOP_UP = args.needed_balance - native_balance
                print(f"Account: {address}, native balance: {str_native_balance}, to fill the balance to ~{args.needed_balance} we need to add ~{BALANCE_TO_TOP_UP}.")
                if args.top_up_balance == "yes":
                    if native_balance >= args.min_balance:
                        print(f"Native balance ({native_balance}) is more than minimal balance ({args.min_balance}). Balance is OK!")
                    elif native_balance < args.min_balance:
                        print(f"Native balance ({native_balance}) is lower than minimal balance ({args.min_balance}). Topping up with {BALANCE_TO_TOP_UP} XLM...")
                        top_up_account(source_key, address)
                elif args.top_up_balance == "no":
                    pass
                print("~~~~~")

