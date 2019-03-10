from django import forms

class tform(forms.Form):
    artist = forms.CharField(label='Artist', max_length=100)
    song = forms.CharField(label='Song', max_length=100)
