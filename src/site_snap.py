import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import zipfile
from datetime import datetime

# 設置目標 URL
base_url = "https://deepwiki.com/vancetang/demo/"
output_dir = "deepwiki_pages"
zip_filename = f"deepwiki_pages_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"

# 創建儲存 HTML 的資料夾
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 儲存已訪問的 URL 以避免重複
visited_urls = set()

def sanitize_filename(url):
    """將 URL 轉換為安全的檔案名稱"""
    parsed = urlparse(url)
    path = parsed.path.replace("/", "_").strip("_")
    if not path:
        path = "index"
    return f"{path}.html"

def save_page(url, content):
    """儲存網頁內容為 HTML 檔案"""
    filename = sanitize_filename(url)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved: {filepath}")

def crawl_page(url):
    """爬取網頁並儲存，遞迴爬取所有連結"""
    if url in visited_urls or not url.startswith(base_url):
        return
    
    visited_urls.add(url)
    print(f"Crawling: {url}")
    
    try:
        # 發送請求
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 儲存當前頁面
        save_page(url, str(soup.prettify()))
        
        # 尋找所有連結
        for link in soup.find_all("a", href=True):
            href = link["href"]
            absolute_url = urljoin(base_url, href)
            
            # 只爬取同一域名下的連結
            if absolute_url.startswith(base_url):
                crawl_page(absolute_url)
                
    except requests.RequestException as e:
        print(f"Error crawling {url}: {e}")

def create_zip():
    """將所有 HTML 檔案壓縮為 ZIP"""
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zf.write(file_path, os.path.relpath(file_path, output_dir))
    print(f"Created ZIP: {zip_filename}")

def main():
    # 開始爬取
    crawl_page(base_url)
    
    # 壓縮檔案
    create_zip()
    
    # 可選：刪除臨時資料夾
    # import shutil
    # shutil.rmtree(output_dir)
    
    print(f"Done! Download the ZIP file: {zip_filename}")

if __name__ == "__main__":
    main()