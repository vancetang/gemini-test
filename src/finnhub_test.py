# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "dotenv",
#     "finnhub-python",
#     "load-dotenv",
# ]
# ///
import os
import finnhub
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設定 API 金鑰
api_key = os.environ.get("FINNHUB_API_KEY")

if api_key is None:
    raise ValueError("FINNHUB_API_KEY 環境變數未設定")

finnhub_client = finnhub.Client(api_key=api_key)

'''
可參考：https://pypi.org/project/finnhub-python/
'''

# Quote
print(finnhub_client.quote('AAOI'))

# Financials as reported
# print(finnhub_client.financials_reported(symbol='AAOI', freq='annual'))
