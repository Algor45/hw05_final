"""Set your users forms here."""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    """Форма создания нового пользователя."""

    class Meta(UserCreationForm.Meta):
        """Наследование от UserCreationForm."""

        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
