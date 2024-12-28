from pydantic import BaseModel, EmailStr


class UserBaseDTO(BaseModel):
    username: str
    email: EmailStr


class UserCreateDTO(UserBaseDTO):
    password: str


class UserResponseDTO(UserBaseDTO):
    id: int

    class Config:
        from_attributes = True
