from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True, max_length=30)
    message = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        fields = ['name', 'email', 'message']
class Status(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        
        fields = ['password']