from django import forms

class RescheduleRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label='Reason / Preferred Time')
    # appointment_id = forms.IntegerField(widget=forms.HiddenInput())