from django import forms
from .models import orders


class orderform(forms.ModelForm):
    states =[('AP','Ahdra Pradesh'),('Gj','Gujarat'),('MH','Maharastra'),('AS','Assam'),('RJ','Rajasthan'),('MP','Madhya Pradesh')]
    name =forms.CharField(max_length=50,widget=forms.TextInput())
    phone = forms.CharField(max_length=50,widget=forms.TextInput())
    email= forms.CharField(max_length=50,widget=forms.TextInput())
    address= forms.CharField(max_length=200,widget=forms.TextInput())
    country = forms.CharField(max_length=50,widget=forms.TextInput())
    state = forms.ChoiceField(choices=states,widget=forms.TextInput())
    city = forms.CharField(max_length=50,widget=forms.TextInput())

    class Meta:
        model = orders
        fields =['name','phone','email','address','country','state']