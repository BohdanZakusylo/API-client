from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField()


class RequestForm(forms.Form):
    request_choices = [
        ('get', ''),
        ('post', ''),
        ('put', ''),
        ('patch' , ''),
        ('delete', ''),

    ]
    method = forms.ChoiceField()