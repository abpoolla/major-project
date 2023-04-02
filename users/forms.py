from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from localflavor.in_.forms import  INZipCodeField
from localflavor.in_.in_states import STATE_CHOICES
from django.forms import CharField
import re
#from validate_email import validate_email
from .models import Profile
import re

from django.core.exceptions import ImproperlyConfigured
from django.forms import ValidationError
from django.forms.fields import CharField, RegexField, Select
from django.utils.translation import gettext_lazy as _
aadhaar_re=re.compile(r"^(?P<part1>\d{4})[-\ ]?(?P<part2>\d{4})[-\ ]?(?P<part3>\d{4})$")

class INAadhaarNumberField(CharField):
    """
    A form field for Aadhaar number issued by Unique Identification Authority of India (UIDAI).
    Checks the following rules to determine whether the number is valid:
        * Conforms to the XXXX XXXX XXXX format.
        * No group consists entirely of zeroes.
    Important information:
        * Aadhaar number is a proof of identity but not of citizenship.
        * Aadhaar number is issued to every resident of India including
          foreign citizens.
        * Aadhaar number is not mandatory.
    More information can be found at
    http://uidai.gov.in/what-is-aadhaar-number.html
    """

    ''' default_error_messages = {
        'invalid': _('Enter a valid Aadhaar number in XXXX XXXX XXXX or '
                     'XXXX-XXXX-XXXX format.'),
    }'''
    
    def clean(self, value):
        #value = super().clean(value)
        if value in self.empty_values:
            return value

        match = re.match(aadhaar_re, value)
        if not match:
            raise ValidationError(self.error_messages['invalid'], code='invalid')
        part1, part2, part3 = match.groupdict()['part1'], match.groupdict()['part2'], match.groupdict()['part3']

        # all the parts can't be zero
        if part1 == '0000' and part2 == '0000' and part3 == '0000':
            raise ValidationError(self.error_messages['invalid'], code='invalid')

        return '%s%s%s' % (part1, part2, part3)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        


class UserUpdateForm(forms.ModelForm):
    try:
        email= User.objects.filter(is_active=True,).values_list('email', flat=False)
    except:
        email=forms.EmailField()
        
    
    
    #print(email)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True

        


class ProfileUpdateForm(forms.ModelForm):
    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    )
    #select_state=INStateSelect(attrs={'placeholder':'ha'})
    aadharno=INAadhaarNumberField(widget=forms.TextInput())
    city = forms.CharField()
    county = forms.ChoiceField(widget=forms.Select, choices=STATE_CHOICES)
    postal_code = INZipCodeField(widget=forms.TextInput(attrs={'placeholder': 'Update your postal code...'}) )
    

    
    class Meta:
        model = Profile
        fields = ['image','address_1', 'address_2', 'aadharno','city', 'county',
                  'postal_code']
