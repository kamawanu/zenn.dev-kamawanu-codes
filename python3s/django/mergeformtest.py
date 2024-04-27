import pprint
from mergeform import mergeform
from django import forms


class CommentForm(forms.Form):
    name = forms.CharField()
    # url = forms.URLField()
    comment = forms.CharField()


class HelpTextContactForm(forms.Form):
    subject = forms.CharField(max_length=100, help_text="100 characters max.")
    message = forms.CharField()
    # sender = forms.EmailField(help_text="A valid email address, please.")
    # cc_myself = forms.BooleanField(required=False)


aa = CommentForm()
bb = HelpTextContactForm()

inject = {
    "name": "*name",
    "subject": "*subject",
    "comment": "*comment",
    "message": "*message",
}

form0 = mergeform(inject, nested=[aa, bb])
form0.is_valid()
pprint.pprint(form0)
pprint.pprint(form0.cleaned_data)
pprint.pprint(aa)
pprint.pprint(aa.cleaned_data)
pprint.pprint(bb)
pprint.pprint(bb.cleaned_data)
# breakpoint()
