# coding : utf-8
from django import forms


class WellnessForm(forms.Form):
    humeur = forms.IntegerField()
    sommeil = forms.IntegerField()
    musculaire = forms.IntegerField()
    stress = forms.IntegerField()
    fatigue = forms.IntegerField()
