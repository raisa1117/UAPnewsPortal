from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Department, Profile

class RegisterForm(UserCreationForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    student_id = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_student_id(self):
        v = self.cleaned_data["student_id"].strip()
        if v and Profile.objects.filter(student_id=v).exists():
            raise forms.ValidationError("This student ID is already registered.")
        return v or None

    def save(self, commit=True):
        user = super().save(commit)
        p = user.profile
        p.department, p.student_id = self.cleaned_data["department"], self.cleaned_data["student_id"]
        p.save()
        return user
