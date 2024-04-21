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
pprint.pprint(form0.cleaned_data)
pprint.pprint(aa)
pprint.pprint(aa.cleaned_data)
pprint.pprint(bb)
pprint.pprint(bb.cleaned_data)
###breakpoint()
