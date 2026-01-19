from django import forms
from ckeditor.widgets import CKEditorWidget  # ✅ import this

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class EmailForm(forms.Form):
    sender = forms.EmailField(label="Sender Email")
    to = forms.CharField(label="Receiver Email(s)")
    cc = forms.CharField(label="CC (comma separated, optional)", required=False)
    subject = forms.CharField(label="Subject")
    body = forms.CharField(widget=CKEditorWidget(), label="Body")  # ✅ Rich text editor
    attachments = forms.FileField(
        required=False,
        widget=MultiFileInput(attrs={'multiple': True})
    )
