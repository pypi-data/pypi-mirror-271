from abc import ABC

from ..mixin import MixinGetURLStandB2P, MixinCreateSignature


class Best2PayABC(MixinGetURLStandB2P, MixinCreateSignature, ABC):
    def do(self):
        raise NotImplementedError('Definition "do" in {self.__class__.__name__}.')
