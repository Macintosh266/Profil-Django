from django import forms
from .models import *

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content','link','photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content', 'post']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'post': forms.Select(),
            'author': forms.Select(),
        }

class LoginUser(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password1') != cleaned_data.get('new_password2'):
            raise forms.ValidationError("Yangi parollar bir xil emas.")
        return cleaned_data

class UserProfilForm(forms.ModelForm):
    class Meta:
        model = UserProfil
        fields = '__all__'
