from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Definición de un gestor personalizado para el modelo de usuario
class CustomUserManager(BaseUserManager):
    # Método para crear un usuario normal
    def create_user(self, email, username, password=None, **extra_fields):
        # Verifica si el campo de email está definido
        if not email:
            raise ValueError(_('The Email field must be set'))
        # Normaliza el email (convierte a minúsculas y quita espacios innecesarios)
        email = self.normalize_email(email)
        # Crea una instancia del modelo de usuario con los datos proporcionados
        user = self.model(email=email, username=username, **extra_fields)
        # Establece la contraseña del usuario
        user.set_password(password)
        # Guarda el usuario en la base de datos
        user.save(using=self._db)
        return user

    # Método para crear un superusuario (admin)
    def create_superuser(self, email, username, password=None, **extra_fields):
        # Establece valores predeterminados para los campos de superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Verifica que el superusuario tenga permisos de staff
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        # Verifica que el superusuario tenga permisos de superusuario
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        # Crea el superusuario con los datos proporcionados
        return self.create_user(email, username, password, **extra_fields)


# Definición de un modelo de usuario personalizado
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Campo para el nombre de usuario
    username = models.CharField(_('username'), max_length=150)
    # Campo para el email, único para cada usuario
    email = models.EmailField(_('email address'), unique=True)
    # Campo para la edad del usuario
    age = models.PositiveIntegerField(_('age'), default=0, blank=True)
    # Campo para indicar si el usuario es superusuario
    is_superuser = models.BooleanField(default=False)
    # Campo para indicar si el usuario es parte del staff
    is_staff = models.BooleanField(_('staff status'), default=False)
    # Campo para indicar si el usuario está activo
    is_active = models.BooleanField(_('active'), default=True)
    # Campo para almacenar la fecha de creación del usuario
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Asigna el gestor personalizado al modelo
    objects = CustomUserManager()

    # Campos que se utilizan para la autenticación
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Metadatos del modelo
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'
        swappable = 'AUTH_USER_MODEL'

    # Método para normalizar el email antes de guardar
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    # Método para enviar un correo electrónico al usuario
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
