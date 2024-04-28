import pprint
from stubdjango.stubmodel import CommentForm,HelpTextContactForm
from variantformset import variantformset

inject = {
    "form-MIN_NUM_FORMS": 2,
    "form-MAX_NUM_FORMS": 2,
    "form-INITIAL_FORMS": 2,
    "form-TOTAL_FORMS": 2,
    "form-0-name": "*name",
    "form-1-subject": "*subject",
    "form-0-comment": "*comment",
    "form-1-message": "*message",
}

form0 = variantformset(inject,stubmanage=False,forms=[CommentForm,HelpTextContactForm])
print(form0)
####breakpoint()
form0.full_clean()
print(vars(form0.management_form))
##print(form0.management_form)
#print(form0)
###print(vars(form0.forms[0]))
###print(vars(form0.forms[1]))
assert form0.is_valid() #, breakpoint()
pprint.pprint(form0)
pprint.pprint(form0.cleaned_data)
# breakpoint()
