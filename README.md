# 🧪 gemini-test

此專案用於測試 Google Gemini API 的功能。

## 🌐 可用語言

[![English](https://img.shields.io/badge/English-Click-yellow)](README_en.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-Click-orange)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-Click-green)](README_zh-CN.md)

## 🔧 安裝

建議使用 `uv` 來管理 Python 環境與相依套件。

1.  🔑 **取得 Google Gemini API 金鑰:**
    前往 [Google AI Studio](https://aistudio.google.com/apikey) 建立您的 API 金鑰。

2.  📄 **設定環境變數:**
    複製 `.env.tpl` 檔案並重新命名為 `.env`：
    ```bash
    copy .env.tpl .env
    ```
    接著，編輯 `.env` 檔案，將您取得的 API 金鑰填入 `GOOGLE_API_KEY` 欄位。

3.  🛠️ **安裝 uv:**
    *   **建議 (跨平台):** 請參考 [uv 官方文件](https://github.com/astral-sh/uv#installation) 進行安裝。
    *   **Windows (使用 Chocolatey):**
        ```bash
        choco install -y uv
        ```

4.  📦 **同步相依套件:**
    在專案根目錄執行以下指令，`uv` 會讀取 `pyproject.toml` (或 `requirements.txt`) 並安裝所需的套件：
    ```bash
    uv sync
    ```

## 🚀 使用方式

### 🌍 Gemini 翻譯 README.md
```python
uv run src/translate.py
```

> **📝 注意**  
> 目前使用的模型為 gemini-2.5-flash-preview-04-17，處理小型檔案，速度表現與其他模型相差不大。


### 🌍 Gemini 翻譯指定Properties
```python
uv run src/transprop.py <properties_file 不含附檔名>
```
例如：檔案為 `test.properties`
```bash
uv run src/transprop.py test
```

> **⚠️ 警告**  
> 由於 properties 檔案通常包含大量資料，建議使用 gemini-2.0-flash 模型以確保高效處理。
