from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        widgets = {
            'content': forms.TextInput(attrs={'size': 120}),
            'content': forms.Textarea(attrs={'rows':4, 'cols':120}),
            'device_type': forms.TextInput(attrs={'size': 10}),
        }