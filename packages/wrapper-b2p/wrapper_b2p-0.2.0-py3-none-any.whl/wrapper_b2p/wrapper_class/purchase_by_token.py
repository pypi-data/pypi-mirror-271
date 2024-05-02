from typing import Union, Optional, Any

from .class_abs import RequestB2PABC


class PurchaseByToken(RequestB2PABC):
    path_to_point_api = 'PurchaseByToken'
    allowed_field_with_default_value_to_b2p = {
        'cvc': '',
        'is_prod_stand': False,
        'stand_url': None,
    }

    def __init__(self, sector: str, id_: Union[str, int], token: str, b2p_token: str, **kwargs: Optional[Any]):
        self.sector = sector
        self.id = id_
        self.token = token
        self.b2p_token = b2p_token
        for item in self.allowed_field_with_default_value_to_b2p:
            setattr(self, item, kwargs.get(item) or self.allowed_field_with_default_value_to_b2p.get(item))
        self.signature = self._create_signature()

    def _get_raw_signature(self) -> str:
        return str(self.sector) + str(self.id) + str(self.token) + self.b2p_token

    def do(self):
        return self._request_best2pay()
