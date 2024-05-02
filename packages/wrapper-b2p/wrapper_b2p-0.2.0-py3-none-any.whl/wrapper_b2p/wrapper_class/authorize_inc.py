from typing import Union, Optional, Any

from ..constant import RUB
from .class_abs import RequestB2PABC


class AuthorizeInc(RequestB2PABC):
    path_to_point_api = 'AuthorizeInc'
    allowed_field_with_default_value_to_b2p = {
        'fee': 0,
        'is_prod_stand': False,
        'stand_url': None,
    }

    def __init__(self, sector: int, id_: Union[str, int], amount: int, b2p_token: str,
                 currency: str = RUB, **kwargs: Optional[Any]):
        self.sector = sector
        self.id = id_
        self.amount = amount
        self.currency = currency
        self.b2p_token = b2p_token
        for item in self.allowed_field_with_default_value_to_b2p:
            setattr(self, item, kwargs.get(item) or self.allowed_field_with_default_value_to_b2p.get(item))
        self.signature = self._create_signature()

    def do(self) -> dict:
        return self._request_best2pay()

    def _get_raw_signature(self) -> str:
        if hasattr(self, 'fee') and self.fee:
            return (str(self.sector) + str(self.id) + str(self.amount) +
                    str(self.fee) + str(self.currency) + self.b2p_token)
        return str(self.sector) + str(self.id) + str(self.amount) + str(self.currency) + self.b2p_token
