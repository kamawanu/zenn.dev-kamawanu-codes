from typing import List
from django.forms.forms import Form
from exmodel import CommentForm, HelpTextContactForm
import pprint
from mergeform import mergeform

aa = CommentForm()
bb = HelpTextContactForm()

inject = {
    "name": "*name",
    "subject": "*subject",
}

form0 = mergeform(inject, nested=[aa, bb])
form0.is_valid()
pprint.pprint(form0)
pprint.pprint(aa)
pprint.pprint(bb)
###breakpoint()
