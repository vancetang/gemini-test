# Python 專案風格指南

本文件旨在規範專案中 Python 程式碼的風格，以提高可讀性、可維護性和一致性。

## General Response Language
* **IMPORTANT:** Please provide all responses, comments, and suggestions exclusively in **Traditional Chinese (繁體中文)**.

## 1. 程式碼格式化

*   **PEP 8:** 嚴格遵守 [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/)。
    *   縮排：使用 4 個空格進行縮排。
    *   行長：每行程式碼不應超過 88 個字元（與 Black 格式化工具預設一致）。
    *   空行：頂層函式和類別定義之間空兩行；類別內部的方法定義之間空一行。
    *   匯入：
        *   匯入應分組，順序為：標準函式庫、相關第三方函式庫、本地應用程式/函式庫。
        *   每組之間空一行。
        *   避免使用 `from module import *`。
*   **自動格式化:** 強烈建議使用 `ruff format` 或 `black` 自動格式化程式碼。

## 2. 命名慣例

*   **變數:** 使用 `snake_case` (小寫字母，底線分隔)。範例：`user_name`, `total_count`。
*   **函式:** 使用 `snake_case`。範例：`calculate_sum()`, `get_user_data()`。
*   **常數:** 使用 `UPPER_SNAKE_CASE` (大寫字母，底線分隔)。範例：`MAX_CONNECTIONS`, `API_ENDPOINT`。
*   **類別:** 使用 `PascalCase` (首字母大寫)。範例：`UserProfile`, `DatabaseConnection`。
*   **模組/套件:** 使用簡短、全小寫的名稱，可使用底線。範例：`utils`, `data_processing`。

## 3. 文件字串 (Docstrings)

*   **PEP 257:** 遵守 [PEP 257 -- Docstring Conventions](https://peps.python.org/pep-0257/)。
*   所有公開的模組、函式、類別和方法都應包含文件字串。
*   文件字串應使用三個雙引號 (`"""Docstring goes here."""`)。
*   第一行應為簡潔的摘要。
*   若有多行，摘要後空一行，接著是更詳細的說明。
*   對於函式和方法，應說明其參數、回傳值和可能引發的例外。

```python
def example_function(param1: int, param2: str) -> bool:
    """
    這是一個範例函式的簡短摘要。

    這個函式執行某些操作並根據輸入參數回傳布林值。

    Args:
        param1: 第一個參數的說明。
        param2: 第二個參數的說明。

    Returns:
        表示操作是否成功的布林值。

    Raises:
        ValueError: 如果 param2 無效。
    """
    if not param2:
        raise ValueError("param2 不能是空的")
    # ... 函式邏輯 ...
    return True
```

## 4. 型別提示 (Type Hints)

*   **PEP 484:** 盡可能使用型別提示 ([PEP 484 -- Type Hints](https://peps.python.org/pep-0484/))。
*   為函式參數和回傳值加上型別提示。
*   對於複雜的型別，使用 `typing` 模組。

```python
from typing import List, Dict, Optional

def process_data(data: List[Dict[str, int]], threshold: Optional[int] = None) -> None:
    # ... 函式邏輯 ...
    pass
```

## 5. 錯誤處理

*   使用明確的例外處理 (`try...except`)。
*   避免使用過於籠統的 `except:` 或 `except Exception:`，除非有充分理由。應捕捉具體的例外類型。
*   在適當的情況下定義自訂例外。

## 6. 測試

*   鼓勵編寫單元測試和整合測試。
*   建議使用 `pytest` 作為測試框架。
*   測試程式碼應與原始碼分開存放（例如在 `tests/` 目錄下）。

## 7. Linting

*   使用 `ruff` 或 `pylint` 等工具進行靜態程式碼分析，以檢查風格和潛在錯誤。
*   將 linter 整合到開發流程和 CI/CD 中。

## 8. 其他

*   **註解:** 註解應簡潔明瞭，解釋 *為什麼* 這樣做，而不是 *做了什麼*（程式碼本身應能說明做了什麼）。
*   **避免魔法數字:** 將常數定義為具名常數。
*   **保持簡單:** 優先選擇簡單直接的解決方案。