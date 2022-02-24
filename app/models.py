from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email é obrigatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if(not extra_fields.get('is_superuser')):
            raise ValueError('Superuser precisa estar ativo')
        if(not extra_fields.get('is_staff')):
            raise ValueError('Staff precisa estar ativo')

        return self._create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    nome_completo = models.CharField('Nome comlpeto', max_length=100)
    interesse = models.CharField('Area de interesse', max_length=100)
    linkedin = models.CharField('Linkedin', max_length=100)
    is_staff = models.BooleanField('Membro', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo', 'interesse']

    def __str__(self):
        return self.email
    
    objects = CustomUserManager()
