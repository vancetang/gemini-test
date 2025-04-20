# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "google-genai",
#     "load-dotenv",
# ]
# ///
import os
import pathlib
import json
import argparse
import logging
from typing import List, Tuple, Dict
from dotenv import load_dotenv
from google import genai
from utils.unicode import unescape_unicode, escape_non_ascii

# 設定日誌格式，包含時間戳記和訊息級別
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)
# 限制 Google API 的日誌輸出
logging.getLogger("google_genai.models").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# 預設配置，集中管理程式參數
CONFIG = {
    # 檔案讀寫的編碼格式
    "file_encoding": "utf-8",
    # 每次 API 呼叫的翻譯行數
    "batch_size": 100,
    # 預設翻譯目標語言
    "languages": ["en", "zh-CN"],
    # 預設模型
    "gemini_model": os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
}

# 批量翻譯的 Prompt 模板，指導 API 進行翻譯
BATCH_TRANSLATION_PROMPT = """
請將以下 JSON 物件中的值翻譯成 {language} 語系。根據目標語系的語言習慣調整描述，確保翻譯內容自然且符合當地文化與用語規範。
請以 JSON 格式返回翻譯結果，格式為一個物件，其中 key 為原文的索引（字串），value 為翻譯後的內容。
例如：
輸入:
{{
  "0": "Hello",
  "1": "World"
}}
輸出:
{{
  "0": "你好",
  "1": "世界"
}}

以下是要翻譯的 JSON 物件：
"""

def setup_arguments() -> argparse.Namespace:
    """設定並解析命令列參數"""
    parser = argparse.ArgumentParser(
        description="將 .properties 檔案翻譯為指定語言的 .properties 檔案",
        usage="%(prog)s filename [--unicode] [--output-dir DIR] [--lang LANG1,LANG2,...]",
    )
    parser.add_argument("filename", help="要翻譯的 .properties 檔案名稱（不含 .properties 副檔名）")
    parser.add_argument(
        "--unicode",
        action="store_true",
        help="是否將輸出檔案中的非 ASCII 字元轉為 Unicode 編碼（預設：否）",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="翻譯後檔案的儲存目錄（預設：專案根目錄）",
    )
    parser.add_argument(
        "--lang",
        default=",".join(CONFIG["languages"]),
        help="以逗號分隔的目標語言清單，例如：en,zh-CN（預設：en,zh-CN）",
    )
    return parser.parse_args()

def initialize_environment() -> tuple[pathlib.Path, pathlib.Path, genai.Client]:
    """初始化環境變數、檔案路徑和 API 客戶端"""
    # 載入 .env 檔案中的環境變數
    load_dotenv()
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        logger.error("未找到 GOOGLE_API_KEY 環境變數，請檢查 .env 檔案")
        raise ValueError("缺少 GOOGLE_API_KEY")

    # 取得腳本所在目錄和專案根目錄
    script_dir = pathlib.Path(__file__).parent
    project_root = script_dir.parent
    client = genai.Client(api_key=google_api_key)
    return script_dir, project_root, client

def read_properties_file(file_path: pathlib.Path) -> List[str]:
    """讀取 .properties 檔案，並將 Unicode 編碼解碼為可讀字元"""
    try:
        with open(file_path, "r", encoding=CONFIG["file_encoding"]) as f:
            # 逐行讀取並解碼 Unicode 字元
            return [unescape_unicode(line) for line in f.readlines()]
    except FileNotFoundError:
        logger.error("輸入檔案不存在：%s", file_path)
        raise
    except Exception as e:
        logger.error("讀取檔案 %s 時發生錯誤：%s", file_path, e)
        raise

def parse_properties_lines(lines: List[str]) -> Tuple[List[str], List[Tuple[int, str, str]]]:
    """解析 .properties 檔案，提取待翻譯的鍵值對"""
    lines_to_translate = []
    original_lines = [line.rstrip("\n") for line in lines]
    
    # 遍歷每一行，識別有效的鍵值對
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        # 忽略空行或註解行
        if not stripped_line or stripped_line.startswith("#"):
            continue
        # 處理 key=value 格式
        if "=" in stripped_line:
            key, value = stripped_line.split("=", 1)
            key, value = key.strip(), value.strip()
            if value:
                lines_to_translate.append((i, key, value))
    
    return original_lines, lines_to_translate

def translate_batch(
    client: genai.Client,
    values: Dict[str, str],
    language: str,
    model: str = CONFIG["gemini_model"],
) -> Dict[str, str]:
    """呼叫 Gemini API 進行批量翻譯"""
    try:
        # 構造翻譯提示並附加 JSON 資料
        prompt = BATCH_TRANSLATION_PROMPT.format(language=language)
        response = client.models.generate_content(
            model=model,
            contents=[prompt, json.dumps(values, ensure_ascii=False)],
            config=genai.types.GenerateContentConfig(temperature=0.3),
        )
        # 處理 API 回應，移除可能的 Markdown 格式
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[len("```json") :].rstrip("```").strip()
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        logger.error("無法解析 API 回應的 JSON 格式：%s", e)
        logger.debug("API 回應內容：%s", response.text)
    except Exception as e:
        logger.error("呼叫翻譯 API 時發生錯誤：%s", e)
        return {}

def translate_properties(
    client: genai.Client,
    lines_to_translate: List[Tuple[int, str, str]],
    language: str,
) -> Dict[int, str]:
    """對所有待翻譯行進行翻譯，分批處理以避免 API 限制"""
    translated_results = {}
    batch_size = CONFIG["batch_size"]
    
    # 分批處理待翻譯行
    for i in range(0, len(lines_to_translate), batch_size):
        batch_info = lines_to_translate[i : i + batch_size]
        batch_values = {str(index): value for index, _, value in batch_info}
        logger.info("處理第 %d 批次（共 %d 筆資料）", i // batch_size + 1, len(batch_values))
        
        # 執行批量翻譯並儲存結果
        translated_batch = translate_batch(client, batch_values, language)
        for idx_str, translated_value in translated_batch.items():
            translated_results[int(idx_str)] = translated_value.strip()
    
    return translated_results

def write_output_file(
    output_file: pathlib.Path,
    original_lines: List[str],
    translated_results: Dict[int, str],
    lines_to_translate: List[Tuple[int, str, str]],
    use_unicode: bool,
) -> None:
    """將翻譯結果寫入輸出檔案，根據需要轉換為 Unicode 編碼"""
    output_lines = original_lines.copy()
    line_info_map = {index: (key, value) for index, key, value in lines_to_translate}
    
    # 將翻譯結果應用到對應行
    for idx, translated_value in translated_results.items():
        if idx in line_info_map:
            key, _ = line_info_map[idx]
            full_line = f"{key}={translated_value}"
             # 根據參數決定是否轉換為 Unicode 編碼
            if use_unicode:
                full_line = escape_non_ascii(full_line)
            output_lines[idx] = full_line
    
    try:
        # 寫入輸出檔案
        with open(output_file, "w", encoding=CONFIG["file_encoding"]) as f:
            f.write("\n".join(output_lines))
        logger.info("翻譯檔案已成功儲存至：%s", output_file)
    except Exception as e:
        logger.error("寫入檔案 %s 時發生錯誤：%s", output_file, e)
        raise

def main():
    """主函數"""
    args = setup_arguments()
    filename_prefix = args.filename
    use_unicode = args.unicode
    output_dir = pathlib.Path(args.output_dir) if args.output_dir else None
    target_languages = args.lang.split(",")

    try:
        # 初始化環境和檔案路徑
        _, project_root, client = initialize_environment()
        input_file = project_root / f"{filename_prefix}.properties"
        output_dir = output_dir or project_root
        
        # 記錄程式執行資訊
        logger.info("*** 專案根目錄：%s", project_root)
        logger.info("*** 輸入檔案路徑：%s", input_file)
        logger.info("*** 輸出檔案編碼：%s", CONFIG["file_encoding"])
        logger.info("*** 是否使用 Unicode 編碼：%s", use_unicode)
        logger.info("*** 目標語言清單：%s", ", ".join(target_languages))
        logger.info("")

        # 讀取並解析輸入檔案
        lines = read_properties_file(input_file)
        original_lines, lines_to_translate = parse_properties_lines(lines)

        # 對每種語言進行翻譯
        for language in target_languages:
            output_file = output_dir / f"{filename_prefix}_{language}.properties"
            logger.info("--- 開始翻譯為 %s ---", language)

            # 執行翻譯並寫入結果
            translated_results = translate_properties(client, lines_to_translate, language)
            write_output_file(
                output_file,
                original_lines,
                translated_results,
                lines_to_translate,
                use_unicode,
            )
        
        logger.info("")
        logger.info("--- 所有翻譯任務已完成 ---")
    
    except Exception as e:
        logger.error("程式執行過程中發生錯誤：%s", e)
        exit(1)

if __name__ == "__main__":
    main()