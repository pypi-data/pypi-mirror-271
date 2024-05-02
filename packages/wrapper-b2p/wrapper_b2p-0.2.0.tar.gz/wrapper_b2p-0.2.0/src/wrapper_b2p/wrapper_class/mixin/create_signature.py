import base64
import hashlib


class MixinCreateSignature:
    def _create_signature(self):
        signature_raw = self._get_raw_signature()
        signature_md5 = hashlib.md5(signature_raw.encode('utf8')).digest()
        signature_md5_hex = signature_md5.hex()
        signature = base64.b64encode(signature_md5_hex.encode())
        return signature.decode()

    def _get_raw_signature(self) -> str:
        raise NotImplementedError(f'Definition "_get_raw_signature" in {self.__class__.__name__}.')
