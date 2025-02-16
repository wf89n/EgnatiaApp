from django import forms
from .models import BasicInfo

class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = BasicInfo
        fields = '__all__'  # or specify a list of fields
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hiring_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_exams_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_exams_renewal_date': forms.DateInput(attrs={'type': 'date'}),
            'safety_passport_date': forms.DateInput(attrs={'type': 'date'}),
            'safety_passport_renewal_date': forms.DateInput(attrs={'type': 'date'}),
            'termination_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        required_fields = [
            'first_name', 'last_name', 'father_name', 'location', 'gender', 'marital_status',
            'date_of_birth', 'mobile_phone', 'email', 'tax_id', 'address'
        ]
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, f'{field.replace("_", " ").capitalize()} is required.')
        return cleaned_data
