# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "finnhub-python",
# ]
# ///
import os
import finnhub

# 設定 API 金鑰
api_key = os.environ.get("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(api_key=api_key)

'''
可參考：https://pypi.org/project/finnhub-python/
'''

# Quote
print(finnhub_client.quote('AAOI'))

# Financials as reported
# print(finnhub_client.financials_reported(symbol='AAOI', freq='annual'))
