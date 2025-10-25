from django import forms

class ResumeUploadForm(forms.Form):
    resume = forms.FileField(
        label="Upload Resume",
        help_text="Supported formats: PDF, DOCX, TXT",
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.docx,.txt',
            'class': 'file-input'
        })
    )
    job_desc = forms.CharField(
        label="Job Description",
        help_text="Paste the job description you're applying for",
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Paste the job description here...',
            'class': 'form-textarea'
        })
    )