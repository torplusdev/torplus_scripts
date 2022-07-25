'''
This script check native balance in all created accounts related to main account
and provide you follow info (info format = list):
- accounts with native balance equal zero
- accounts with native balance not equal zero
- account-candidates to merge to main account   # accounts with native balance zero and not in list NODE_ADDRESSES_FILE_PATH could be merged to main account
'''

from stellar_sdk import Server

server = Server(horizon_url="https://horizon.stellar.org")
#server = Server(horizon_url="https://api-horizon.torplus.com") ### TEST server
account = "GBUOWEFRO5KA2K5C5BZQURRFYZQIZASQLP76UJP762NEXQ4BCBYLG6L5"
NODE_ADDRESSES_FILE_PATH="node_addresses"   # file contain stellar (public) addresses that shouldn't be deleted

node_addresses = []
payments_records = []
payments_call_builder = (
    server.payments().for_account(account).order(desc=False).limit(200)
)  # limit can be set to a maximum of 200

payments_records += payments_call_builder.call()["_embedded"]["records"]
while page_records := payments_call_builder.next()["_embedded"]["records"]:
    payments_records += page_records

created_accounts = []

for payment_record in payments_records:
    if payment_record["type"] == "create_account":
        created_accounts.append(payment_record["account"])

created_accounts_zero_balance = []
created_accounts_non_zero_balance = []

for created_account in created_accounts:
    account_data_balances = server.load_account(account_id=created_account).raw_data
    for balance in account_data_balances["balances"]:
        if balance["asset_type"] == "native":
            native_balance = balance["balance"]
            print(f"Account: {created_account}, native balance: {native_balance}")
            if int(float(native_balance)) > 0:
                created_accounts_non_zero_balance.append(created_account)
            elif int(float(native_balance)) == 0:
                created_accounts_zero_balance.append(created_account)

with open(NODE_ADDRESSES_FILE_PATH) as file:
    for line in file:
        node_addresses.append(line.rstrip())

addresses_to_merge = list(set(created_accounts_non_zero_balance)-set(node_addresses))


len_created_accounts_zero_balance = len(created_accounts_zero_balance)
len_created_accounts_non_zero_balance = len(created_accounts_non_zero_balance)
len_addresses_to_merge = len(addresses_to_merge)

print(f"{len_created_accounts_zero_balance} accounts with native balance equal zero: {created_accounts_zero_balance}")
print(f"{len_created_accounts_non_zero_balance} accounts with native balance not equal zero: {created_accounts_non_zero_balance}")
print(f"{len_addresses_to_merge} account-candidates to merge to main account: {addresses_to_merge}")
