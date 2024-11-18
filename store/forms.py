from django import forms

class OrderForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True, label="Full Name")
    address = forms.CharField(widget=forms.Textarea, required=True, label="Shipping Address")
    phone = forms.CharField(max_length=15, required=True, label="Phone Number")
    email = forms.EmailField(required=True, label="Email")
