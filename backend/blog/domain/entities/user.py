from blog.domain.values_objects.email_vo import Email
from blog.domain.values_objects.password import Password

class  User:
    def __init__(self,id: str, name: str, email: Email, password: Password,role: str):
        if role not in ["user"]:
            raise ValueError ("O usuario ")
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role


        
