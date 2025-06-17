# -----------------------------------------------------------------------------
# 파일: app/core/detector.py
# 설명: 실제 표절 검사 로직을 구현합니다.
# -----------------------------------------------------------------------------
import difflib
import unicodedata
from app.core.config import settings # 설정 값 가져오기

def normalize_text(text: str) -> str:
    """
    텍스트 정규화 함수: 유니코드 NFC 정규화, 공백 표준화.
    Args:
        text (str): 입력 텍스트
    Returns:
        str: 정규화된 텍스트
    """
    if not text:
        return ""
    # 유니코드 정규화 (조합형 문자를 완성형으로)
    text = unicodedata.normalize('NFC', text)
    # 여러 종류의 공백(스페이스, 탭, 줄바꿈 등)을 단일 스페이스로 대체 후 양쪽 공백 제거
    text = " ".join(text.split())
    return text

def find_plagiarism(article_text: str, source_text: str) -> dict:
    """
    두 텍스트를 비교하여 표절률 및 복사된 부분을 찾습니다.
    Args:
        article_text (str): 검사 대상 기사 텍스트
        source_text (str): 원본 자료 텍스트
    Returns:
        dict: 표절 검사 결과 (표절률, 복사된 부분 상세 정보 등)
    """
    if not article_text or not source_text:
        return {
            "percentage_copied": 0.0,
            "total_article_chars": len(article_text or ""),
            "total_copied_chars": 0,
            "copied_segments": [],
            "article_preview": (article_text or "")[:200] + "..." if article_text else "",
            "source_preview": (source_text or "")[:200] + "..." if source_text else ""
        }

    normalized_article = normalize_text(article_text)
    normalized_source = normalize_text(source_text)

    # 문자 리스트로 변환하여 SequenceMatcher 사용 (엄격한 문자 단위 비교)
    seq_article = list(normalized_article)
    seq_source = list(normalized_source)

    # SequenceMatcher 생성. autojunk=False로 설정하여 모든 요소를 비교.
    matcher = difflib.SequenceMatcher(None, seq_article, seq_source, autojunk=False)
    
    # 일치하는 블록 가져오기: (article_idx, source_idx, length) 튜플의 리스트
    matching_blocks = matcher.get_matching_blocks()

    total_copied_chars = 0
    copied_segments_details = []
    
    # 설정에서 최소 일치 길이 가져오기
    min_match_len = settings.MIN_MATCH_LENGTH_CHARS

    for i, j, n in matching_blocks:
        # 마지막 블록은 SequenceMatcher가 추가하는 더미 블록이므로 제외 (길이가 0)
        if n == 0: 
            continue
        if n >= min_match_len: # 설정된 최소 일치 길이 이상인 경우에만 고려
            # 일치하는 세그먼트(부분 문자열) 추출
            segment = "".join(seq_article[i : i + n])
            total_copied_chars += n
            copied_segments_details.append({
                "article_start_char_index": i,
                "source_start_char_index": j,
                "length_chars": n,
                "segment_text": segment
            })
    
    article_total_chars = len(seq_article)
    # 기사 전체 길이가 0일 경우 ZeroDivisionError 방지
    copy_percentage = (total_copied_chars / article_total_chars) * 100 if article_total_chars > 0 else 0

    return {
        "percentage_copied": round(copy_percentage, 2),
        "total_article_chars": article_total_chars,
        "total_copied_chars": total_copied_chars,
        "copied_segments": copied_segments_details,
        "article_preview": normalized_article[:200] + "..." if normalized_article else "",
        "source_preview": normalized_source[:200] + "..." if normalized_source else ""
    }