from django.contrib.auth.models import User
from django import forms
from django.urls import reverse_lazy

from rango.models import Page, Category
from rango.models import UserProfile
from rango.models import Submission
from rango.models import CPU, CPU_Family
from rango.models import Feedback


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=Category.NAME_MAX_LEN, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # Inline class to provide additional info on the form
    class Meta:
        # assoc ModelForm and a model
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=Page.TITLE_MAX_LEN, help_text="Please enter the title of the page.")
    url = forms.URLField(
        max_length=Page.URL_MAX_LEN, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        # define what keys to include  with fields, or define what we do not want via exclude
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)


# form for accepting submitted code
class SubmissionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 130, 'class': 'form-control'}), label='Title')
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 130, 'class': 'form-control'}), label='Paste your code here')
    cpu_family = forms.ModelChoiceField(queryset=CPU_Family.objects.all(), empty_label="---Please Select---", label="CPU Family")
    cpu = forms.ModelChoiceField(queryset=CPU.objects.all(), label="CPU")
    result = forms.CharField(widget=forms.HiddenInput(), initial="Pending")

    class Meta:
        model = Submission
        fields = ('title', 'content', 'result')


# for instructor to write a feedback
class FeedbackForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 130, 'class': 'form-control'}), label='')

    class Meta:
        model = Feedback
        fields = ('content',)
