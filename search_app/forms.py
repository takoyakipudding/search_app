from django import forms 
from .models import Product 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

 
class SearchForm(forms.Form): 
    query = forms.CharField( 
        label='検索キーワード', 
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'})    
    ) 
 
class ProductForm(forms.ModelForm): 
    class Meta: 
        model = Product 
        fields = ['name', 'description', 'price', 'category']
        
        
        

