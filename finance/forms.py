from django import forms


class Finance(forms.Form):
    symbol = forms.CharField(label="Please enter a symbol:")
