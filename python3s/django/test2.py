import pprint
from stubdjango.stubmodel import CommentForm,HelpTextContactForm
from variantformset import variantformset

inject = {
    "form-0-name": "*name",
    "form-1-subject": "*subject",
    "form-0-comment": "*comment",
    "form-1-message": "*message",
}

form0 = variantformset(inject,forms=[CommentForm,HelpTextContactForm])
print(form0)
####breakpoint()
form0.full_clean()
print(form0)
###print(vars(form0.forms[0]))
###print(vars(form0.forms[1]))
assert form0.is_valid() #, breakpoint()
pprint.pprint(form0)
pprint.pprint(form0.cleaned_data)
# breakpoint()
