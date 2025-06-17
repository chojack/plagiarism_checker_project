# -----------------------------------------------------------------------------
# 파일: app/core/config.py
# 설명: 애플리케이션 설정을 관리합니다.
# -----------------------------------------------------------------------------
# from pydantic_settings import BaseSettings # pydantic-settings v2.0+
#from pydantic import BaseSettings # pydantic v1.x (uvicorn 기본 설치와 호환성 고려)
from pydantic_settings import BaseSettings # <--- 이렇게 수정하세요!

class Settings(BaseSettings):
    MIN_MATCH_LENGTH_CHARS: int = 5  # 표절로 간주할 최소 일치 문자 수
    # 필요에 따라 다른 설정 추가 가능
    # 예: API_KEY: str = "your_secret_api_key"

    class Config:
        # .env 파일을 사용할 경우 (선택 사항)
        # env_file = ".env"
        pass

settings = Settings()