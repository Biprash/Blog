from django import forms
from users.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

        # widgets = {
        #     'username':forms.TextInput(attrs={'class':'form-control form-control-lg'}),
        #     'email':forms.TextInput(attrs={'class':'form-control form-control-lg'}),
        #     'password1':forms.PasswordInput(attrs={'class':'form-control form-control-lg'})

        # }
    
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        
        return user
    
class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

        # widgets = {
        #     'username':forms.TextInput(attrs={'class':'form-control form-control-lg is-invalid'}),
        #     'password':forms.PasswordInput(attrs={'class':'form-control form-control-lg is-invalid'})
        # }

    