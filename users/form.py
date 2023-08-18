from django import forms
class MyForm(forms.Form):
    gender=forms.ChoiceField(choices=[
        ('male','male'),
        ('female','female'),
        ])
    
    blood=forms.ChoiceField(choices=[
        ('a+ve','a+ve'),
        ('a1+ve','a1+ve'),
        ('a2+ve','a2+ve'),
        ])
    
    
    