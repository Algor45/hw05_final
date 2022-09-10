"""Set your Posts forms here."""

from django import forms

from .models import Comment, Group, Post


class PostForm(forms.ModelForm):
    """Создание формы модели записей."""

    text = forms.CharField(required=True)

    class Meta():
        """Наследование от модели Post."""

        model = Post
        fields = ('text', 'group', 'image')

    def clean_text(self):
        """Проверка валидности формы."""
        text_check = self.cleaned_data['text']

        if (text_check == '' or text_check.isspace()):
            raise forms.ValidationError("Поле текст не может быть пустым")
        return text_check

    def get_group_list(self):
        """Функция для получения групп."""
        return Group.objects.all()


class CommentForm(forms.ModelForm):
    """Создание формы модели комментариев."""

    text = forms.CharField(required=True)

    class Meta():
        """Наследование от модели Comment."""

        model = Comment
        fields = {'text'}

    def clean_text(self):
        """Проверка валидности формы."""
        text_check = self.cleaned_data['text']

        if (text_check == '' or text_check.isspace()):
            raise forms.ValidationError("Поле текст не может быть пустым")
        return text_check
