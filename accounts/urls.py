from django.urls import path  # Importa el módulo para definir URLs en Django
from django.contrib.auth.views import LoginView, LogoutView
# Importa las vistas de autenticación predeterminadas de Django
from . import views  # Importa las vistas personalizadas del módulo actual

# Lista de patrones de URL para la aplicación
urlpatterns = [
    # Ruta para la vista de registro y login de usuario
    path(
        'signup/',
        views.UserCreateAndLoginView.as_view(),
        name='signup'
    ),

    # Ruta para la vista de login utilizando una plantilla personalizada
    path(
        '',
        LoginView.as_view(template_name='login.html'),
        name='login'
    ),

    # Ruta para la vista de logout
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),

    # Ruta para la vista de detalles del usuario, identificada por el ID del usuario
    path(
        'user_detail/<int:pk>/',
        views.UserDetail.as_view(),
        name='detalle_user'
    ),

    # Ruta para la vista de actualización de usuario, identificada por el ID del usuario
    path(
        'user_update/<int:pk>/',
        views.UserUpdate.as_view(),
        name='Actualizar_user'
    ),

    # Ruta para la vista de cambio de contraseña
    path(
        'password_change/',
        views.PasswordChange.as_view(),
        name='Cambiar_password'
    ),

    # Ruta para la vista que se muestra después de cambiar la contraseña
    path(
        'password_change/done/',
        views.PasswordChangeDone.as_view(),
        name='password_change_done'
    ),

    # Ruta para la vista de eliminación de usuario, identificada por el ID del usuario
    path(
        'user_delete/<int:pk>/',
        views.UserDelete.as_view(),
        name='borrar_user'
    ),
]
