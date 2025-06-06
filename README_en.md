# 🧪 gemini-test

This project is designed to test the functionalities of the Google Gemini API.

## 🌐 Available Languages

[![English](https://img.shields.io/badge/English-Click-yellow)](README_en.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-Click-orange)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-Click-green)](README_zh-CN.md)

## 🔧 Installation

It is recommended to use `uv` for managing your Python environment and dependencies.

1.  🔑 **Obtain Google Gemini API Key:**
    Go to [Google AI Studio](https://aistudio.google.com/apikey) to create your API key.

2.  📄 **Set Environment Variables:**
    Copy the `.env.tpl` file and rename it to `.env`:
    ```bash
    copy .env.tpl .env
    ```
    Then, edit the `.env` file and fill in your API key in the `GOOGLE_API_KEY` field.

3.  🛠️ **Install uv:**
    *   **Recommended (Cross-platform):** Please refer to the [uv official documentation](https://github.com/astral-sh/uv#installation) for installation.
    *   **Windows (using Chocolatey):**
        ```bash
        choco install -y uv
        ```

4.  📦 **Sync Dependencies:**
    Run the following command in the project root directory. `uv` will read `pyproject.toml` (or `requirements.txt`) and install the required packages:
    ```bash
    uv sync
    ```

## 🚀 Usage

### 🌍 Translate Text Files

This feature allows you to translate text files into multiple languages (e.g., English `en`, Simplified Chinese `zh-CN`) and generate corresponding language-specific output files (e.g., `README_en.md`, `README_zh-CN.md`).

> [!NOTE]  
> Currently, the translation is done by reading the entire file at once, so there might be issues if the file contains too much text!

The command format is as follows:

```bash
uv run src/i18n_tool.py --name <filename> [--lang <language1,language2,...>]
```

Example:

```bash
uv run src/i18n_tool.py --name README.md --lang en
```

> [!NOTE]  
> The current model used is `gemini-2.5-flash-preview-04-17`. Preliminary tests show that while this model is slightly slower than `2.0 Flash` for translation, considering its reasoning capabilities and being the latest version, plus the `README.md` file not being large, the translation time won't be too long. Therefore, this model was chosen for initial testing and development.  
> For simple translations using `gemini-2.5-flash-preview-04-17`, you can set `thinking_budget=0` to disable deep thinking mode.

---

### 🌍 Translate `.properties` Files

This feature allows you to translate `.properties` files into multiple languages (e.g., English `en`, Simplified Chinese `zh-CN`) and generate corresponding language-specific output files (e.g., `test_en.properties`, `test_zh-CN.properties`).

The command format is as follows:

```bash
uv run src/i18n_props.py --name <filename> [--unicode] [--output-dir DIR] [--lang LANG1,LANG2,...]
```

Example: To translate `test.properties` to `English`, and `without using Unicode encoding`:

```bash
uv run src/i18n_props.py --name test --lang en
```

> [!NOTE]
> `.properties` files often contain a large amount of text content. It is recommended to use the `gemini-2.0-flash` model to improve translation efficiency and stability.