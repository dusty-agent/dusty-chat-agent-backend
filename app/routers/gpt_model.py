from fastapi import APIRouter

router = APIRouter()

@router.get("/model")
def get_model():
    """현재 사용 가능한 GPT 모델 반환"""
    return {"models": ["gpt-3.5-turbo", "gpt-4"]}