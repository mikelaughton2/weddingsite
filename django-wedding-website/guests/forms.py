from django import forms

class ConfirmForm(forms.Form):
    do_it = forms.BooleanField(required=True)
