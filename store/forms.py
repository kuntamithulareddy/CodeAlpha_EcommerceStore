from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=160, widget=forms.TextInput(attrs={"placeholder": "Full name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email address"}))
    address = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "House number, street and area", "rows": 3}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "City"}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"placeholder": "PIN code"}))
