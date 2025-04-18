# 🧪 gemini-test

This project is for testing the capabilities of the Google Gemini API.

## 🌐 Available Languages

[![English](https://img.shields.io/badge/English-Click-yellow)](README_en.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-Click-orange)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-Click-green)](README_zh-CN.md)

## 🔧 Installation

It's recommended to use `uv` to manage the Python environment and dependencies.

1.  🔑 **Obtain a Google Gemini API Key:**
    Go to [Google AI Studio](https://aistudio.google.com/apikey) to create your API key.

2.  📄 **Set Environment Variables:**
    Copy the `.env.tpl` file and rename it to `.env`:
    ```bash
    copy .env.tpl .env
    ```
    Then, edit the `.env` file and fill in your API key in the `GOOGLE_API_KEY` field.

3.  🛠️ **Install uv:**
    *   **Recommended (Cross-Platform):** Refer to the [uv official documentation](https://github.com/astral-sh/uv#installation) for installation instructions.
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

### 🌍 Translate `README.md`

Use the following command to translate `README.md` into multiple languages using the Google Gemini API:

```bash
uv run src/i18n_readme.py
```

> **📝 Note:**
> The current model used is `gemini-2.5-flash-preview-04-17`, which is suitable for smaller documents. This model strikes a good balance between translation speed and quality, making it ideal for initial testing and development purposes.

---

### 🌍 Translate `.properties` Files

This feature allows you to translate `.properties` files into multiple languages (such as English `en`, Simplified Chinese `zh-CN`) and generate corresponding language-specific output files (e.g., `test_en.properties`, `test_zh-CN.properties`).

The command format is as follows:

```bash
uv run src/i18n_props.py <filename> [--unicode]
```

Example: To translate `test.properties` without using Unicode encoding:

```bash
uv run src/i18n_props.py test
```

> **⚠️ Recommendation:**
> Since `.properties` files often contain a large amount of text, it is recommended to use the `gemini-2.0-flash` model to improve translation efficiency and stability.
