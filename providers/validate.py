import argparse
import sys
import json
from stellar_sdk import Keypair, Network, Server, TransactionBuilder, Account, Asset
from horizon import client_horizon_create, horizon_passphrase,torplus_token_asset_name,torplus_issuer_address

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Verify that the provided account can be used in TorPlus network.')
    parser.add_argument('account_address', help='Stellar address of the account to validate')

    args = parser.parse_args()
    server = client_horizon_create()
    kp = Keypair.from_public_key(args.account_address)

    account = server.load_account(account_id=kp.public_key)
    account_full = server.accounts().account_id(account_id=kp.public_key).call()
    balances = account_full['balances']

    torplus_token_balance = [x for x in balances if ((x.get('asset_code') == torplus_token_asset_name) and (x.get('asset_issuer') == torplus_issuer_address))]

    if not torplus_token_balance:
        print(f"Account does not contain torplus_token asset ({torplus_token_asset_name}/{torplus_issuer_address}), please make sure trustlines are set correctly")
        sys.exit(0)

    print(f"Account validated correctly, you can use acconut {args.account_address} with TorPlus.")
    print(f"Current torplus_token balance is {torplus_token_balance[0].get('balance')}")


