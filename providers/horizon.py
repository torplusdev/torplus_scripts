from stellar_sdk import Server, Network

torplus_issuer_address = "GC4EEF32WLRFI7ZU7SKZ4Q7PMITKYAAMZK65AKD2PLI6E5WKYCN7OZCE"
torplus_distribution_address = "GBRQ4L76ERJ7XQXC3UX7LK3ZB45RHQ43WUHSEWS3K26LMMKBYB4WSBVN"
torplus_token_asset_name = "TPT"

def client_horizon_create() :
    return Server(horizon_url="https://horizon.stellar.org")

def horizon_passphrase() :
    return Network.PUBLIC_NETWORK_PASSPHRASE