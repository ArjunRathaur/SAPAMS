from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label="", widget=forms.EmailInput(attrs = {
        'class': 'form-control transparent-input',
        'placeholder': 'Email'
    }))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs = {
        'class': 'form-control transparent-input',
        'placeholder': 'Password'
    }))

class SubmitAssignmentForm(forms.Form):
    text = forms.CharField(label="Submit your work", widget=forms.Textarea(attrs={
        'class': 'form-control transparent-input',
        'placeholder': 'Submission text or links'
    }))

class ChangePasswordForm(forms.Form):
    current = forms.CharField(label="", widget=forms.PasswordInput(attrs = {
        'class': 'form-control transparent-input',
        'placeholder': 'Current password'
    }))
    new1 = forms.CharField(label="", widget=forms.PasswordInput(attrs = {
        'class': 'form-control transparent-input',
        'placeholder': 'New password'
    }))
    new2 = forms.CharField(label="", widget=forms.PasswordInput(attrs = {
        'class': 'form-control transparent-input',
        'placeholder': 'Repeat new password'
    }))

class CreateDisputeForm(forms.Form):
    text = forms.CharField(label="Dispute Message", widget=forms.Textarea(attrs={
        'class': 'form-control transparent-input',
        'placeholder': 'Enter your dispute here'
    }))

class DisputeResponseForm(forms.Form):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'form-control transparent-input',
        'placeholder': 'Enter your response here.'
    }))