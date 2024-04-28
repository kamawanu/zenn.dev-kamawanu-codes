from django import forms


class CommentForm(forms.Form):
    name = forms.CharField()
    # url = forms.URLField()
    comment = forms.CharField()


class HelpTextContactForm(forms.Form):
    subject = forms.CharField(max_length=100, help_text="100 characters max.")
    message = forms.CharField()
    #comment = forms.CharField()
