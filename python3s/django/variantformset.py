import dataclasses
from typing import Any, Type
from django.forms.formsets import BaseFormSet, TOTAL_FORM_COUNT, INITIAL_FORM_COUNT
from django.forms.forms import Form


@dataclasses.dataclass
class stubmanagementform:
    parent: "variantformset"

    def is_valid(self):
        return True

    @property
    def cleaned_data(self):
        return {
            # TOTAL_FORM_COUNT: len(self.parent.baseforms_),
            # INITIAL_FORM_COUNT: len(self.parent.baseforms_),
        }


class variantformset(BaseFormSet):
    baseforms_: list[Type[Form]]
    form_renderer = None
    renderer = None
    selected: int = None
    stubmanage_: bool

    can_order = False
    can_delete = False
    max_num = None
    validate_max = False
    min_num = None
    validate_min = False
    # absolute_max=None
    can_delete_extra = True
    renderer = None

    @property
    def absolute_max(self):
        return len(self.baseforms_)

    @property
    def management_form(self) -> Any:
        return stubmanagementform(self) if self.stubmanage_ else super().management_form

    def total_form_count(self) -> int:
        return len(self.baseforms_)

    initial_form_count = total_form_count

    def __init__(self, data: dict[str, Any], *, stubmanage=True, forms: list[Form], **kwargs):
        self.baseforms_ = forms
        self.stubmanage_ = stubmanage
        super().__init__(data, **kwargs)

    def _construct_form(self, i, **kwargs):
        self.selected = i
        form = super()._construct_form(i, **kwargs)
        self.selected = None
        return form

    @property
    def form(self):
        return self.baseforms_[self.selected]
