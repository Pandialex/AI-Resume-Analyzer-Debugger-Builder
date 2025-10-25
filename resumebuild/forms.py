# forms.py
from django import forms

class ResumeForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    summary = forms.CharField(widget=forms.Textarea)
    skills = forms.CharField(widget=forms.Textarea)
    experience = forms.CharField(widget=forms.Textarea)
    education = forms.CharField(widget=forms.Textarea)
