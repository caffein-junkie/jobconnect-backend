from passlib.context import CryptContext
from app.config import settings

security_context = CryptContext(
    schemes=["bcrypt", "argon2"],
    deprecated="auto",
    bcrypt__rounds=settings.BCRYPT_ROUNDS,
    argon2__time_cost=3,
    argon2__memory_cost=65536,
    argon2__parallelism=4,
    argon2__hash_len=32
)


class SecurityUtils:
    
    @staticmethod
    def hash_password(password: str) -> str:
        """"""
        return security_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """"""
        return security_context.verify(password, hashed_password)
