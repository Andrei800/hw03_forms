from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from posts.models import Post
from .models import Contact


User = get_user_model()


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'body')


    def clean_subject(self):
        data = self.cleaned_data['subject']
        if 'спасибо' not in data.lower():
            raise forms.ValidationError('Вы обязательно должны нас поблагодарить!')
        return data 


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ( 'text' , 'group')



