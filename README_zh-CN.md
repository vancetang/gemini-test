# 🧪 gemini-test

本项目用于测试 Google Gemini API 的功能。

## 🌐 可用语言

[![English](https://img.shields.io/badge/English-Click-yellow)](README_en.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-Click-orange)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-Click-green)](README_zh-CN.md)

## 🔧 安装

推荐使用 `uv` 来管理 Python 环境和依赖包。

1.  🔑 **获取 Google Gemini API 密钥:**
    前往 [Google AI Studio](https://aistudio.google.com/apikey) 创建您的 API 密钥。

2.  📄 **设置环境变量:**
    复制 `.env.tpl` 文件并重命名为 `.env`：
    ```bash
    copy .env.tpl .env
    ```
    然后，编辑 `.env` 文件，将您获取的 API 密钥填入 `GOOGLE_API_KEY` 字段。

3.  🛠️ **安装 uv:**
    *   **推荐 (跨平台):** 请参考 [uv 官方文档](https://github.com/astral-sh/uv#installation) 进行安装。
    *   **Windows (使用 Chocolatey):**
        ```bash
        choco install -y uv
        ```

4.  📦 **同步依赖包:**
    在项目根目录执行以下命令，`uv` 会读取 `pyproject.toml` (或 `requirements.txt`) 并安装所需的包：
    ```bash
    uv sync
    ```

## 🚀 使用方式

### 🌍 翻译 `README.md`

使用以下命令通过 Google Gemini API 对 `README.md` 进行多语言翻译：

```bash
uv run src/i18n_readme.py
```

> [!NOTE]  
> 目前使用的模型为 `gemini-2.5-flash-preview-04-17`，适用于小型文档。此模型在翻译速度与质量之间取得良好平衡，适合进行初步测试与开发用途。

---

### 🌍 翻译 `.properties` 文件

此功能可以将 `.properties` 文件翻译为多种语言（如英文 `en`、简体中文 `zh-CN`），并生成对应语系的输出文件（例如：`test_en.properties`、`test_zh-CN.properties`）。

执行命令格式如下：

```bash
uv run src/i18n_props.py filename [--unicode] [--output-dir DIR] [--lang LANG1,LANG2,...]
```

示例：若要翻译 `test.properties` 为 `英文`，且 `不使用 Unicode 编码`：

```bash
uv run src/i18n_props.py test --lang en
```

> [!NOTE]
> `.properties` 文件常包含大量文字内容，建议选用 `gemini-2.0-flash` 模型以提升翻译效率与稳定性。
