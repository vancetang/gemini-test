# 🧪 gemini-test

This project is for testing the capabilities of the Google Gemini API.

## 🌐 Available Languages

[![English](https://img.shields.io/badge/English-Click-yellow)](README_en.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-Click-orange)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-Click-green)](README_zh-CN.md)

## 🔧 Installation

It is recommended to use `uv` to manage the Python environment and dependencies.

1.  🔑 **Obtain a Google Gemini API Key:**
    Go to [Google AI Studio](https://aistudio.google.com/apikey) to create your API key.

2.  📄 **Set up Environment Variables:**
    Copy the `.env.tpl` file and rename it to `.env`:
    ```bash
    copy .env.tpl .env
    ```
    Then, edit the `.env` file and fill in the `GOOGLE_API_KEY` field with your API key.

3.  🛠️ **Install uv:**
    *   **Recommended (Cross-Platform):** Refer to the [uv official documentation](https://github.com/astral-sh/uv#installation) for installation instructions.
    *   **Windows (using Chocolatey):**
        ```bash
        choco install -y uv
        ```

4.  📦 **Synchronize Dependencies:**
    Run the following command in the project root directory. `uv` will read `pyproject.toml` (or `requirements.txt`) and install the necessary packages:
    ```bash
    uv sync
    ```

## 🚀 Usage

### 🌍 Translate Text Files

This feature can translate text files into multiple languages (such as English `en`, Simplified Chinese `zh-CN`), and generate corresponding language-specific output files (e.g., `README_en.md`, `README_zh-CN.md`).

> [!NOTE]
> Currently, the file is read and translated all at once, so there may be issues if the file contains too much text!

The command format is as follows:

```bash
uv run src/i18n_tool.py --name <filename> [--lang <language1,language2,...>]
```

Example:

```bash
uv run src/i18n_tool.py --name README.md --lang en
```

> [!NOTE]
> The current model being used is `gemini-2.5-flash-preview-04-17`. Initial testing shows that although this model is slightly slower than `2.0 Flash` in terms of translation speed, it has reasoning capabilities and is the latest version. Considering that the `README.md` file is not large, the translation time will not be too long. Therefore, this model was chosen for initial testing and development.
> For simple translations using `gemini-2.5-flash-preview-04-17`, you can set `thinking_budget=0` to turn off the deep thinking mode.

---

### 🌍 Translate `.properties` Files

This feature can translate `.properties` files into multiple languages (such as English `en`, Simplified Chinese `zh-CN`), and generate corresponding language-specific output files (e.g., `test_en.properties`, `test_zh-CN.properties`).

The command format is as follows:

```bash
uv run src/i18n_props.py --name <filename> [--unicode] [--output-dir DIR] [--lang LANG1,LANG2,...]
```

Example: To translate `test.properties` to `English` and `without Unicode encoding`:

```bash
uv run src/i18n_props.py --name test --lang en
```

> [!NOTE]
> `.properties` files often contain a large amount of text content. It is recommended to use the `gemini-2.0-flash` model to improve translation efficiency and stability.

## 📄 PDF → Markdown Conversion Tool

A PDF → Markdown conversion CLI (src/pdf_to_markdown.py) built with PyMuPDF + PyMuPDF4LLM.

- Features
  - Uses TOC (bookmarks) to automatically determine Markdown heading levels.
  - Supports exporting images as files and referencing them in Markdown with relative paths.
  - Adjustable table detection strategy (lines_strict / lines / none).
  - Can specify page ranges (1-based, supports commas and ranges), otherwise processes the entire file.
  - Supports per-page chunking (page_chunks) and progress bar (show_progress).

### Quick Start (CLI)
Display parameters:

```powershell
uv run src\pdf_to_markdown.py --help
```

Example 1: Full file conversion (output images, use TOC headings, per-page chunking, show progress)

```powershell
uv run src\pdf_to_markdown.py -i "C:\path\input.pdf" -o .\out.md --write-images --image-dir .\images --use-toc --page-chunks --show-progress
```

Example 2: Specify page range (1-based, supports commas and ranges)

```powershell
uv run src\pdf_to_markdown.py -i "C:\path\input.pdf" -o .\out.md --pages "1-5,8,10-12" --write-images --image-dir .\images --use-toc --page-chunks --show-progress
```

### Parameter Description (Excerpt)
- -i, --input: Input PDF file (required)
- -o, --output: Output Markdown file (required)
- --pages: Page range (1-based, e.g., "1-5,8,10-12"); if not provided, processes the entire file
- --write-images: Output image files (enabled by default; requires --image-dir)
- --image-dir: Image output directory (defaults to the images subdirectory in the same directory as the output file)
- --use-toc: Use TOC to determine heading levels (enabled by default)
- --table-strategy: Table detection strategy (defaults to lines_strict, can be lines or none)
- --page-chunks: Output per-page chunks (enabled by default; outputs `<!-- page: N -->` comments)
- --show-progress: Show processing progress bar (enabled by default)

### Output Behavior and Notes
- When page_chunks is enabled, Markdown will mark each page boundary with `<!-- page: N -->` (N is 1-based).
- When --write-images is enabled, images that meet the size threshold will be output to the folder specified by --image-dir, and relative path references will be inserted into the Markdown.
- Tables are output as Markdown tables (affected by --table-strategy).
- If text cannot be extracted from scanned PDFs (image-based), OCR (e.g., Tesseract) is required; this tool does not currently have a built-in OCR process and can be expanded as needed.
