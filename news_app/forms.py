from django  import forms
from .models import Contact


class ContactForm(forms.ModelForm): #bu ModelForm class orqali contact formani ishlatishimiz mumkin

    class Meta:
        model = Contact
        fields = "__all__" # Contact modelidagi barcha fieldlarni formaga chiqaradi



# class SubscriptionForm(forms.Form): #bu Form class orqali subscription formani ishlatishimiz mumkin
#     subject = forms.CharField(max_length=100)
#     message = forms.CharField()
#     email = forms.EmailField()
