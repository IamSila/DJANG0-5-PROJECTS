from django import forms
from .models import Csv
import os

class CsvFileForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('file_name', 'activated')  # Include all fields you want editable
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only add class - DON'T override widget type
        self.fields['file_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['activated'].widget.attrs.update({'class': 'form-check-input'})
    
    def clean_file_name(self):
        file = self.cleaned_data.get('file_name')
        
        if not file:
            raise forms.ValidationError('Please select a file')
        
        # Check file extension
        valid_extensions = ['.csv', '.xlsx', '.json']
        ext = os.path.splitext(file.name)[1].lower()
        
        if ext not in valid_extensions:
            raise forms.ValidationError(
                f'Invalid file type. Allowed: {", ".join(valid_extensions)}'
            )
        
        # Check file size (5MB max)
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File too large. Max 5MB')
        return file