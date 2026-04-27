import os
import re
import difflib
import json
import threading
from typing import List, Dict, Any
from .doc_parser import parse_document

def _normalize_text(text: str) -> str:
    """공백, 줄바꿈, 특수문자를 제거하여 순수 텍스트만 남깁니다."""
    if not text:
        return ""
    # 영문/숫자/한글만 남기고 모두 제거
    s = re.sub(r'[^a-zA-Z0-9가-힣]', '', text)
    return s

class WordingVerifier:
    def __init__(self, doc_path: str):
        self.doc_path = doc_path
        self.doc_raw_text = parse_document(doc_path)
        self.doc_norm_text = _normalize_text(self.doc_raw_text)
        # differences: {"page_title": [{"original_text": "...", "reason": "..."}]}
        self.differences: Dict[str, List[Dict[str, str]]] = {}
        self._lock = threading.Lock()
        
        
    def verify_page(self, page_title: str, page_texts: List[str]):
        """
        웹페이지에서 추출한 텍스트 리스트(문항/보기들)를 원본 문서와 비교합니다.
        문서에 없거나 크게 다르면 differences에 추가합니다.
        """
        if not self.doc_norm_text:
            return

        diffs = []
        for text in page_texts:
            text = str(text).strip()
            if not text:
                continue
                
            norm_t = _normalize_text(text)
            if not norm_t or len(norm_t) < 3: # 너무 짧은 텍스트(예: "1", "A")는 검증 생략
                continue
                
            # 문서 텍스트 안에 포함되어 있는지 확인
            if norm_t in self.doc_norm_text:
                continue
                
            # 포함되어 있지 않으면, difflib으로 유사도를 확인하여 비슷한 부분이 있는지 탐색
            # 문서 전체와 비교하면 오래 걸리므로, substring 매칭 방식의 한계가 있지만 
            # 일단 완벽히 포함되지 않은 항목을 오타/누락 의심으로 잡습니다.
            diffs.append({
                "original_text": text,
                "reason": "문서에서 정확히 일치하는 문구를 찾을 수 없습니다."
            })
            
        if diffs:
            with self._lock:
                if page_title not in self.differences:
                    self.differences[page_title] = []
                self.differences[page_title].extend(diffs)
            
    def generate_html_report(self, out_dir: str) -> str:
        """분석 결과를 HTML 리포트로 생성하여 저장하고 파일 경로를 반환합니다."""
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)
            
        report_path = os.path.join(out_dir, "diff_report.html")
        
        html = [
            "<!doctype html>",
            "<html lang='ko'>",
            "<head>",
            "  <meta charset='utf-8'/>",
            "  <title>워딩 검증 리포트</title>",
            "  <style>",
            "    body { font-family: sans-serif; background: #f4f4f9; padding: 20px; color: #333; }",
            "    h1 { color: #2c3e50; }",
            "    .summary { background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }",
            "    .page-section { background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }",
            "    .page-title { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; color: #e74c3c; border-bottom: 2px solid #eee; padding-bottom: 5px; }",
            "    .diff-item { margin-bottom: 10px; padding: 10px; background: #fff3f3; border-left: 4px solid #e74c3c; }",
            "    .diff-text { font-weight: bold; margin-bottom: 5px; }",
            "    .diff-reason { font-size: 0.9em; color: #666; }",
            "    .ok { color: #27ae60; font-weight: bold; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <h1>설문 워딩 검증 리포트</h1>",
            "  <div class='summary'>",
            f"    <p>기준 문서: <strong>{os.path.basename(self.doc_path)}</strong></p>",
            f"    <p>검출된 불일치 페이지 수: <strong>{len(self.differences)}</strong></p>",
            "  </div>"
        ]
        
        if not self.differences:
            html.append("<div class='summary'><p class='ok'>✅ 모든 문구가 원본 문서와 완벽하게 일치합니다!</p></div>")
        else:
            for page_title, diffs in self.differences.items():
                html.append("<div class='page-section'>")
                html.append(f"  <div class='page-title'>{page_title}</div>")
                for diff in diffs:
                    html.append("  <div class='diff-item'>")
                    html.append(f"    <div class='diff-text'>{diff['original_text']}</div>")
                    html.append(f"    <div class='diff-reason'>{diff['reason']}</div>")
                    html.append("  </div>")
                html.append("</div>")
                
        html.append("</body></html>")
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html))
            
        return report_path
