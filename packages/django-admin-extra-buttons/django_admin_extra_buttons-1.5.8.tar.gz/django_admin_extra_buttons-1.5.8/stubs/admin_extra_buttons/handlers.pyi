from .buttons import Button as Button, ChoiceButton as ChoiceButton, LinkButton as LinkButton
from .utils import HttpResponseRedirectToReferrer as HttpResponseRedirectToReferrer, check_permission as check_permission, handle_basic_auth as handle_basic_auth, labelize as labelize
from _typeshed import Incomplete

class BaseExtraHandler:
    func: Incomplete
    config: Incomplete
    model_admin: Incomplete
    decorators: Incomplete
    login_required: Incomplete
    permission: Incomplete
    sig: Incomplete
    def __init__(self, func, **kwargs) -> None: ...
    def func_args(self): ...
    def get_instance(self, model_admin): ...
    def name(self): ...
    def __call__(self, model_admin, request, *args, **kwargs): ...

class ViewHandler(BaseExtraHandler):
    login_required: Incomplete
    http_auth_handler: Incomplete
    http_basic_auth: Incomplete
    def __init__(self, func, login_required: bool = True, http_basic_auth: bool = False, http_auth_handler: Incomplete | None = None, **kwargs) -> None: ...
    model_admin: Incomplete
    def __call__(self, model_admin, request, *args, **kwargs): ...
    def url_pattern(self): ...

class ButtonMixin:
    change_form: Incomplete
    change_list: Incomplete
    visible: Incomplete
    enabled: Incomplete
    html_attrs: Incomplete
    def __init__(self, func, html_attrs: Incomplete | None = None, change_list: Incomplete | None = None, change_form: Incomplete | None = None, visible: bool = True, enabled: bool = True, **kwargs) -> None: ...
    def get_button_params(self, context, **extra): ...
    def get_button(self, context): ...

class ButtonHandler(ButtonMixin, ViewHandler):
    button_class = Button

class LinkHandler(ButtonMixin, BaseExtraHandler):
    button_class = LinkButton
    url_pattern: Incomplete
    href: Incomplete
    def __init__(self, func, **kwargs) -> None: ...
    def get_button_params(self, context, **extra): ...
    def get_button(self, context): ...

class ChoiceHandler(LinkHandler):
    button_class = ChoiceButton
    href: Incomplete
    choices: Incomplete
    selected_choice: Incomplete
    def __init__(self, func, **kwargs) -> None: ...
    def get_button_params(self, context, **extra): ...
