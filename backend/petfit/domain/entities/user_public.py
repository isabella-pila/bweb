
from petfit.domain.value_objects.email_vo import Email

class UserPublic:
    def __init__(self, id: str, name: str, email: Email):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"UserPublic(id='{self.id}', name='{self.name}', email='{self.email}')"

    def __eq__(self, other):
        if not isinstance(other, UserPublic):
            return NotImplemented
        return self.id == other.id and self.name == other.name and self.email == other.email
    
    def __hash__(self):
        return hash((self.id, self.name, self.email))