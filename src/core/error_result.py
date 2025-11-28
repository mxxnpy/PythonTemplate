"""
ErrorResult - Tipo de Erro Padrao

Representa diferentes tipos de erros com mensagens e categorias.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ErrorResult:
    """tipo padrao de erro"""

    messages: tuple[str, ...]
    is_validation: bool = False
    is_not_found: bool = False
    is_exception: bool = False
    is_unauthorized: bool = False
    is_forbidden: bool = False

    @classmethod
    def validation(cls, msg: str) -> ErrorResult:
        """erro de validacao (400)"""
        return cls(messages=(msg,), is_validation=True)

    @classmethod
    def validation_list(cls, msgs: list[str]) -> ErrorResult:
        """multiplos erros de validacao (400)"""
        return cls(messages=tuple(msgs), is_validation=True)

    @classmethod
    def not_found(cls, msg: str) -> ErrorResult:
        """recurso nao encontrado (404)"""
        return cls(messages=(msg,), is_not_found=True)

    @classmethod
    def exception(cls, msg: str) -> ErrorResult:
        """erro interno (500)"""
        return cls(messages=(msg,), is_exception=True)

    @classmethod
    def from_exception(cls, ex: Exception) -> ErrorResult:
        """cria ErrorResult a partir de excecao"""
        return cls(messages=(str(ex),), is_exception=True)

    @classmethod
    def unauthorized(cls, msg: str = "Nao autorizado") -> ErrorResult:
        """nao autenticado (401)"""
        return cls(messages=(msg,), is_unauthorized=True)

    @classmethod
    def forbidden(cls, msg: str = "Acesso negado") -> ErrorResult:
        """sem permissao (403)"""
        return cls(messages=(msg,), is_forbidden=True)

    @property
    def http_status(self) -> int:
        """retorna status http correspondente"""
        if self.is_validation:
            return 400
        if self.is_unauthorized:
            return 401
        if self.is_forbidden:
            return 403
        if self.is_not_found:
            return 404
        return 500

    @property
    def first_message(self) -> str:
        """retorna primeira mensagem de erro"""
        return self.messages[0] if self.messages else "Erro desconhecido"

    def __str__(self) -> str:
        return "; ".join(self.messages)


@dataclass
class ValidationBuilder:
    """builder para acumular erros de validacao"""

    errors: list[str] = field(default_factory=list)

    def add(self, condition: bool, msg: str) -> ValidationBuilder:
        """adiciona erro se condicao for True"""
        if condition:
            self.errors.append(msg)
        return self

    def add_if_empty(self, value: str | None, field_name: str) -> ValidationBuilder:
        """adiciona erro se valor estiver vazio"""
        if not value or not value.strip():
            self.errors.append(f"{field_name} e obrigatorio")
        return self

    def add_if_none(self, value: object | None, field_name: str) -> ValidationBuilder:
        """adiciona erro se valor for None"""
        if value is None:
            self.errors.append(f"{field_name} e obrigatorio")
        return self

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    @property
    def is_invalid(self) -> bool:
        return len(self.errors) > 0

    def build(self) -> ErrorResult | None:
        """retorna ErrorResult se houver erros, None caso contrario"""
        if self.is_invalid:
            return ErrorResult.validation_list(self.errors)
        return None
