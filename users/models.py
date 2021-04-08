from django.contrib.auth.models import AbstractUser
from django.db import models


class AdvUser(AbstractUser):
    class UserRole(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    role = models.TextField('Роль', choices=UserRole.choices,
                            default=UserRole.USER, )
    email = models.EmailField(unique=True, db_index=True)
    bio = models.TextField('Биография', blank=True, )
    confirmation_code = models.CharField('Код подтверждения', max_length=24,
                                         blank=True, null=True)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator' or self.is_superuser

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
