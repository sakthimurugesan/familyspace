from django import forms
import users.models
class MyForm(forms.Form):
    user=users.models.User
    choices=[('all','all')]
    for i in user.objects.values_list('name'):
        for j in i:
            l=[]
            l.append(j)
            l.append(j)
            choices.append(tuple(l))
    towhom=forms.ChoiceField(choices=choices)

user=users.models.User
print(user.objects.values_list('name'))

