from django import forms
from .models import Records

class RecordsForm(forms.ModelForm):
    class Meta:
        model = Records
        fields = "__all__"

        Widgets = {
            'DcID': forms.TextInput(attrs={'class': 'form-control'}),
            'UserName': forms.TextInput(attrs={'class': 'form-control'}),
            'Record': forms.TextInput(attrs={'class': 'form-control'}),
            'Account': forms.TextInput(attrs={'class': 'form-control'}),
            'PokerID': forms.TextInput(attrs={'class': 'form-control'}),
            'Total': forms.NumberInput(attrs={'class': 'form-control'}),
            'WOL': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'Balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }

