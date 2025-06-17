import os
from fastapi import FastAPI, Request, HTTPException # HTTPException 추가
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles # CSS, JS 등 정적 파일 서빙용
from fastapi.templating import Jinja2Templates

#detector.py와 plagiarism_models.py는 이전과 동일하다고 가정
from app.core.detector import find_plagiarism 
from app.models.plagiarism_models import PlagiarismCheckRequest, PlagiarismCheckResponse
# config.py도 이전과 동일하다고 가정
from app.core.config import settings


# 현재 파일(main.py)의 디렉토리 경로를 기준으로 절대 경로 설정
# app_dir = os.path.dirname(os.path.abspath(__file__)) # 이 방식은 심볼릭 링크 등에서 문제 소지 가능
# 보다 안정적인 방식:
current_file_path = os.path.abspath(__file__)
app_dir = os.path.dirname(current_file_path) # .../app
project_root = os.path.dirname(app_dir) # .../plagiarism_checker_project

app = FastAPI(title="표절 검사 API")

# 정적 파일 마운트 (예: app/static 폴더에 CSS, JS 파일이 있을 경우)
app.mount("/static", StaticFiles(directory=os.path.join(app_dir, "static")), name="static")
# 위 index.html은 style을 내부에 포함하고 있어 별도 static 설정이 필수는 아님

# Jinja2 템플릿 설정 (templates 폴더가 app 폴더 내에 있다고 가정)
templates = Jinja2Templates(directory=os.path.join(app_dir, "templates"))


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    메인 index.html 페이지를 서빙합니다.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/check_plagiarism", response_model=PlagiarismCheckResponse)
async def check_plagiarism_endpoint(request_data: PlagiarismCheckRequest):
    """
    기사 텍스트와 원본 텍스트를 입력받아 표절 분석 결과를 반환합니다.
    index.html의 JavaScript에서 이 엔드포인트를 호출합니다.
    """
    if not request_data.article_text.strip() or not request_data.source_text.strip():
        raise HTTPException(status_code=400, detail="기사 내용과 원본 내용이 모두 필요합니다.")
    
    try:
        # detector.py의 find_plagiarism 함수는 이미 PlagiarismCheckResponse 구조와
        # 호환되는 dict를 반환하도록 설계되었습니다.
        result = find_plagiarism(
            article_text=request_data.article_text,
            source_text=request_data.source_text
        )
        return result
    except Exception as e:
        # 실제 운영 환경에서는 더 상세한 로깅 및 에러 처리가 필요합니다.
        # print(f"Error during plagiarism check: {e}") # 서버 로그에 에러 기록
        raise HTTPException(status_code=500, detail=f"표절 검사 중 서버 오류 발생: {str(e)}")