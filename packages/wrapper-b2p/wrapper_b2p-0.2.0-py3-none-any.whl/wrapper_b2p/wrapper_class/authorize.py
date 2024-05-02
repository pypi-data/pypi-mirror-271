from typing import Union, Optional, Any

from .class_abs import RedirectB2PABC


class Authorize(RedirectB2PABC):
    path_to_point_api = 'Authorize'

    allowed_field_with_default_value_to_b2p = {
        'get_token': 0,
        'token': False,
        'payer_id': False,
        'save_card': False,
        'is_prod_stand': False,
        'stand_url': None,
    }

    def __init__(self, sector: str, id_: Union[str, int], b2p_token: str, **kwargs: Optional[Any]):
        self.sector = sector
        self.id = id_
        self.b2p_token = b2p_token
        for item in self.allowed_field_with_default_value_to_b2p:
            setattr(self, item, kwargs.get(item) or self.allowed_field_with_default_value_to_b2p.get(item))
        self.signature = self._create_signature()
