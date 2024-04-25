from django import forms
from .models import Debt

class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = "__all__"
        #fields = ('DcID', 'UserName', 'Record', 'Account', 'PokerID', 'PokerID2', 'Total')

        Widgets = {
            'DcID': forms.TextInput(attrs={'class': 'form-control'}),
            'UserName': forms.TextInput(attrs={'class': 'form-control'}),
            'Record': forms.TextInput(attrs={'class': 'form-control'}),
            'Account': forms.TextInput(attrs={'class': 'form-control'}),
            'PokerID': forms.TextInput(attrs={'class': 'form-control'}),
            'PokerID2': forms.TextInput(attrs={'class': 'form-control'}),
            'Total': forms.NumberInput(attrs={'class': 'form-control'}),
        }

