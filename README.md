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

### 🌍 翻譯文字檔

此功能可將文字檔翻譯為多種語言（如英文 `en`、簡體中文 `zh-CN`），並產生對應語系的輸出檔案（例如：`README_en.md`、`README_zh-CN.md`）。

> [!NOTE]
> 目前是採用一次性讀檔翻譯，所以如果檔案文字太多可能會有問題!!。

執行指令格式如下：

```bash
uv run src/i18n_tool.py --name <filename> [--lang <language1,language2,...>]
```

範例：

```bash
uv run src/i18n_tool.py --name README.md --lang en
```

> [!NOTE]
> 目前使用的模型是 `gemini-2.5-flash-preview-04-17`，初步測試顯示，此模型雖然翻譯速度相較於 `2.0 Flash` 稍慢，但考量其具備推理功能且為最新版本，加上 `README.md` 檔案不大，翻譯時間也不會太長，因此選擇此模型進行初步測試與開發。
> 簡單翻譯使用 `gemini-2.5-flash-preview-04-17` 可設定 `thinking_budget=0` 關閉深度思考模式。


---

### 🌍 翻譯 `.properties` 檔案

此功能可將 `.properties` 檔案翻譯為多種語言（如英文 `en`、簡體中文 `zh-CN`），並產生對應語系的輸出檔案（例如：`test_en.properties`、`test_zh-CN.properties`）。

執行指令格式如下：

```bash
uv run src/i18n_props.py --name <filename> [--unicode] [--output-dir DIR] [--lang LANG1,LANG2,...]
```

範例：若要翻譯 `test.properties` 為 `英文`，且 `不使用 Unicode 編碼`：

```bash
uv run src/i18n_props.py --name test --lang en
```

> [!NOTE]
> `.properties` 檔案常包含大量文字內容，建議選用 `gemini-2.0-flash` 模型以提升翻譯效率與穩定性。


## 📄 PDF → Markdown 轉換工具

以 PyMuPDF + PyMuPDF4LLM 打造的 PDF → Markdown 轉換 CLI（src/pdf_to_markdown.py）。

- 特色
  - 使用 TOC（書籤）自動判定 Markdown 標題層級
  - 支援圖片輸出為檔案並在 Markdown 中以相對路徑引用
  - 表格偵測策略可調（lines_strict / lines / none）
  - 可指定頁範圍（1-based，支援逗號與區間），未指定則處理全檔
  - 支援每頁分塊（page_chunks）與進度列（show_progress）

### 快速開始（CLI）
顯示參數：

```powershell
uv run src\pdf_to_markdown.py --help
```

範例 1：全檔轉換（輸出圖片、使用 TOC 標題、每頁分塊、顯示進度）

```powershell
uv run src\pdf_to_markdown.py -i "C:\path\input.pdf" -o .\out.md --write-images --image-dir .\images --use-toc --page-chunks --show-progress
```

範例 2：指定頁範圍（1-based，支援逗號與區間）

```powershell
uv run src\pdf_to_markdown.py -i "C:\path\input.pdf" -o .\out.md --pages "1-5,8,10-12" --write-images --image-dir .\images --use-toc --page-chunks --show-progress
```

### 參數說明（節錄）
- -i, --input：輸入 PDF 檔（必填）
- -o, --output：輸出 Markdown 檔（必填）
- --pages：頁範圍（1-based，如 "1-5,8,10-12"）；未提供則處理全部
- --write-images：輸出圖片檔（預設開啟；搭配 --image-dir）
- --image-dir：圖片輸出目錄（預設為輸出檔同層 images 子目錄）
- --use-toc：使用 TOC 判定標題層級（預設開啟）
- --table-strategy：表格偵測策略（預設 lines_strict，可選 lines 或 none）
- --page-chunks：每頁分塊輸出（預設開啟；輸出含 `<!-- page: N -->` 註解）
- --show-progress：顯示處理進度列（預設開啟）

### 輸出行為與注意事項
- page_chunks 啟用時，Markdown 中會以 `<!-- page: N -->`（N 為 1-based）標示每頁界線。
- 啟用 --write-images 時，會將頁面中符合大小門檻的圖片輸出到 --image-dir 指定資料夾，並在 Markdown 插入相對路徑引用。
- 表格以 Markdown 表格輸出（受 --table-strategy 影響）。
- 掃描型 PDF（圖片為主）若文字無法抽取，需搭配 OCR（例如 Tesseract）；本工具目前未內建 OCR 流程，可依需求擴充。
