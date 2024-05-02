from .b2p_abc import Best2PayABC
from ..mixin import MixinRequestPostB2P


class RequestB2PABC(MixinRequestPostB2P, Best2PayABC):
    pass
