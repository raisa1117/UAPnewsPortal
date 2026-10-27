from django import forms
from .models import Comment, Post

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Comma separated, up to 6", widget=forms.TextInput(attrs={"placeholder": "exam, fest, cse"}))
    class Meta:
        model = Post
        fields = ["title", "kind", "category", "body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 12, "maxlength": 6000})}
    field_order = ["title", "kind", "category", "tags", "body"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 2, "placeholder": "Add a comment"})}
        labels = {"body": ""}
