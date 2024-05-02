from copy import copy

import requests
import xmltodict
from requests import RequestException

from ... import exception
from ...constant import MAX_COUNT_REQUEST_B2P


class MixinRequestPostB2P:
    def _request_best2pay(self) -> dict:

        count_request_to_b2p = 1
        while True:
            try:
                res = requests.post(f'{self._get_url_b2p()}/{self.path_to_point_api}',
                                    data=self._get_date_by_send_b2p())
            except RequestException as err:
                if count_request_to_b2p < MAX_COUNT_REQUEST_B2P:
                    count_request_to_b2p += 1
                    continue
                raise exception.ErrorConnectB2P() from err
            res_dict = self._parser_xml_to_dict(res.text)
            return res_dict

    @staticmethod
    def _parser_xml_to_dict(text: str) -> dict:
        res_dict = xmltodict.parse(text, process_namespaces=True)
        return res_dict

    def _get_date_by_send_b2p(self) -> dict:
        data = copy(self.__dict__)
        data.pop('is_prod_stand')
        data.pop('b2p_token')
        data.pop('stand_url')
        return data
