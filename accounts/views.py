from django.urls import reverse_lazy, reverse  # type: ignore
from django.contrib.auth import (  # type: ignore
    login,
    authenticate,
    logout,
    get_user_model,
)

from .forms import CustomUserCreationForm, UserUpdateForm
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.views import (    # type: ignore
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.contrib.auth.mixins import UserPassesTestMixin  # type: ignore


# user model
User = get_user_model()


# usuario solo puede ver sus propios datos
class OnlyYouMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


# class para registrar un usuario
class UserCreateAndLoginView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('tasks:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        raw_pw = form.cleaned_data.get("password1")
        user = authenticate(email=email, password=raw_pw)
        login(self.request, user)
        return response


# class para ver un detalle de un usuario
class UserDetail(DetailView):
    model = User
    template_name = 'userdetalle.html'


# class para editar un usuario
class UserUpdate(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'useredit.html'

    def get_success_url(self):
        return reverse('detalle_user', kwargs={'pk': self.kwargs['pk']})


# class para cambiar la contraseña
class PasswordChange(PasswordChangeView):
    template_name = 'cambiarcontraseña.html'


# class para cambiar la contraseña
class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'userdetalle.html'


# class para borrar un usuario
class UserDelete(DeleteView):
    model = User
    template_name = 'userdelete.html'
    success_url = reverse_lazy('login')
