# 🧪 gemini-test

This project is a playground for exploring the capabilities of the Google Gemini API.

## 🌐 Available Languages

[![English](https://img.shields.io/badge/English-Click-yellow)](README_en.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-Click-orange)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-Click-green)](README_zh-CN.md)

## 🔧 Installation

It's recommended to use `uv` for managing the Python environment and dependencies.

1.  🔑 **Obtain a Google Gemini API Key:**
    Head over to [Google AI Studio](https://aistudio.google.com/apikey) to create your API key.

2.  📄 **Set up Environment Variables:**
    Duplicate the `.env.tpl` file and rename it to `.env`:
    ```bash
    copy .env.tpl .env
    ```
    Then, edit the `.env` file and paste your API key into the `GOOGLE_API_KEY` field.

3.  🛠️ **Install uv:**
    *   **Recommended (Cross-Platform):** Follow the installation instructions on the [uv official documentation](https://github.com/astral-sh/uv#installation).
    *   **Windows (Using Chocolatey):**
        ```bash
        choco install -y uv
        ```

4.  📦 **Sync Dependencies:**
    Run the following command in the project root directory. `uv` will read `pyproject.toml` (or `requirements.txt`) and install the necessary packages:
    ```bash
    uv sync
    ```

## 🚀 Usage

### 🌍 Translate `README.md`

Use the following command to translate `README.md` into multiple languages using the Google Gemini API:

```bash
uv run src/i18n_readme.py
```

> [!NOTE]
> The current model being used is `gemini-2.5-flash-preview-04-17`. Initial testing suggests that while the translation speed is slightly slower compared to `2.0 Flash`, the model's reasoning capabilities and its status as the latest version, combined with the relatively small size of the `README.md` file, make it a suitable choice for initial testing and development.

---

### 🌍 Translate `.properties` Files

This feature allows you to translate `.properties` files into multiple languages (e.g., English `en`, Simplified Chinese `zh-CN`) and generate corresponding output files (e.g., `test_en.properties`, `test_zh-CN.properties`).

The command format is as follows:

```bash
uv run src/i18n_props.py filename [--unicode] [--output-dir DIR] [--lang LANG1,LANG2,...]
```

Example: To translate `test.properties` into `English` and `without using Unicode encoding`:

```bash
uv run src/i18n_props.py test --lang en
```

> [!NOTE]
> `.properties` files often contain a large amount of text. It is recommended to use the `gemini-2.0-flash` model to improve translation efficiency and stability.
