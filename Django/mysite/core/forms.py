from django import forms

from .models import StudyGroup


class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ('field','title', 'content', 'author', 'image')
