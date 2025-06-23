from petfit.domain.values_objects.email_vo import Email
from petfit.domain.values_objects.password import Password

class  User:
    def __init__(self,id: str, name: str, email: Email, password: Password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password



        
