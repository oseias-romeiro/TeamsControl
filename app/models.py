from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

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

class Team(models.Model):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True,)
    participants = models.ManyToManyField(CustomUser, related_name='+')
    name = models.CharField('Name', max_length=20)
    focus = models.CharField('Focus', max_length=50)
    max = models.PositiveIntegerField('Max participants', default=1,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ])
    description = models.CharField('Description', max_length=200)
    private = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.owner
    
    def clean(self, *args, **kwargs):
        if self.participants.count() > self.max:
            raise ValidationError(f"You can't assign more than {self.max} participants")
        super(Team, self).clean(*args, **kwargs)
