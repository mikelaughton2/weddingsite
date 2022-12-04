from django import forms

class ConfirmForm(forms.Form):
    do_it = forms.BooleanField(required=False)
    test_only = forms.BooleanField(required=False)
    mark_sent = forms.BooleanField(required=False)
