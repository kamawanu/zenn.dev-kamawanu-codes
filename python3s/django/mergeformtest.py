import pprint
from mergeform import mergeform
from stubdjango.stubmodel import CommentForm,HelpTextContactForm

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
