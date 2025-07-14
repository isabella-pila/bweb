import re
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Self # Necessário para type hinting do retorno do validador

class PasswordValidationError(Exception):
    pass

class Password:
    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValueError("Password must be at least 8 characters and contain letters and numbers.")
        self._value = value

    def _is_valid(self, password: str) -> bool:
        return len(password) >= 8 and any(c.isalpha() for c in password) and any(c.isdigit() for c in password)

    def value(self) -> str:
        return self._value

    def __eq__(self, other) -> bool:
        if isinstance(other, Password):
            return self._value == other._value
        if isinstance(other, str): # Permite Password("myP@ss123") == "myP@ss123"
            return self._value == other
        return NotImplemented

    def __str__(self) -> str:
        
        return "*" * len(self._value)

    def __hash__(self) -> int: # Adicionado: Bom ter __hash__ se você define __eq__
        return hash(self._value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: type, handler: GetCoreSchemaHandler) -> CoreSchema:
        """
        Define como o Pydantic deve lidar com a validação e serialização do tipo Password.
        """
        def validate_from_str(value: str) -> Self:
            """Valida uma string e cria uma instância de Password."""
            return cls(value) # Chama o __init__ do Password com a string validada

        string_schema = core_schema.str_schema()
        password_instance_schema = core_schema.is_instance_schema(cls)
        plain_validator = core_schema.no_info_plain_validator_function(validate_from_str)

        return core_schema.union_schema(
            [
                password_instance_schema,
                core_schema.chain_schema([string_schema, plain_validator])
            ],
            # Define como o Password deve ser serializado de volta para uma string.
            # CUIDADO: Em produção real, você NUNCA retornaria a senha em texto claro.
            # Para o esquema da documentação, um valor 'str' é necessário.
            serialization=core_schema.to_string_ser_schema()
        )