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
> 简单翻译使用 `gemini-2.5-flash-preview-04-17` 可设定 `thinking_budget=0` 关闭深度思考模式。

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

## 📄 PDF → Markdown 转换工具

以 PyMuPDF + PyMuPDF4LLM 打造的 PDF → Markdown 转换 CLI（src/pdf_to_markdown.py）。

- 特点
  - 使用 TOC（书签）自动判定 Markdown 标题层级
  - 支持图片输出为文件并在 Markdown 中以相对路径引用
  - 表格侦测策略可调（lines_strict / lines / none）
  - 可指定页范围（1-based，支持逗号与区间），未指定则处理全档
  - 支持每页分块（page_chunks）与进度条（show_progress）

### 快速开始（CLI）
显示参数：

```powershell
uv run src\pdf_to_markdown.py --help
```

示例 1：全档转换（输出图片、使用 TOC 标题、每页分块、显示进度）

```powershell
uv run src\pdf_to_markdown.py -i "C:\path\input.pdf" -o .\out.md --write-images --image-dir .\images --use-toc --page-chunks --show-progress
```

示例 2：指定页范围（1-based，支持逗号与区间）

```powershell
uv run src\pdf_to_markdown.py -i "C:\path\input.pdf" -o .\out.md --pages "1-5,8,10-12" --write-images --image-dir .\images --use-toc --page-chunks --show-progress
```

### 参数说明（节选）
- -i, --input：输入 PDF 文件（必填）
- -o, --output：输出 Markdown 文件（必填）
- --pages：页范围（1-based，如 "1-5,8,10-12"）；未提供则处理全部
- --write-images：输出图片文件（默认开启；搭配 --image-dir）
- --image-dir：图片输出目录（默认为输出文件同层 images 子目录）
- --use-toc：使用 TOC 判定标题层级（默认开启）
- --table-strategy：表格侦测策略（默认 lines_strict，可选 lines 或 none）
- --page-chunks：每页分块输出（默认开启；输出含 `<!-- page: N -->` 注释）
- --show-progress：显示处理进度条（默认开启）

### 输出行为与注意事项
- page_chunks 启用时，Markdown 中会以 `<!-- page: N -->`（N 为 1-based）标示每页界线。
- 启用 --write-images 时，会将页面中符合大小门槛的图片输出到 --image-dir 指定文件夹，并在 Markdown 插入相对路径引用。
- 表格以 Markdown 表格输出（受 --table-strategy 影响）。
- 扫描型 PDF（图片为主）若文字无法抽取，需搭配 OCR（例如 Tesseract）；本工具目前未内建 OCR 流程，可依需求扩充。
