from .b2p_abc import Best2PayABC
from ...exception import ErrorPayerIDNotExist


class RedirectB2PABC(Best2PayABC):

    def do(self) -> str:
        return f'{self._get_url_b2p()}/{self.path_to_point_api}?{self._get_params()}'

    def _get_raw_signature(self):
        if self.save_card and not self.payer_id:
            raise ErrorPayerIDNotExist()

        if getattr(self, 'save_card', False):
            return str(self.sector) + str(self.id) + str(self.payer_id) + self.b2p_token
        return str(self.sector) + str(self.id) + self.b2p_token

    def _get_params(self) -> str:
        return '&'.join([f'{item}={getattr(self, item)}' for item in self.__dict__
                         if getattr(self, item) and (item not in ['is_prod_stand', 'b2p_token'])])
