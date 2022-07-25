import argparse
import sys
from stellar_sdk import Keypair, Network, Server, TransactionBuilder, Asset
from horizon import client_horizon_create, horizon_passphrase, torplus_issuer_address,torplus_token_asset_name, torplus_distribution_address
import decimal
from decimal import Decimal,getcontext

default_base_fee = 200
default_max_overprice_factor = 1.03

const_method_offer = 1
const_method_pay_strict = 2

convert_method = const_method_pay_strict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts TPT to XLM for an existing account with a positive TPT balance')
    parser.add_argument('account_seed', help='Stellar seed of the account')
    parser.add_argument('tpt_amount', help='Amount of TPT to sell')
    parser.add_argument('tpt_price', help='Price of TPT in [XLM] to sell for')

    args = parser.parse_args()

    server = client_horizon_create()
    source = Keypair.from_secret(args.account_seed)
    source_account = server.load_account(account_id=source.public_key)

    tptAsset = Asset(torplus_token_asset_name,torplus_issuer_address)

    getcontext().prec = 7

    if convert_method == const_method_offer:
        transaction = (
            TransactionBuilder(
                source_account=source_account,
                network_passphrase=horizon_passphrase(),
                base_fee=default_base_fee,
            )
                .append_manage_sell_offer_op(selling_code=torplus_token_asset_name, selling_issuer=torplus_issuer_address,buying_code="XLM",buying_issuer=None,amount=args.tpt_amount, price=args.tpt_price)
        ).build()
    elif convert_method == const_method_pay_strict:
        transaction = (
            TransactionBuilder(
            source_account=source_account,
            network_passphrase=horizon_passphrase(),
            base_fee=default_base_fee,
            )
                .append_path_payment_strict_receive_op(destination=torplus_distribution_address,
                                                       send_code=torplus_token_asset_name,
                                                       send_issuer=torplus_issuer_address, dest_amount=str(
                    Decimal(args.tpt_amount) * Decimal(args.tpt_price)),
                                                       dest_code="XLM", dest_issuer=None, source=source.public_key,
                                                       send_max=str(Decimal(float(args.tpt_amount) * float(
                                                           default_max_overprice_factor))), path=[])
         ).build()
    else:
        print("Unexpected convert_method")
        raise ValueError

    transaction.sign(source)

    response = server.submit_transaction(transaction)

    print(f"Transaction hash: {response['hash']}")
    print(f"Conversion has been successful. Your account ({source.public_key}) has been granted balance according to sold amount. (Note that the price serves essentially as min. price and can vary according to orders on book)")