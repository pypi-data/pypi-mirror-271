# ------ Pyth Network ------
DEFAULT_PYTH_PRICE_SERVICE_URL = "https://hermes.pyth.network"

CONTRACT_ADDRESS = {
  # Arbitrum One
  42161: {
    "MULTICALL_ADDRESS": "0xcA11bde05977b3631167028862bE2a173976CA11",
    "CROSS_MARGIN_HANDLER_ADDRESS": "0xB189532c581afB4Fbe69aF6dC3CD36769525d446",
    "LIMIT_TRADE_HANDLER_ADDRESS": "0xeE116128b9AAAdBcd1f7C18608C5114f594cf5D6",
    "GLP_MANAGER_ADDRESS": "0x3963FfC9dff443c2A94f21b129D429891E32ec18",
    "CONFIG_STORAGE_ADDRESS": "0xF4F7123fFe42c4C90A4bCDD2317D397E0B7d7cc0",
    "PERP_STORAGE_ADDRESS": "0x97e94BdA44a2Df784Ab6535aaE2D62EFC6D2e303",
    "VAULT_STORAGE_ADDRESS": "0x56CC5A9c0788e674f17F7555dC8D3e2F1C0313C0",
    "DIX_PRICE_ADAPTER_ADDRESS": "0x222918d230c5A29F334fFb3020aD57b8CeBD1B82",
    "GM_BTC_PRICE_ADAPTER_ADDRESS": "0x85680bba8a94c9be1DDd7Be802885DFCe95F8164",
    "GM_ETH_PRICE_ADAPTER_ADDRESS": "0x700083c72eBc86CbFc865830F5706a2DbC392f26",
    "TRADE_HELPER_ADDRESS": "0x963Cbe4cFcDC58795869be74b80A328b022DE00C",
    "ONCHAIN_PRICELENS_ADDRESS": "0x7D8eAa8dF02526c711F4ff1f97F6c5324212DBBa",
    "CALCULATOR_ADDRESS": "0x0FdE910552977041Dc8c7ef652b5a07B40B9e006",
  },
  # Arbitrum Sepolia
  421614: {
    "MULTICALL_ADDRESS": "0xcA11bde05977b3631167028862bE2a173976CA11",
    "CROSS_MARGIN_HANDLER_ADDRESS": "0xF21405bA59E79762C306c83298dbD10a8A285f2F",
    "LIMIT_TRADE_HANDLER_ADDRESS": "0x676715779e3bFaa9B1a98De4F1F0745cF4E65bcE",
    "VAULT_STORAGE_ADDRESS": "0x4D9DF83C94c54F75aC2870514C2AD72047f96BB8",
    "GLP_MANAGER_ADDRESS": "0x3963FfC9dff443c2A94f21b129D429891E32ec18",
    "PERP_STORAGE_ADDRESS": "0x8b0D385b260a2532205CB0012F1550F9310d1d77",
    "CONFIG_STORAGE_ADDRESS": "0xfc51C8c673C27e1b3D89688ef46D706A77CA28DB",
    "DIX_PRICE_ADAPTER_ADDRESS": "0x76473d85404D275F06E5835FFFc6006De0C4F0Ee",
    "GM_BTC_PRICE_ADAPTER_ADDRESS": "0x85680bba8a94c9be1DDd7Be802885DFCe95F8164",
    "GM_ETH_PRICE_ADAPTER_ADDRESS": "0x700083c72eBc86CbFc865830F5706a2DbC392f26",
    "TRADE_HELPER_ADDRESS": "0xFd89a05652492D748a94cD24c636e33054E9F4c2",
    "ONCHAIN_PRICELENS_ADDRESS": "0x2f035c75bE06cdDCA5E23649d9635f649Cb279E5",
    "CALCULATOR_ADDRESS": "0x35A301796949f5235f8fc3311E6013450aaf2354"
  },
  # Blast Mainnet
  81457: {
    "MULTICALL_ADDRESS": "0xcA11bde05977b3631167028862bE2a173976CA11",
    "CROSS_MARGIN_HANDLER_ADDRESS": "0xE7D96684A56e60ffBAAe0fC0683879da48daB383",
    "LIMIT_TRADE_HANDLER_ADDRESS": "0xcf533D0eEFB072D1BB68e201EAFc5368764daA0E",
    "CONFIG_STORAGE_ADDRESS": "0x9F09b53ee28a93951fe546dEfB24C0f908eEda22",
    "PERP_STORAGE_ADDRESS": "0x9c83e1046dA4727F05C6764c017C6E1757596592",
    "VAULT_STORAGE_ADDRESS": "0x97e94BdA44a2Df784Ab6535aaE2D62EFC6D2e303",
    "DIX_PRICE_ADAPTER_ADDRESS": "0x7557573E674B55Da6c25fEa9f648b019D1Dfd499",
    "TRADE_HELPER_ADDRESS": "0x9F1f13eBC178122C3ef6c14FA3A523680563F58b",
    "ONCHAIN_PRICELENS_ADDRESS": "0x9C67046f42eFfbA03d58aA54cB9C75aFDa38146e",
    "CALCULATOR_ADDRESS": "0x4307fbDCD9Ec7AEA5a1c2958deCaa6f316952bAb",
  }
}

# ------ ABI Path ------
ERC20_ABI_PATH = "abis/ERC20.json"
CROSS_MARGIN_HANDLER_ABI_PATH = "abis/CrossMarginHandler.json"
LIMIT_TRADE_HANDLER_ABI_PATH = "abis/LimitTradeHandler.json"
VAULT_STORAGE_ABI_PATH = "abis/VaultStorage.json"
GLP_MANAGER_ABI_PATH = "abis/GlpManager.json"
PERP_STORAGE_ABI_PATH = "abis/PerpStorage.json"
CONFIG_STORAGE_ABI_PATH = "abis/ConfigStorage.json"
CIX_PRICE_ADAPTER_ABI_PATH = "abis/CIXPriceAdapter.json"
GM_PRICE_ADAPTER_ABI_PATH = "abis/GMPriceAdapter.json"
TRADE_HELPER_ABI_PATH = "abis/TradeHelper.json"
ONCHAIN_PRICELENS_ABI_PATH = "abis/OnchainPricelens.json"
CALCULATOR_ABI_PATH = "abis/Calculator.json"

# ------ Market ------
MARKET_ETH_USD = 0
MARKET_BTC_USD = 1
MARKET_AAPL_USD = 2
MARKET_JPY_USD = 3
MARKET_XAU_USD = 4
MARKET_AMZN_USD = 5
MARKET_MSFT_USD = 6
MARKET_TSLA_USD = 7
MARKET_EUR_USD = 8
MARKET_XAG_USD = 9
MARKET_AUD_USD = 10
MARKET_GBP_USD = 11
MARKET_ADA_USD = 12
MARKET_MATIC_USD = 13
MARKET_SUI_USD = 14
MARKET_ARB_USD = 15
MARKET_OP_USD = 16
MARKET_LTC_USD = 17
MARKET_COIN_USD = 18
MARKET_GOOG_USD = 19
MARKET_BNB_USD = 20
MARKET_SOL_USD = 21
MARKET_QQQ_USD = 22
MARKET_XRP_USD = 23
MARKET_NVDA_USD = 24
MARKET_LINK_USD = 25
MARKET_USD_CHF = 26
MARKET_DOGE_USD = 27
MARKET_USD_CAD = 28
MARKET_USD_SGD = 29
MARKET_USD_CNH = 30
MARKET_USD_HKD = 31
MARKET_BCH_USD = 32
MARKET_MEME_USD = 33
MARKET_DIX_USD = 34
MARKET_JTO_USD = 35
MARKET_STX_USD = 36
MARKET_ORDI_USD = 37
MARKET_TIA_USD = 38
MARKET_AVAX_USD = 39
MARKET_INJ_USD = 40
MARKET_DOT_USD = 41
MARKET_SEI_USD = 42
MARKET_ATOM_USD = 43
MARKET_1000PEPE_USD = 44
MARKET_1000SHIB_USD = 45
MARKET_USD_SEK = 46
MARKET_ICP_USD = 47
MARKET_MANTA_USD = 48
MARKET_STRK_USD = 49
MARKET_PYTH_USD = 50

# ------ Assets ------
ASSET_ETH = "ETH"
ASSET_BTC = "BTC"
ASSET_AAPL = "AAPL"
ASSET_JPY = "JPY"
ASSET_XAU = "XAU"
ASSET_AMZN = "AMZN"
ASSET_MSFT = "MSFT"
ASSET_TSLA = "TSLA"
ASSET_EUR = "EUR"
ASSET_XAG = "XAG"
ASSET_AUD = "AUD"
ASSET_GBP = "GBP"
ASSET_ADA = "ADA"
ASSET_MATIC = "MATIC"
ASSET_SUI = "SUI"
ASSET_ARB = "ARB"
ASSET_OP = "OP"
ASSET_LTC = "LTC"
ASSET_COIN = "COIN"
ASSET_GOOG = "GOOG"
ASSET_BNB = "BNB"
ASSET_SOL = "SOL"
ASSET_QQQ = "QQQ"
ASSET_XRP = "XRP"
ASSET_USDC = "USDC"
ASSET_USDT = "USDT"
ASSET_DAI = "DAI"
ASSET_GLP = "GLP"
ASSET_NVDA = "NVDA"
ASSET_LINK = "LINK"
ASSET_CHF = "CHF"
ASSET_DOGE = "DOGE"
ASSET_CAD = "CAD"
ASSET_SGD = "SGD"
ASSET_CNH = "CNH"
ASSET_wstETH = "wstETH"
ASSET_HKD = "HKD"
ASSET_BCH = "BCH"
ASSET_MEME = "MEME"
ASSET_gmBTC = "gmBTC"
ASSET_gmETH = "gmETH"
ASSET_SEK = "SEK"
ASSET_DIX = "DIX"
ASSET_JTO = "JTO"
ASSET_STX = "STX"
ASSET_ORDI = "ORDI"
ASSET_TIA = "TIA"
ASSET_AVAX = "AVAX"
ASSET_INJ = "INJ"
ASSET_DOT = "DOT"
ASSET_SEI = "SEI"
ASSET_ATOM = "ATOM"
ASSET_1000SHIB = "1000SHIB"
ASSET_1000PEPE = "1000PEPE"
ASSET_ICP = "ICP"
ASSET_MANTA = "MANTA"
ASSET_STRK = "STRK"
ASSET_PYTH = "PYTH"

ASSETS = [ASSET_ETH, ASSET_BTC, ASSET_AAPL, ASSET_JPY, ASSET_XAU, ASSET_AMZN,
          ASSET_MSFT, ASSET_TSLA, ASSET_EUR, ASSET_XAG, ASSET_AUD, ASSET_GBP,
          ASSET_ADA, ASSET_MATIC, ASSET_SUI, ASSET_ARB, ASSET_OP, ASSET_LTC,
          ASSET_COIN, ASSET_GOOG, ASSET_BNB, ASSET_SOL, ASSET_QQQ, ASSET_XRP,
          ASSET_USDC, ASSET_USDT, ASSET_DAI, ASSET_GLP, ASSET_NVDA, ASSET_LINK,
          ASSET_CHF, ASSET_DOGE, ASSET_CAD, ASSET_SGD, ASSET_CNH, ASSET_wstETH,
          ASSET_HKD, ASSET_BCH, ASSET_MEME, ASSET_gmBTC, ASSET_gmETH, ASSET_SEK,
          ASSET_DIX, ASSET_JTO, ASSET_STX, ASSET_ORDI, ASSET_TIA, ASSET_AVAX,
          ASSET_INJ, ASSET_DOT, ASSET_SEI, ASSET_ATOM, ASSET_1000SHIB, ASSET_1000PEPE,
          ASSET_ICP, ASSET_MANTA, ASSET_STRK, ASSET_PYTH]


# ------ Token Profiles ------
TOKEN_PROFILE = {
  # Arbitrum One
  42161: {
    "USDC.e": {
      "symbol": "USDC.e",
      "address": "0xB853c09b6d03098b841300daD57701ABcFA80228",
      "asset": ASSET_USDC,
      "decimals": 6
    },
    "0xB853c09b6d03098b841300daD57701ABcFA80228": {
      "symbol": "USDC.e",
      "address": "0xB853c09b6d03098b841300daD57701ABcFA80228",
      "asset": ASSET_USDC,
      "decimals": 6
    },
    "USDT": {
      "symbol": "USDT",
      "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
      "asset": ASSET_USDT,
      "decimals": 6
    },
    "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9": {
      "symbol": "USDT",
      "address": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
      "asset": ASSET_USDT,
      "decimals": 6
    },
    "DAI": {
      "symbol": "DAI",
      "address": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
      "asset": ASSET_DAI,
      "decimals": 18
    },
    "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1": {
      "symbol": "DAI",
      "address": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
      "asset": ASSET_DAI,
      "decimals": 18
    },
    "WETH": {
      "symbol": "WETH",
      "address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
      "asset": ASSET_ETH,
      "decimals": 18
    },
    "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1": {
      "symbol": "WETH",
      "address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
      "asset": ASSET_ETH,
      "decimals": 18
    },
    "WBTC": {
      "symbol": "WBTC",
      "address": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
      "asset": ASSET_BTC,
      "decimals": 8
    },
    "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f": {
      "symbol": "WBTC",
      "address": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
      "asset": ASSET_BTC,
      "decimals": 8
    },
    "sGLP": {
      "symbol": "sGLP",
      "address": "0x5402B5F40310bDED796c7D0F3FF6683f5C0cFfdf",
      "asset": ASSET_GLP,
      "decimals": 18
    },
    "0x5402B5F40310bDED796c7D0F3FF6683f5C0cFfdf": {
      "symbol": "sGLP",
      "address": "0x5402B5F40310bDED796c7D0F3FF6683f5C0cFfdf",
      "asset": ASSET_GLP,
      "decimals": 18
    },
    "ARB": {
      "symbol": "ARB",
      "address": "0x912CE59144191C1204E64559FE8253a0e49E6548",
      "asset": ASSET_ARB,
      "decimals": 18
    },
    "0x912CE59144191C1204E64559FE8253a0e49E6548": {
      "symbol": "ARB",
      "address": "0x912CE59144191C1204E64559FE8253a0e49E6548",
      "asset": ASSET_ARB,
      "decimals": 18
    },
    "wstETH": {
      "symbol": "wstETH",
      "address": "0x5979D7b546E38E414F7E9822514be443A4800529",
      "asset": ASSET_wstETH,
      "decimals": 18
    },
    "0x5979D7b546E38E414F7E9822514be443A4800529": {
      "symbol": "wstETH",
      "address": "0x5979D7b546E38E414F7E9822514be443A4800529",
      "asset": ASSET_wstETH,
      "decimals": 18
    },
    "USDC": {
      "symbol": "USDC",
      "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
      "asset": ASSET_USDC,
      "decimals": 6
    },
    "0xaf88d065e77c8cC2239327C5EDb3A432268e5831": {
      "symbol": "USDC",
      "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
      "asset": ASSET_USDC,
      "decimals": 6
    },
    "gmBTC": {
      "symbol": "gmBTC",
      "address": "0x47c031236e19d024b42f8AE6780E44A573170703",
      "asset": ASSET_gmBTC,
      "decimals": 18
    },
    "0x47c031236e19d024b42f8AE6780E44A573170703": {
      "symbol": "gmBTC",
      "address": "0x47c031236e19d024b42f8AE6780E44A573170703",
      "asset": ASSET_gmBTC,
      "decimals": 18
    },
    "gmETH": {
      "symbol": "gmETH",
      "address": "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336",
      "asset": ASSET_gmETH,
      "decimals": 18
    },
    "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336": {
      "symbol": "gmETH",
      "address": "0x70d95587d40A2caf56bd97485aB3Eec10Bee6336",
      "asset": ASSET_gmETH,
      "decimals": 18
    },
  },
  # Arbitrum Sepolia
  421614: {
      "USDC.e": {
          "symbol": "USDC.e",
          "address": "0xB853c09b6d03098b841300daD57701ABcFA80228",
          "asset": ASSET_USDC,
          "decimals": 6
      },
      "0xB853c09b6d03098b841300daD57701ABcFA80228": {
          "symbol": "USDC.e",
          "address": "0xB853c09b6d03098b841300daD57701ABcFA80228",
          "asset": ASSET_USDC,
          "decimals": 6
      },
      "USDT": {
          "symbol": "USDT",
          "address": "0x20E58fC5E1ee3C596fb3ebD6de6040e7800e82E6",
          "asset": ASSET_USDT,
          "decimals": 6
      },
      "0x20E58fC5E1ee3C596fb3ebD6de6040e7800e82E6": {
          "symbol": "USDT",
          "address": "0x20E58fC5E1ee3C596fb3ebD6de6040e7800e82E6",
          "asset": ASSET_USDT,
          "decimals": 6
      },
      "DAI": {
          "symbol": "DAI",
          "address": "0x8D715a015aC0e064a3Cfb88DA755d346Aee65433",
          "asset": ASSET_DAI,
          "decimals": 18
      },
      "0x8D715a015aC0e064a3Cfb88DA755d346Aee65433": {
          "symbol": "DAI",
          "address": "0x8D715a015aC0e064a3Cfb88DA755d346Aee65433",
          "asset": ASSET_DAI,
          "decimals": 18
      },
      "WETH": {
          "symbol": "WETH",
          "address": "0xc88322Ec9526A7A98B7F58ff773b3B003C91ce71",
          "asset": ASSET_ETH,
          "decimals": 18
      },
      "0xc88322Ec9526A7A98B7F58ff773b3B003C91ce71": {
          "symbol": "WETH",
          "address": "0xc88322Ec9526A7A98B7F58ff773b3B003C91ce71",
          "asset": ASSET_ETH,
          "decimals": 18
      },
      "WBTC": {
          "symbol": "WBTC",
          "address": "0x4c08D11Bc95075AD992Bd7A5776D0D9813E264d5",
          "asset": ASSET_BTC,
          "decimals": 8
      },
      "0x4c08D11Bc95075AD992Bd7A5776D0D9813E264d5": {
          "symbol": "WBTC",
          "address": "0x4c08D11Bc95075AD992Bd7A5776D0D9813E264d5",
          "asset": ASSET_BTC,
          "decimals": 8
      },
      "sGLP": {
          "symbol": "sGLP",
          "address": "0x7AAF085e43f059105F7e1ECc525E8142fF962159",
          "asset": ASSET_GLP,
          "decimals": 18
      },
      "0x7AAF085e43f059105F7e1ECc525E8142fF962159": {
          "symbol": "sGLP",
          "address": "0x7AAF085e43f059105F7e1ECc525E8142fF962159",
          "asset": ASSET_GLP,
          "decimals": 18
      },
      "ARB": {
          "symbol": "ARB",
          "address": "0x4Dc3c929DDa7451012F408d1f376221621dD2a56",
          "asset": ASSET_ARB,
          "decimals": 18
      },
      "0x4Dc3c929DDa7451012F408d1f376221621dD2a56": {
          "symbol": "ARB",
          "address": "0x4Dc3c929DDa7451012F408d1f376221621dD2a56",
          "asset": ASSET_ARB,
          "decimals": 18
      },
      "wstETH": {
          "symbol": "wstETH",
          "address": "0xFc41505F4e24345E3797b6730a948a2B03a5eC5e",
          "asset": ASSET_wstETH,
          "decimals": 18
      },
      "0xFc41505F4e24345E3797b6730a948a2B03a5eC5e": {
          "symbol": "wstETH",
          "address": "0xFc41505F4e24345E3797b6730a948a2B03a5eC5e",
          "asset": ASSET_wstETH,
          "decimals": 18
      },
      "USDC": {
          "symbol": "USDC",
          "address": "0xEB27B05178515c7E6E51dEE159c8487A011ac030",
          "asset": ASSET_USDC,
          "decimals": 6
      },
      "0xEB27B05178515c7E6E51dEE159c8487A011ac030": {
          "symbol": "USDC",
          "address": "0xEB27B05178515c7E6E51dEE159c8487A011ac030",
          "asset": ASSET_USDC,
          "decimals": 6
      },
      "gmBTC": {
          "symbol": "gmBTC",
          "address": "0xC4605B61675654396f3b77F9D4c3bE661fa0d873",
          "asset": ASSET_gmBTC,
          "decimals": 18
      },
      "0xC4605B61675654396f3b77F9D4c3bE661fa0d873": {
          "symbol": "gmBTC",
          "address": "0xC4605B61675654396f3b77F9D4c3bE661fa0d873",
          "asset": ASSET_gmBTC,
          "decimals": 18
      },
      "gmETH": {
          "symbol": "gmETH",
          "address": "0x417B34E90990657BF6adC1Ecc2ac4B36069cc927",
          "asset": ASSET_gmETH,
          "decimals": 18
      },
      "0x417B34E90990657BF6adC1Ecc2ac4B36069cc927": {
          "symbol": "gmETH",
          "address": "0x417B34E90990657BF6adC1Ecc2ac4B36069cc927",
          "asset": ASSET_gmETH,
          "decimals": 18
      },
  },
}


DELISTED_MARKET = [
    MARKET_AAPL_USD,
    MARKET_AMZN_USD,
    MARKET_MSFT_USD,
    MARKET_TSLA_USD,
    MARKET_COIN_USD,
    MARKET_GOOG_USD,
    MARKET_QQQ_USD,
    MARKET_NVDA_USD
]

# ------ Market ----
MARKET_PROFILE = {
  MARKET_ETH_USD: {
    "name": "ETHUSD",
    "asset": ASSET_ETH,
    "display_decimal": 2,
  },
  MARKET_BTC_USD: {
    "name": "BTCUSD",
    "asset": ASSET_BTC,
    "display_decimal": 2,
  },
  MARKET_AAPL_USD: {
    "name": "AAPLUSD",
    "asset": ASSET_AAPL,
    "display_decimal": 2,
  },
  MARKET_JPY_USD: {
    "name": "JPYUSD",
    "asset": ASSET_JPY,
    "display_decimal": 8,
  },
  MARKET_XAU_USD: {
    "name": "XAUUSD",
    "asset": ASSET_XAU,
    "display_decimal": 2,
  },
  MARKET_AMZN_USD: {
    "name": "AMZNUSD",
    "asset": ASSET_AMZN,
    "display_decimal": 2,
  },
  MARKET_MSFT_USD: {
    "name": "MSFTUSD",
    "asset": ASSET_MSFT,
    "display_decimal": 2,
  },
  MARKET_TSLA_USD: {
    "name": "TSLAUSD",
    "asset": ASSET_TSLA,
    "display_decimal": 2,
  },
  MARKET_EUR_USD: {
    "name": "EURUSD",
    "asset": ASSET_EUR,
    "display_decimal": 5,
  },
  MARKET_XAG_USD: {
    "name": "XAGUSD",
    "asset": ASSET_XAG,
    "display_decimal": 3,
  },
  MARKET_AUD_USD: {
    "name": "AUDUSD",
    "asset": ASSET_AUD,
    "display_decimal": 5,
  },
  MARKET_GBP_USD: {
    "name": "GBPUSD",
    "asset": ASSET_GBP,
    "display_decimal": 5,
  },
  MARKET_ADA_USD: {
    "name": "ADAUSD",
    "asset": ASSET_ADA,
    "display_decimal": 4,
  },
  MARKET_MATIC_USD: {
    "name": "MATICUSD",
    "asset": ASSET_MATIC,
    "display_decimal": 4,
  },
  MARKET_SUI_USD: {
    "name": "SUIUSD",
    "asset": ASSET_SUI,
    "display_decimal": 4,
  },
  MARKET_ARB_USD: {
    "name": "ARBUSD",
    "asset": ASSET_ARB,
    "display_decimal": 4,
  },
  MARKET_OP_USD: {
    "name": "OPUSD",
    "asset": ASSET_OP,
    "display_decimal": 4,
  },
  MARKET_LTC_USD: {
    "name": "LTCUSD",
    "asset": ASSET_LTC,
    "display_decimal": 2,
  },
  MARKET_COIN_USD: {
    "name": "COINUSD",
    "asset": ASSET_COIN,
    "display_decimal": 2,
  },
  MARKET_GOOG_USD: {
    "name": "GOOGUSD",
    "asset": ASSET_GOOG,
    "display_decimal": 2,
  },
  MARKET_BNB_USD: {
    "name": "BNBUSD",
    "asset": ASSET_BNB,
    "display_decimal": 2,
  },
  MARKET_SOL_USD: {
    "name": "SOLUSD",
    "asset": ASSET_SOL,
    "display_decimal": 3,
  },
  MARKET_QQQ_USD: {
    "name": "QQQUSD",
    "asset": ASSET_QQQ,
    "display_decimal": 2,
  },
  MARKET_XRP_USD: {
    "name": "XRPUSD",
    "asset": ASSET_XRP,
    "display_decimal": 4,
  },
  MARKET_NVDA_USD: {
    "name": "NVDAUSD",
    "asset": ASSET_NVDA,
    "display_decimal": 2,
  },
  MARKET_LINK_USD: {
    "name": "LINKUSD",
    "asset": ASSET_LINK,
    "display_decimal": 3,
  },
  MARKET_USD_CHF: {
    "name": "USDCHF",
    "asset": ASSET_CHF,
    "display_decimal": 5,
  },
  MARKET_DOGE_USD: {
    "name": "DOGEUSD",
    "asset": ASSET_DOGE,
    "display_decimal": 5,
  },
  MARKET_USD_CAD: {
    "name": "USDCAD",
    "asset": ASSET_CAD,
    "display_decimal": 5,
  },
  MARKET_USD_SGD: {
    "name": "USDSGD",
    "asset": ASSET_SGD,
    "display_decimal": 5,
  },
  MARKET_USD_CNH: {
    "name": "USDCNH",
    "asset": ASSET_CNH,
    "display_decimal": 5,
  },
  MARKET_USD_HKD: {
    "name": "USDHKD",
    "asset": ASSET_HKD,
    "display_decimal": 5,
  },
  MARKET_BCH_USD: {
    "name": "BCHUSD",
    "asset": ASSET_BCH,
    "display_decimal": 2,
  },
  MARKET_MEME_USD: {
    "name": "MEMEUSD",
    "asset": ASSET_MEME,
    "display_decimal": 8,
  },
  MARKET_DIX_USD: {
    "name": "DIX",
    "asset": ASSET_DIX,
    "display_decimal": 4,
  },
  MARKET_JTO_USD: {
    "name": "JTOUSD",
    "asset": ASSET_JTO,
    "display_decimal": 4,
  },
  MARKET_STX_USD: {
    "name": "STXUSD",
    "asset": ASSET_STX,
    "display_decimal": 4,
  },
  MARKET_ORDI_USD: {
    "name": "ORDIUSD",
    "asset": ASSET_ORDI,
    "display_decimal": 3,
  },
  MARKET_TIA_USD: {
    "name": "TIAUSD",
    "asset": ASSET_TIA,
    "display_decimal": 4,
  },
  MARKET_AVAX_USD: {
    "name": "AVAXUSD",
    "asset": ASSET_AVAX,
    "display_decimal": 3,
  },
  MARKET_INJ_USD: {
    "name": "INJUSD",
    "asset": ASSET_INJ,
    "display_decimal": 3,
  },
  MARKET_DOT_USD: {
    "name": "DOTUSD",
    "asset": ASSET_DOT,
    "display_decimal": 3,
  },
  MARKET_SEI_USD: {
    "name": "SEIUSD",
    "asset": ASSET_SEI,
    "display_decimal": 4,
  },
  MARKET_ATOM_USD: {
    "name": "ATOMUSD",
    "asset": ASSET_ATOM,
    "display_decimal": 3,
  },
  MARKET_1000PEPE_USD: {
    "name": "1000PEPEUSD",
    "asset": ASSET_1000PEPE,
    "display_decimal": 8,
  },
  MARKET_1000SHIB_USD: {
    "name": "1000SHIBUSD",
    "asset": ASSET_1000SHIB,
    "display_decimal": 8,
  },
  MARKET_USD_SEK: {
    "name": "USDSEK",
    "asset": ASSET_SEK,
    "display_decimal": 5,
  },
  MARKET_ICP_USD: {
    "name": "ICPUSD",
    "asset": ASSET_ICP,
    "display_decimal": 3,
  },
  MARKET_MANTA_USD: {
    "name": "MANTAUSD",
    "asset": ASSET_MANTA,
    "display_decimal": 3,
  },
  MARKET_STRK_USD: {
    "name": "STRKUSD",
    "asset": ASSET_STRK,
    "display_decimal": 3,
  },
  MARKET_PYTH_USD: {
    "name": "PYTHUSD",
    "asset": ASSET_PYTH,
    "display_decimal": 4,
  },
}

# Address
ADDRESS_ZERO = "0x0000000000000000000000000000000000000000"
BYTE_ZERO = "0x0000000000000000000000000000000000000000000000000000000000000000"

# Math
MAX_UINT = 2 ** 256 - 1
BPS = 10000

EXECUTION_FEE = 3 * 10 ** 14

SECONDS = 1
MINUTES = 60
HOURS = 3600
DAYS = 86400
YEARS = 31536000
