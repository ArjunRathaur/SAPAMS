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

class ConfirmForm(forms.Form):
    text = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control transparent-input',
        'placeholder': "Type 'CONFIRM' to confirm this action."
    }))

class GradeForm(forms.Form):
    value = forms.CharField(label="", widget=forms.NumberInput(attrs={
        'class': 'form-control transparent-input',
        'placeholder': 'Grade'
    }))

class CreateCourseForm(forms.Form):
    courseCode = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control transparent-input',
        'placeholder': "Course Code"
    }))
    courseName = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control transparent-input',
        'placeholder': "Course Name"
    }))
    studentEmails = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'form-control transparent-input',
        'placeholder': "Enter student email addresses, separated by commas (,) and NO SPACES."
    }))
    teacherEmails = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'form-control transparent-input',
        'placeholder': "Enter email addresses of other teachers you want to give access to this course to, separated by commas (,) and NO SPACES."
    }), required=False)

class CreateAssignmentForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control transparent-input',
        'placeholder': "Name"
    }))
    criteria = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'form-control transparent-input',
        'placeholder': "Enter the criteria for this assignment - each new line is a new criteria."
    }))
    intensity = forms.CharField(label="", widget=forms.NumberInput(attrs={
        'class': 'form-control transparent-input',
        'placeholder': 'Intensity (1 to 10)'
    }))