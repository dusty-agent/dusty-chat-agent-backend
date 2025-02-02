from passlib.context import CryptContext

# ✅ Bcrypt 해싱 알고리즘을 사용하여 비밀번호를 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 비밀번호 해싱 함수
def hash_password(password: str) -> str:
    """비밀번호를 해싱하여 저장"""
    return pwd_context.hash(password)

# ✅ 비밀번호 검증 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """입력된 비밀번호가 저장된 해시와 일치하는지 확인"""
    return pwd_context.verify(plain_password, hashed_password)
