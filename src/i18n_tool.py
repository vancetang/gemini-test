# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "google-genai",
#     "dotenv",
#     "typing",
# ]
# ///
import os
import pathlib
import argparse
import logging
from typing import List
from dotenv import load_dotenv
from google import genai

# 設定日誌格式，包含時間戳記、級別和訊息
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)
# 限制 Google API 的日誌輸出
logging.getLogger("google_genai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# 預設配置，集中管理程式參數
CONFIG = {
    # 檔案讀寫的編碼格式
    "file_encoding": "utf-8",
    # 預設翻譯目標語言
    "languages": ["en", "zh-CN"],
    # 預設模型
    "gemini_model": os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
}

def setup_environment() -> str:
    """設置環境變數和檔案路徑"""
    load_dotenv()
    
    # 檢查 Google API 金鑰
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise EnvironmentError("找不到 GOOGLE_API_KEY 環境變數")
    
    return google_api_key

def read_input_file(file_path: pathlib.Path) -> str:
    """讀取輸入檔案內容"""
    try:
        with open(file_path, "r", encoding=CONFIG["file_encoding"]) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"輸入檔案不存在：{file_path}")
    except Exception as e:
        raise Exception(f"讀取輸入檔案時發生錯誤：{e}")

def translate_content(client: genai.Client, model: str, content: str, language: str) -> str:
    """將內容翻譯為目標語系"""
    prompt = f"""
    將以下文字翻譯為 {language} 語系，保留 URL 不變。
    根據目標語系的文化和用語規範調整描述，確保翻譯自然。
    僅返回翻譯後的內容，不包含其他文字：
    """
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=[prompt, content],
            config=genai.types.GenerateContentConfig(
                temperature=0.3,  # 控制輸出隨機性，0.5 為平衡值
                # 禁用 Thinking Mode(thinking budget)為 0，表示不進行思考
                # 並不是每個模型都有支援 thinking_config
                thinking_config=genai.types.ThinkingConfig(thinking_budget=0)
            ),
        )
        return response.text
    except Exception as e:
        raise Exception(f"翻譯為 {language} 時發生錯誤：{e}")

def write_output_file(content: str, output_path: pathlib.Path) -> None:
    """將翻譯內容寫入輸出檔案"""
    try:
        with open(output_path, "w", encoding=CONFIG["file_encoding"]) as outfile:
            outfile.write(content)
        logger.info("翻譯內容已儲存至 %s", output_path)
    except Exception as e:
        raise Exception(f"寫入輸出檔案時發生錯誤：{e}")

def parse_arguments() -> argparse.Namespace:
    """解析命令列參數"""
    parser = argparse.ArgumentParser(
        description="將檔案翻譯為多種語系",
        usage="%(prog)s [options] --name <filename> [--lang <language1,language2,...>]",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="輸入檔案名稱（例如 README.md）"
    )
    parser.add_argument(
        "--lang",
        default=",".join(CONFIG["languages"]),
        help="以逗號分隔的目標語言清單，例如：en,zh-CN（預設：en,zh-CN）",
    )
    return parser.parse_args()

def main():
    """主程式：協調翻譯流程"""
    try:
        # 解析命令列參數
        args = parse_arguments()
        target_languages = args.lang.split(",")
        
        # 設置環境
        google_api_key = setup_environment()
        
        # 將輸入路徑轉為 pathlib.Path 物件，並解析為絕對路徑
        input_path = pathlib.Path(args.name).resolve()
        if not input_path.is_file():
            raise FileNotFoundError(f"輸入檔案不存在：{input_path}")
        
        # 輸出檔案將生成在輸入檔案的同一目錄下
        input_dir = input_path.parent
        
        logger.info("*** 輸入檔案：%s", input_path)
        logger.info("*** 使用模型：%s", CONFIG["gemini_model"])
        logger.info("*** 輸出檔案編碼：%s", CONFIG["file_encoding"])
        logger.info("*** 目標語言清單：%s", ", ".join(target_languages))
        logger.info("")
        
        # 初始化 Gemini 客戶端
        client = genai.Client(api_key=google_api_key)
        
        # 讀取輸入檔案
        content = read_input_file(input_path)
        
        # 處理翻譯
        for lang in target_languages:
            logger.info("--- 開始翻譯為 %s ---", lang) 
            
            # 執行翻譯
            translated_content = translate_content(client, CONFIG["gemini_model"], content, lang)
            
            # 生成輸出檔案名稱
            output_filename = f"{input_path.stem}_{lang}{input_path.suffix}"
            output_path = input_dir / output_filename
            
            # 寫入翻譯結果
            write_output_file(translated_content, output_path)
            
        logger.info("")
        logger.info("--- 所有翻譯任務已完成 ---")
        
    except Exception as e:
        logger.error("錯誤：%s", e)
        exit(1)

if __name__ == "__main__":
    main()