from __future__ import annotations
import argparse
import sys
from pathlib import Path

import pymupdf as pymupdf  # PyMuPDF
import pymupdf4llm


def parse_pages_spec(spec: str, page_count: int) -> list[int]:
    """解析 1-based 頁範圍字串為 0-based 整數清單。
    支援格式："1-5,8,10-12"；若超出頁數或格式錯誤將拋出 ValueError。
    參數：
      - spec: 頁範圍字串（1-based）
      - page_count: PDF 總頁數
    回傳：0-based 頁碼清單（已排序且去重）
    """
    pages: set[int] = set()
    parts = [s.strip() for s in spec.split(",") if s.strip()]
    for p in parts:
        if "-" in p:
            a, b = [x.strip() for x in p.split("-", 1)]
            if not a.isdigit() or not b.isdigit():
                raise ValueError(f"頁範圍片段格式錯誤：{p}")
            start = int(a)
            end = int(b)
            if start <= 0 or end <= 0 or start > end:
                raise ValueError(f"頁範圍不合法：{p}")
            for i in range(start, end + 1):
                if i > page_count:
                    raise ValueError(f"指定頁碼 {i} 超出總頁數 {page_count}")
                pages.add(i - 1)
        else:
            if not p.isdigit():
                raise ValueError(f"頁碼格式錯誤：{p}")
            idx1 = int(p)
            if idx1 <= 0 or idx1 > page_count:
                raise ValueError(f"指定頁碼 {idx1} 超出總頁數 {page_count}")
            pages.add(idx1 - 1)
    return sorted(pages)


def build_markdown_from_chunks(chunks: list[dict]) -> str:
    """將 page_chunks 的 list[dict] 合併為單一 Markdown 字串。
    每頁前加上頁界線註解：<!-- page: N -->（N 以 1 開始）。
    """
    parts: list[str] = []
    for i, page in enumerate(chunks, start=1):
        text = page.get("text", "") or ""
        parts.append(f"\n\n<!-- page: {i} -->\n\n{text}")
    return "".join(parts)


def pdf_to_markdown(
    input_path: str,
    output_path: str,
    *,
    pages: list[int] | None = None,
    image_dir: str | None = None,
    table_strategy: str = "lines_strict",
    use_toc: bool = True,
    page_chunks: bool = True,
    show_progress: bool = True,
    write_images: bool = True,
) -> None:
    """讀取 PDF 並輸出 Markdown。
    - 以 TOC 判定標題層級（use_toc）
    - 圖片輸出為檔案（write_images + image_dir）
    - 可選頁範圍（pages 為 0-based；None=全部）
    - 可啟用每頁分塊（page_chunks）與進度列（show_progress）
    - 表格策略（table_strategy）可調整
    """
    in_path = Path(input_path)
    out_path = Path(output_path)
    if not in_path.exists():
        raise FileNotFoundError(f"找不到輸入檔：{in_path}")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(str(in_path))
    try:
        hdr_info = pymupdf4llm.TocHeaders(doc) if use_toc else None

        final_image_dir: Path | None = None
        if write_images:
            final_image_dir = Path(image_dir) if image_dir else (out_path.parent / "images")
            final_image_dir.mkdir(parents=True, exist_ok=True)

        ts = None if table_strategy.lower() in {"none", "off", "disable"} else table_strategy

        md_or_chunks = pymupdf4llm.to_markdown(
            doc,
            pages=pages,
            hdr_info=hdr_info,
            write_images=bool(write_images),
            embed_images=False,
            ignore_images=False,
            ignore_graphics=False,
            dpi=150,
            image_path=str(final_image_dir) if final_image_dir else "",
            image_format="png",
            force_text=True,
            margins=0,
            page_chunks=bool(page_chunks),
            table_strategy=ts,
            show_progress=bool(show_progress),
        )

        md_text = build_markdown_from_chunks(md_or_chunks) if page_chunks else str(md_or_chunks)
        out_path.write_bytes(md_text.encode("utf-8"))
    finally:
        doc.close()


def _build_arg_parser() -> argparse.ArgumentParser:
    """建立命令列參數解析器。"""
    p = argparse.ArgumentParser(description="PDF → Markdown 轉換（PyMuPDF4LLM）")
    p.add_argument("-i", "--input", required=True, help="輸入 PDF 檔路徑")
    p.add_argument("-o", "--output", required=True, help="輸出 Markdown 檔路徑")
    p.add_argument("--pages", help="頁範圍（1-based），如: 1-5,8,10-12；未提供則處理全部")
    p.add_argument("--write-images", action="store_true", default=True, help="輸出圖片檔（預設開啟）")
    p.add_argument("--image-dir", help="圖片輸出目錄，預設為輸出檔同層 images 子目錄")
    p.add_argument("--use-toc", action="store_true", default=True, help="使用 TOC 判定標題層級（預設開啟）")
    p.add_argument("--table-strategy", default="lines_strict", choices=["lines_strict", "lines", "none"], help="表格偵測策略")
    p.add_argument("--page-chunks", action="store_true", default=True, help="每頁分塊輸出（預設開啟）")
    p.add_argument("--show-progress", action="store_true", default=True, help="顯示處理進度（預設開啟）")
    return p


def main(argv: list[str] | None = None) -> int:
    """主進入點：解析參數與執行轉換。"""
    argv = argv if argv is not None else sys.argv[1:]
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    in_path = Path(args.input)
    try:
        with pymupdf.open(str(in_path)) as tmp_doc:
            pages_0: list[int] | None = None
            if args.pages:
                pages_0 = parse_pages_spec(args.pages, len(tmp_doc))

        pdf_to_markdown(
            input_path=str(in_path),
            output_path=args.output,
            pages=pages_0,
            image_dir=args.image_dir,
            table_strategy=args.table_strategy,
            use_toc=bool(args.use_toc),
            page_chunks=bool(args.page_chunks),
            show_progress=bool(args.show_progress),
            write_images=bool(args.write_images),
        )
        print(f"已將 {in_path} 轉換為 {args.output}")
        return 0
    except Exception as e:
        print(f"錯誤：{e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
