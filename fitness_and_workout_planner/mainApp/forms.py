from django import forms
from .models import Trainer, Member

# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['member_id', 'name', 'email', 'phone', 'membership', 'join_date', 'status']
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'member_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., MEM001'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
            'membership': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_phone(self):
        """Clean and validate phone number"""
        phone = self.cleaned_data.get('phone')
        
        # Remove any non-digit characters
        cleaned_phone = ''.join(filter(str.isdigit, phone))
        
        # Check if it's exactly 10 digits
        if len(cleaned_phone) != 10:
            raise ValidationError('Phone number must be exactly 10 digits.')
        
        return cleaned_phone
    
    def clean_member_id(self):
        """Ensure member_id is unique and properly formatted"""
        member_id = self.cleaned_data.get('member_id')
        member_id = member_id.upper().strip()
        
        # Check for existing member_id except current instance
        if Member.objects.filter(member_id=member_id).exists():
            if self.instance and self.instance.member_id != member_id:
                raise ValidationError('Member ID already exists.')
            elif not self.instance:
                raise ValidationError('Member ID already exists.')
        
        return member_id

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'specialization', 'email', 'phone', 'status', 
                  'bio', 'years_of_experience', 'certifications', 'hire_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Yoga, Cardio, Strength'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'trainer@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'certifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }





FORMAT_CHOICES = (
    ('xls', 'xlsx'),
    ('csv', 'csv'),
    ('json', 'json')
)

class FormatForm(forms.Form):
    format = forms.ChoiceField(label="format", choices=FORMAT_CHOICES)

# upload form for member import
class ImportForm(forms.ModelForm):
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply to a specific field
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
