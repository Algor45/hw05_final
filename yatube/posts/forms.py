from django import forms

from .models import Comment, Group, Post


class PostForm(forms.ModelForm):
    """Форма модели записей"""
    text = forms.CharField(required=True)

    class Meta():
        model = Post
        fields = ('text', 'group', 'image')

    def clean_text(self):
        text_check = self.cleaned_data['text']

        if (text_check == '' or text_check.isspace()):
            raise forms.ValidationError("Поле текст не может быть пустым")
        return text_check

    def get_group_list(self):
        return Group.objects.all()


class CommentForm(forms.ModelForm):
    text = forms.CharField(required=True)

    class Meta():
        model = Comment
        fields = {'text'}

    def clean_text(self):
        text_check = self.cleaned_data['text']

        if (text_check == '' or text_check.isspace()):
            raise forms.ValidationError("Поле текст не может быть пустым")
        return text_check
