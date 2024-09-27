from pydantic import BaseModel, EmailStr, conint, ValidationError
class UserModel(BaseModel):
        name: str
        email: EmailStr
        age: conint(ge=0, le=120)

        def to_dict(self):
            return {
                "name":self.name,
                "email":self.email,
                "age":self.age

            }

