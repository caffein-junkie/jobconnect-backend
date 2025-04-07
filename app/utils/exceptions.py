from fastapi import HTTPException, status
from typing import Optional


class JobConnectException(HTTPException):
    """Base exception class for consistent error handling"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[dict] = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.code = status_code
        self.detail = detail


class InvalidCredentialsException(JobConnectException):
    """Raised when login fails"""
    def __init__(self, detail: str = "Invalid email or password") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class AccountLockedException(JobConnectException):
    """Raised when an account is locked or inactive"""
    def __init__(self, detail: str = "Account is locked") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class TokenExpiredException(JobConnectException):
    """Raised when a JWT token is expired"""
    def _init__(self, detail: str = "Token expired") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class PermissionDeniedException(JobConnectException):
    """Raised when user lacks required permissions"""
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )
    

class NotFoundException(JobConnectException):
    """Raised when resource is not found"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class RateLimitExceededException(JobConnectException):
    """Raised when rate limit is exceeded"""
    def __init__(self, detail: str = "Too many requests"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers={"Retry-After": "60"}
        )


class DuplicateEntryException(JobConnectException):
    """"""
    def __init__(self, detail: str = "Email or phone number already exists"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
        )
