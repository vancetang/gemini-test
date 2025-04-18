import os
import requests
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設定 API 金鑰
api_key = os.environ.get("FINANCIAL_DATASETS_API_KEY")

if not api_key:
    print(
        "錯誤：找不到 FINANCIAL_DATASETS_API_KEY 環境變數。請確定 .env 檔案存在且包含 FINANCIAL_DATASETS_API_KEY。"
    )
    exit()

# add your API key to the headers
headers = {"X-API-KEY": api_key}

# set your query params
# 目前使用的token只能查詢免費的股票代號
ticker = "NVDA"  # stock ticker
period = "annual"  # possible values are 'annual', 'quarterly', or 'ttm'
limit = 30  # number of periods to return

# create the URL
url = (
    f"https://api.financialdatasets.ai/financial-metrics"
    f"?ticker={ticker}"
    f"&period={period}"
    f"&limit={limit}"
)

# make API request
response = requests.get(url, headers=headers)

# parse financial_metrics from the response
financial_metrics = response.json().get("financial_metrics")

print(financial_metrics)
