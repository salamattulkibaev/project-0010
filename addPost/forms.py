from django import forms
from mainPage.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "user",
            "title",
            "description",
            "image",
            "category",
            "city",
            "status"
        ]