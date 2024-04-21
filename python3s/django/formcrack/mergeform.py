from typing import List
from django.forms import Form


class mergeform(Form):
    _nested:List[Form] = None

    def __init__(self, *args, nested:List[Form], **kwargs):
        self._nested = nested
        ###breakpoint()
        super().__init__(*args, **kwargs)
        flds = {}
        for zz in self._nested:
            flds.update(zz.base_fields)
        self.fields = flds

    def is_valid(self) -> bool:
        if not self.is_bound:
            return False
        e = {}
        for zz in self._nested:
            zz.data = self.data
            zz.is_bound = True
            zz.cleaned_data = None
            zz.full_clean()
            if zz.is_valid():
                zz._clean_form()
            e.update(zz._errors)
        self._errors = e
        return not self._errors

    @property
    def cleaned_data(self):
        r = {}
        for zz in self._nested:
            r.update(zz.cleaned_data or {})
        return r
