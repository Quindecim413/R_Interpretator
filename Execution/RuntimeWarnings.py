import warnings
from abc import abstractmethod


class BaseWarn(Warning):
    @abstractmethod
    def warn(self):
        pass

class NumberOfReplacingItemsIsNotMultipleOfReplacement(BaseWarn):
    def warn(self):
        warnings.warn('number of items to replace is not a multiple of replacement length',
                      NumberOfReplacingItemsIsNotMultipleOfReplacement)
