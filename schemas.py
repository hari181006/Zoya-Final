from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    mobile: str = Field(pattern=r"^\d{10}$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginRequest(BaseModel):
    mobile: str = Field(pattern=r"^\d{10}$")
    password: str = Field(min_length=1, max_length=128)

class SupportRequestIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    mobile: str = Field(min_length=5, max_length=20)
    message: str = Field(min_length=1, max_length=5000)
