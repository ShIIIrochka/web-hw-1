# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.base_model import BaseModel


@dataclass
class User(BaseModel):
    """Модель пользователя."""

    email: str
    login: str
    password: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @classmethod
    def create(cls, email: str, login: str, password: str) -> User:
        """Создает нового пользователя.

        Args:
            email (str): Электронная почта
            login (str): Логин
            password (str): Пароль

        Returns:
            User: Созданный пользователь
        """
        return cls(
            email=email,
            login=login,
            password=password,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def update(
        self,
        email: str,
        login: str,
    ) -> User:
        """Обновляет пользователя.

        Args:
            email (str | None, optional): Новый email
            login (str | None, optional): Новый логин

        Returns:
            User: Обновленный пользователь
        """
        self.login = login
        self.email = email
        self.updated_at = datetime.now()
        return self
