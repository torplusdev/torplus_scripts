import argparse
import sys
from stellar_sdk import Keypair, Network, Server, TransactionBuilder
from horizon import client_horizon_create, horizon_passphrase


def create_and_fund(funder, starting_balance):

    if starting_balance < 2.1:
        print("Min. balance for funding a new account is 2.1")
        sys.exit()

    server = client_horizon_create()
    source = Keypair.from_secret(funder)

    destination = Keypair.random()
    source_account = server.load_account(account_id=source.public_key)

    transaction = (
        TransactionBuilder(
        source_account=source_account,
        network_passphrase=horizon_passphrase(),
        base_fee=100,
        )
        .append_create_account_op( destination = destination.public_key, starting_balance = str(starting_balance)
     ).build()
    )

    transaction.sign(source)

    response = server.submit_transaction(transaction)

    print(f"Transaction hash: {response['hash']}")
    print(f"New Keypair: \n\taccount id: {destination.public_key}\n\tsecret seed: {destination.secret}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new account and fund it from a provided seed.')
    parser.add_argument('funder_seed', help='Stellar seed of the funding account')
    parser.add_argument('--balance', default=2.5, type=float, help='Starting stellar balance [XLM], will be deducted from the funder account.')

    args = parser.parse_args()

    create_and_fund(args.funder_seed, args.balance)

