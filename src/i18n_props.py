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
from dotenv import load_dotenv
from google import genai
from utils.unicode import unescape_unicode, escape_non_ascii

# 設置命令列參數解析
parser = argparse.ArgumentParser(
    description="翻譯 .properties 檔案到多種語言", usage="%(prog)s filename [--unicode]"
)
parser.add_argument("filename", help="要翻譯的 .properties 檔案名稱（不含副檔名）")
parser.add_argument(
    "--unicode",
    action="store_true",
    default=False,  # 預設為 False
    help="是否使用 Unicode 編碼（預設為 False）",
)
args = parser.parse_args()

# 從參數取得值
filename_prefix = args.filename
IS_UNICODE = args.unicode

# 載入環境變數
load_dotenv()

# 取得腳本所在的目錄
script_dir = pathlib.Path(__file__).parent
# 取得專案根目錄 (src 的上一層)
project_root = script_dir.parent

# 建立輸入檔案的絕對路徑
input_file_path = project_root / f"{filename_prefix}.properties"
# 建立輸出檔案的目錄 (專案根目錄)
output_dir = project_root

print(f"*** 專案根目錄: {project_root}")
print(f"*** 輸入檔案路徑: {input_file_path}")

# 設定檔案編碼格式
FILE_ENCODING = "utf-8"
print(f"*** 產出檔案編碼格式: {FILE_ENCODING}")
print(f"*** 產出檔案是否轉為Unicode編碼: {IS_UNICODE}")

# 設定 API 金鑰和模型名稱
google_api_key = os.environ.get("GOOGLE_API_KEY")
gemini_model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

print(f"*** 使用的模型: {gemini_model}")

if not google_api_key:
    print(
        "錯誤：找不到 GOOGLE_API_KEY 環境變數。請確定 .env 檔案存在且包含 GOOGLE_API_KEY。"
    )
    exit()

client = genai.Client(api_key=google_api_key)

# 讀取輸入檔案的內容 (逐行讀取)
try:
    with open(input_file_path, "r", encoding="utf-8") as f:
        input_lines = [unescape_unicode(line) for line in f.readlines()]
except FileNotFoundError:
    print(f"錯誤：找不到檔案：{input_file_path}")
    exit()
except Exception as e:
    print(f"讀取 {input_file_path} 時發生錯誤：{e}")
    exit()

# 定義要翻譯的語言
languages = ["en", "zh-CN"]

# 定義批量翻譯的 prompt 模板
# 要求返回 JSON 格式，key 為原始索引(字串)，value 為翻譯後的內容
batch_translation_prompt_template = """
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

# 定義批量大小
BATCH_SIZE = 100

for language in languages:
    # 建立輸出檔案的絕對路徑，使用提供的檔案名稱前綴
    output_filename = output_dir / f"{filename_prefix}_{language}.properties"

    # 清空目標語系檔案
    try:
        with open(output_filename, "w", encoding=FILE_ENCODING) as outfile:
            pass  # 開啟寫入模式並立即關閉，清空檔案內容
        print(f"\n--- 開始翻譯為 {language} ---")
        print(f"已清空檔案：{output_filename}")
    except Exception as e:
        print(f"清空檔案 {output_filename} 時發生錯誤：{e}")
        continue  # 跳過此語言的翻譯

    lines_to_translate_info = []  # 儲存 (index, key, value) 的列表
    original_lines = []  # 儲存所有原始行

    # 遍歷輸入行，識別需要翻譯的行並儲存資訊
    for i, line in enumerate(input_lines):
        original_lines.append(line.rstrip("\n"))  # 儲存原始行內容 (移除換行符)
        stripped_line = line.strip()

        # 忽略空行或註解行
        if not stripped_line or stripped_line.startswith("#"):
            continue

        # 處理 key=value 格式的行
        if "=" in stripped_line:
            key, value = stripped_line.split("=", 1)  # 只在第一個 '=' 處分割
            key = key.strip()
            value = value.strip()

            if value:  # 如果值不為空，則加入待翻譯列表
                lines_to_translate_info.append((i, key, value))

    translated_results = {}  # 儲存翻譯結果 {index: translated_value}

    # 分批處理需要翻譯的行
    for i in range(0, len(lines_to_translate_info), BATCH_SIZE):
        batch_info = lines_to_translate_info[i : i + BATCH_SIZE]
        batch_values_dict = {
            str(index): value for index, key, value in batch_info
        }  # 使用索引作為 key

        if not batch_values_dict:
            continue  # 如果批次為空，跳過

        print(f"  正在處理批次 {i // BATCH_SIZE + 1} (共 {len(batch_info)} 筆)...")

        try:
            # 構造批量翻譯的 prompt
            batch_prompt = batch_translation_prompt_template.format(language=language)

            # 呼叫 Gemini API 進行批量翻譯
            response = client.models.generate_content(
                model=gemini_model,
                # 傳遞 prompt 和 JSON 格式的待翻譯內容
                contents=[
                    batch_prompt,
                    json.dumps(batch_values_dict, ensure_ascii=False),
                ],
                config=genai.types.GenerateContentConfig(
                    temperature=0.3,
                ),
            )

            # 解析 API 返回的 JSON 結果
            response_text = response.text.strip()
            # 嘗試從可能的 markdown 程式碼區塊中提取 JSON
            if response_text.startswith("```json"):
                response_text = response_text[len("```json") :].strip()
                if response_text.endswith("```"):
                    response_text = response_text[: -len("```")].strip()

            batch_translated_values = json.loads(response_text)

            # 將翻譯結果儲存到 translated_results 字典中
            for original_index_str, translated_value in batch_translated_values.items():
                original_index = int(original_index_str)
                # 儲存翻譯結果並移除首尾空白
                translated_results[original_index] = translated_value.strip()

        except json.JSONDecodeError as e:
            print(f"  錯誤：解析 API 返回的 JSON 時發生錯誤：{e}")
            print(f"  API 返回內容：{response.text}")
            # JSON 解析失敗，此批次的翻譯結果將會遺失
        except Exception as e:
            print(f"  呼叫 API 翻譯批次時發生錯誤：{e}")
            # API 呼叫失敗，此批次的翻譯結果將會遺失

    # 構造最終的輸出內容
    output_lines = []
    # 建立索引到 (key, value) 的映射
    line_info_map = {
        index: (key, value) for index, key, value in lines_to_translate_info
    }

    for i, original_line in enumerate(original_lines):
        full_line = original_line

        if i in translated_results:
            if "=" in original_line:
                key, _ = original_line.split("=", 1)
                key = key.strip()
                # 先串接 key=value，再整體進行轉義
                full_line = f"{key}={translated_results[i]}"

        # 根據輸出編碼決定是否進行非 ASCII 字元轉義
        if IS_UNICODE:
            full_line = escape_non_ascii(full_line)

        # 將處理後的行加入輸出列表
        output_lines.append(full_line)

    # 將所有處理後的行寫入輸出檔案
    try:
        with open(output_filename, "w", encoding=FILE_ENCODING) as outfile:
            outfile.write("\n".join(output_lines))

        print(f"翻譯後的內容已成功儲存至 {output_filename}")

    except Exception as e:
        print(f"寫入檔案 {output_filename} 時發生錯誤：{e}")

print("\n--- 翻譯完成 ---")
