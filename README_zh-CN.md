# 🧪 gemini-test

此项目用于测试 Google Gemini API 的功能。

## 🌐 可用语言

[![English](https://img.shields.io/badge/English-Click-yellow)](README_en.md)
[![繁體中文](https://img.shields.io/badge/繁體中文-Click-orange)](README.md)
[![简体中文](https://img.shields.io/badge/简体中文-Click-green)](README_zh-CN.md)

## 🔧 安装

建议使用 `uv` 来管理 Python 环境和依赖包。

1.  🔑 **获取 Google Gemini API 密钥:**
    前往 [Google AI Studio](https://aistudio.google.com/apikey) 创建您的 API 密钥。

2.  📄 **配置环境变量:**
    复制 `.env.tpl` 文件并重命名为 `.env`：
    ```bash
    copy .env.tpl .env
    ```
    接着，编辑 `.env` 文件，将您获取的 API 密钥填入 `GOOGLE_API_KEY` 字段。

3.  🛠️ **安装 uv:**
    *   **建议 (跨平台):** 请参考 [uv 官方文档](https://github.com/astral-sh/uv#installation) 进行安装。
    *   **Windows (使用 Chocolatey):**
        ```bash
        choco install -y uv
        ```

4.  📦 **同步依赖包:**
    在项目根目录执行以下指令，`uv` 会读取 `pyproject.toml` (或 `requirements.txt`) 并安装所需的包：
    ```bash
    uv sync
    ```

## 🚀 使用方法

### 🌍 Gemini 翻译 README.md
```python
uv run src/translate.py
```

> **📝 注意**
> 目前使用的模型为 gemini-2.5-flash-preview-04-17，处理小型文件，速度表现与其他模型相差不大。


### 🌍 Gemini 翻译指定 Properties 文件
```python
uv run src/transprop.py <properties_file 不含文件扩展名>
```
例如：文件为 `test.properties`
```bash
uv run src/transprop.py test
```

> **⚠️ 警告**
> 由于 properties 文件通常包含大量数据，建议使用 gemini-2.0-flash 模型以确保高效处理。
