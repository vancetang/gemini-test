# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "google-genai",
#     "load-dotenv",
# ]
# ///
import os
import pathlib
from dotenv import load_dotenv
from google import genai

# 載入環境變數
load_dotenv()

# 取得腳本所在的目錄
script_dir = pathlib.Path(__file__).parent
# 取得專案根目錄 (src 的上一層)
project_root = script_dir.parent
# 建立 README.md 的絕對路徑
readme_path = project_root / "README.md"
# 建立輸出檔案的目錄 (專案根目錄)
output_dir = project_root

print(f"*** 專案根目錄: {project_root}")
print(f"*** 輸入檔案路徑: {readme_path}")

# 設定 API 金鑰和模型名稱
google_api_key = os.environ.get("GOOGLE_API_KEY")
gemini_model = os.environ.get(
    "GEMINI_MODEL", "gemini-2.0-flash"
)

print(f"*** 使用的模型: {gemini_model}")

if not google_api_key:
    print("錯誤：找不到 GOOGLE_API_KEY 環境變數。請確定 .env 檔案存在且包含 GOOGLE_API_KEY。")
    exit()

client = genai.Client(api_key=google_api_key)

# 讀取 README.md 檔案內容
try:
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
except FileNotFoundError:
    print("錯誤：找不到 README.md 檔案。")
    exit()
except Exception as e:
    print(f"讀取 README.md 時發生錯誤：{e}")
    exit()

# 定義要翻譯的語言
languages = ["en", "zh-CN"]

for language in languages:
    print(f"\n--- 開始翻譯為 {language} ---")

    # 準備翻譯請求的內容
    prompt = f"""
    請將以下文字翻譯成 {language} 語系，保留原文中的 URL 網址不進行翻譯，
    根據目標語系的語言習慣調整描述，確保翻譯內容自然且符合當地文化與用語規範。
    僅返回翻譯後的內容，不包含開場白、說明或其他多餘文字:
    """
    contents_to_translate = [prompt, readme_content]

    try:
        # 呼叫 Gemini API 進行翻譯
        response = client.models.generate_content(
            model=gemini_model, contents=contents_to_translate,
            config=genai.types.GenerateContentConfig(
                # 設定模型的隨機程度(0-1)，較高的值會使輸出更具變化性，而較低的值(接近 0)會使輸出更具確定性
                temperature=0.5,
                # 並不是每個模型都有支援thinking_config
                # 禁用 Thinking Mode(thinking budget)為 0，表示不進行思考
                # thinking_config=genai.types.ThinkingConfig(thinking_budget=0)
            )
        )

        # 將翻譯後的內容寫入對應的 README 檔案
        translated_text = response.text
        # 在專案根目錄建立輸出檔案
        output_filename = output_dir / f"README_{language}.md"
        with open(output_filename, "w", encoding="utf-8") as outfile:
            outfile.write(translated_text)

        print(f"翻譯後的內容已成功儲存至 {output_filename}")

    except Exception as e:
        print(f"處理過程中發生錯誤：{e}")

print("\n--- 翻譯完成 ---")