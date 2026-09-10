from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "message": forms.Textarea(attrs={"placeholder": "Tell me what you would like to build or discuss.", "rows": 5}),
        }
