# ================== Settings ==================

chain   = 'Starknet' # ERC20 | OKTC | Arbitrum One | zkSync Lite | zkSync Era | Optimism | Harmony | Starknet
token   = 'ETH' # ETH | ONE | CORE. To add other coins, you need to add them below in the links dictionary

OKX_2FA = "your_okx_2fa"
EMAIL_LOGIN = "your_email_login"
EMAIL_2FA = "your_email_2fa"

links = {
    'ETH'   : {'link' : 'https://www.okx.cab/ru/balance/withdrawal-address/eth/2',  'token' : 'ETH'}, # it's for all the coins in the chains : ERC20 | OKTC | Arbitrum one | zkSync Lite | zkSync Era | Optimism | Starknet
    'ONE'   : {'link' : 'https://www.okx.cab/ru/balance/withdrawal-address/one/1926',  'token' : 'ONE'}, # it's for the ONE coin on the Harmony network
    'CORE'  : {'link' : 'https://www.okx.cab/ru/balance/withdrawal-address/core/2806', 'token' : 'CORE'}, # it's for the CORE coin on the CORE network
}

CHROME_VERSION = 119 # Change to your version of chrome if you get an error

with open(f"wallets.txt", "r") as f:
    WALLETS = [row.strip() for row in f]
