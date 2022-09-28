from django import forms




class Scraping (forms.Form):
        subject=forms.CharField( widget=forms.widgets.TextInput(attrs={'class': 'inputSuj'}),
                     )