# 🧪 gemini-test

此项目用于测试 Google Gemini API 的功能。

## 🌐 可用语言

[![English](https://img.shields.io/badge/English-Click-yellow)](README_en.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-Click-orange)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-Click-green)](README_zh-CN.md)

## 🔧 安装

建议使用 `uv` 来管理 Python 环境与依赖包。

1.  🔑 **获取 Google Gemini API 密钥:**
    前往 [Google AI Studio](https://aistudio.google.com/apikey) 创建您的 API 密钥。

2.  📄 **设置环境变量:**
    复制 `.env.tpl` 文件并重命名为 `.env`：
    ```bash
    copy .env.tpl .env
    ```
    接着，编辑 `.env` 文件，将您获取的 API 密钥填入 `GOOGLE_API_KEY` 字段。

3.  🛠️ **安装 uv:**
    *   **推荐 (跨平台):** 请参考 [uv 官方文档](https://github.com/astral-sh/uv#installation) 进行安装。
    *   **Windows (使用 Chocolatey):**
        ```bash
        choco install -y uv
        ```

4.  📦 **同步依赖包:**
    在项目根目录执行以下指令，`uv` 会读取 `pyproject.toml` (或 `requirements.txt`) 并安装所需的包：
    ```bash
    uv sync
    ```

## 🚀 使用方式

### 🌍 翻译文本文件

此功能可将文本文件翻译为多种语言（如英文 `en`、简体中文 `zh-CN`），并生成对应语系的输出文件（例如：`README_en.md`、`README_zh-CN.md`）。

> [!NOTE]  
> 目前是采用一次性读档翻译，所以如果文件文字太多可能会有问题!!。

执行指令格式如下：

```bash
uv run src/i18n_tool.py --name <filename> [--lang <language1,language2,...>]
```

示例：

```bash
uv run src/i18n_tool.py --name README.md --lang en
```

> [!NOTE]  
> 目前使用的模型是 `gemini-2.5-flash-preview-04-17`，初步测试显示，此模型虽然翻译速度相较于 `2.0 Flash` 稍慢，但考量其具备推理功能且为最新版本，加上 `README.md` 文件不大，翻译时间也不会太长，因此选择此模型进行初步测试与开发。

---

### 🌍 翻译 `.properties` 文件

此功能可将 `.properties` 文件翻译为多种语言（如英文 `en`、简体中文 `zh-CN`），并生成对应语系的输出文件（例如：`test_en.properties`、`test_zh-CN.properties`）。

执行指令格式如下：

```bash
uv run src/i18n_props.py --name <filename> [--unicode] [--output-dir DIR] [--lang LANG1,LANG2,...]
```

示例：若要翻译 `test.properties` 为 `英文`，且 `不使用 Unicode 编码`：

```bash
uv run src/i18n_props.py --name test --lang en
```

> [!NOTE]
> `.properties` 文件常包含大量文字内容，建议选用 `gemini-2.0-flash` 模型以提升翻译效率与稳定性。
