from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=200)

    class Meta:
        model = Item
        fields = ('name', 'emailid', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
