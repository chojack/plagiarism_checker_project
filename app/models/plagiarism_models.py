# -----------------------------------------------------------------------------
# 파일: app/models/plagiarism_models.py
# 설명: API 요청 및 응답 데이터 모델을 정의합니다. (Pydantic 사용)
# -----------------------------------------------------------------------------
from pydantic import BaseModel
from typing import List, Optional

class PlagiarismCheckRequest(BaseModel):
    article_text: str
    source_text: str

class CopiedSegmentDetail(BaseModel):
    article_start_char_index: int
    source_start_char_index: int
    length_chars: int
    segment_text: str

class PlagiarismCheckResponse(BaseModel):
    percentage_copied: float
    total_article_chars: int
    total_copied_chars: int
    copied_segments: List[CopiedSegmentDetail]
    article_preview: Optional[str] = None # 원본 기사 미리보기 (앞부분)
    source_preview: Optional[str] = None  # 원본 자료 미리보기 (앞부분)