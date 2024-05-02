import base64
import hashlib
from typing import Union, Optional, Any

from .class_abs import RequestB2PABC
from ..exception import ErrorDefined


class Order(RequestB2PABC):
    path_to_point_api = 'Order'
    allowed_field_with_default_value_to_b2p = {
        'mode': 0,
        'get_token': 0,
        'is_prod_stand': False,
        'stand_url': None,
    }

    def __init__(self, sector: Union[str, int], b2p_token: str, id_: Union[str, int] = None,
                 reference: Union[str, int] = None, **kwargs: Optional[Any]):
        self.sector = sector
        self.id = id_
        self.reference = reference
        if not any([self.id, self.reference]):
            raise ErrorDefined()
        self.b2p_token = b2p_token
        for item in self.allowed_field_with_default_value_to_b2p:
            setattr(self, item, kwargs.get(item) or self.allowed_field_with_default_value_to_b2p.get(item))
        self.signature = self._create_signature()

    def do(self):
        return self._request_best2pay()

    def _create_signature(self):
        signature_raw = self._get_raw_signature()
        md5 = hashlib.md5(signature_raw.encode('utf8')).digest()
        md5_hex = md5.hex()
        signature = base64.b64encode(md5_hex.encode())
        return signature.decode()

    def _get_raw_signature(self) -> str:
        if self.id:
            return str(self.sector) + str(self.id) + self.b2p_token
        return str(self.sector) + str(self.reference) + self.b2p_token

    def _get_date_by_send_b2p(self) -> dict:
        data = super()._get_date_by_send_b2p()
        if self.id is None:
            data.pop('id')
        if self.reference is None:
            data.pop('reference')
        return data
