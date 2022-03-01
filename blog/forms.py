from .models import Comment
from django import forms

# form to make a comment on the sites blogs


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fieldss = ('body',)

