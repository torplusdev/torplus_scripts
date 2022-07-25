import argparse
import sys
from stellar_sdk import Keypair, Network, Server, TransactionBuilder, Asset
from horizon import client_horizon_create, horizon_passphrase, torplus_issuer_address,torplus_token_asset_name


default_torplus_token_limit = "1000"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sets up an existing and funded account for using in TorPlus network.')
    parser.add_argument('account_seed', help='Stellar seed of the account')

    args = parser.parse_args()

    server = client_horizon_create()
    source = Keypair.from_secret(args.account_seed)
    source_account = server.load_account(account_id=source.public_key)

    tptAsset = Asset(torplus_token_asset_name,torplus_issuer_address)

    transaction = (
        TransactionBuilder(
        source_account=source_account,
        network_passphrase=horizon_passphrase(),
        base_fee=100,
        )
        .append_change_trust_op(asset_code=torplus_token_asset_name, asset_issuer=torplus_issuer_address, limit=default_torplus_token_limit)
     ).build()

    transaction.sign(source)

    response = server.submit_transaction(transaction)

    print(f"Transaction hash: {response['hash']}")
    print(f"Your account ({source.public_key}) is now set up for TorPlus network. You may use your stellar seed for configuring TorPlus applications.")