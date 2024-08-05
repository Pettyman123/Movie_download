from django import forms

class MovieSearchForm(forms.Form):
    movie_name = forms.CharField(label='Movie Name', max_length=100)
