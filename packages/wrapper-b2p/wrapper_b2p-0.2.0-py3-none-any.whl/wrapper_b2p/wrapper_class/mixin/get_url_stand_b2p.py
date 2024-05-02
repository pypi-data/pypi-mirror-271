from ... import settings


class MixinGetURLStandB2P:
    is_prod_stand = False
    stand_url = None

    def _get_url_b2p(self) -> str:
        if self.stand_url:
            return self.stand_url

        if self.is_prod_stand:
            return settings.URL_PROD_STAND
        return settings.URL_TEST_STAND
