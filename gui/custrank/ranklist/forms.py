from django import forms

class add(forms.Form):  
    Username = forms.CharField(label='Username :')

class hidden(forms.Form):
    hidden_field = forms.CharField(widget=forms.HiddenInput())