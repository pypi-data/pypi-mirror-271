from typing import Optional, Any

from ..constant import RUB
from .class_abs import RequestB2PABC


class Register(RequestB2PABC):
    path_to_point_api = 'Register'
    allowed_field_with_default_value_to_b2p = {
        'fee': 0,
        'url': '',
        'failurl': '',
        'currency': RUB,
        'lang': 'RU',
        'is_prod_stand': False,
        'stand_url': None,
    }

    def __init__(self, sector: str, amount: int, description: str, b2p_token: str, **kwargs: Optional[Any]):
        self.sector = sector
        self.amount = amount
        self.description = description
        self.b2p_token = b2p_token
        for item in self.allowed_field_with_default_value_to_b2p:
            setattr(self, item, kwargs.get(item) or self.allowed_field_with_default_value_to_b2p.get(item))
        self.signature = self._create_signature()

    def do(self) -> dict:
        return self._request_best2pay()

    def _get_raw_signature(self) -> str:
        return str(self.sector) + str(self.amount) + str(self.currency) + self.b2p_token
