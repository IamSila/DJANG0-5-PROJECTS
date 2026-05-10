from django import forms
from .models import Trainer

#  form to add members to the db
class AddMemberForm(forms.Form):
    pass

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
class ImportForm(forms.Form):
    file = forms.FileField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply to a specific field
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
