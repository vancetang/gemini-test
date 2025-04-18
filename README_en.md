# 🧪 gemini-test

This project is used to test the functionalities of the Google Gemini API.

## 🌐 Available Languages

[![English](https://img.shields.io/badge/English-Click-yellow)](README_en.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-Click-orange)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-Click-green)](README_zh-CN.md)

## 🔧 Installation

It is recommended to use `uv` for managing the Python environment and dependencies.

1.  🔑 **Get Your Google Gemini API Key:**
    Go to [Google AI Studio](https://aistudio.google.com/apikey) to create your API key.

2.  📄 **Configure Environment Variables:**
    Copy the `.env.tpl` file and rename it to `.env`:
    ```bash
    copy .env.tpl .env
    ```
    Then, edit the `.env` file and fill in your obtained API key in the `GOOGLE_API_KEY` field.

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

### 🌍 Gemini Translate README.md
```python
uv run src/translate.py
```

> **📝 Note**
> The current model used is gemini-2.5-flash-preview-04-17. For small files, the speed performance is not significantly different from other models.

### 🌍 Gemini Translate Specific Properties File
```python
uv run src/transprop.py <properties_file without extension>
```
For example: If the file is `test.properties`
```bash
uv run src/transprop.py test
```

> **⚠️ Warning**
> Since properties files usually contain a large amount of data, it is recommended to use the gemini-2.0-flash model to ensure efficient processing.
