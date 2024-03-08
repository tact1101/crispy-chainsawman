from django import forms
from .models import Comment, CustomUser
from django.contrib.auth.forms import UserCreationForm, authenticate



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text'] 
        
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text.strip():
            raise forms.ValidationError('Text field cannot be empty')
        return text

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 5})
        
        
class CustomUserCreationForm(UserCreationForm):
    pfp = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'pfp']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.pfp = self.cleaned_data['pfp']
        if commit:
            user.save()
        return user

        
class UserAuthForm(forms.Form):
    username_or_email = forms.CharField(max_length=254)
    password = forms.CharField(max_length=30)  
    
    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        
        if username_or_email and password:
            user = authenticate(username=username_or_email, password=password)
            if user is None:
                # authenticate using email
                user = authenticate(email=username_or_email, password=password)

            if user is None:
                raise forms.ValidationError("Invalid username/email or password.")
            
        return cleaned_data
        
    
    