from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Type
from habanero import cn
from requests import HTTPError
from .library import EntrySplitter
import re
import warnings
import six

# When working with `venv`, to get pylance to work:
# You have to choose the correct interpreter.
# Use shortcuts "Ctrl+Shift+P" and type "Python: Select Interperter" to choose the venv.

@six.add_metaclass(ABCMeta)
class Query:
    def __init__(self, id: Type[str]) -> None:
        self.success = True
        self.id = self._handleId(id)
        self.type = self._handleType()
        self.result = self._handleResult()
        self.block = self._handleBlock() 

    def _fail(self, result):
        self.success = False
        self.result = result

    def _handleId(self, id):
        try:
            return self._id(id)
        except TypeError as e:
            self._fail(e)
        return None

    @staticmethod
    def _id(id):
        if isinstance(id, str):
            return id
        elif isinstance(id, list) and all(isinstance(i, str) for i in id):
            warnings.warn("ID is a list of strings. Using the first element.")
            return id[0]
        else:
            raise TypeError("ID must be a string or a list of strings")

    def _handleType(self):
        if not self.success:
            return None
        try:
            return self._type(self.id)
        except ValueError as e:
            self._fail(e)
        return None

    @staticmethod
    def _type(id):
        for reid in ReID:
            if re.match(reid.value, id, flags=re.I):
                return reid.name
        raise ValueError("ID is not a valid article identifier")

    def _handleResult(self):
        if not self.success:
            return self.result
        try:
            return self._result(self.id)
        except HTTPError:
            error = f"Unable to find {self.id}"
            self._fail(error)
        except ValueError as e:
            self._fail(e)
        except TypeError as e:
            self._fail(e)
        except:
            raise
        return self.result

    @abstractmethod
    def _result(id):
        pass

    def _handleBlock(self):
        if self.success:
           block = EntrySplitter(self.result).split()
           self.result = f"Found {self.type} {self.id}"
           return block
        return None

class ReID(Enum):
    DOI = r"^10\.\d{4,9}\/[-._;()/:A-Z0-9]+$"
    PMID = r"^\d+$"

# https://www.crossref.org/blog/dois-and-matching-regular-expressions/
# Need to review to learn and consolidate.
# When to use static methods?

# consider allowing different urls/formats for cn.contentnegotiation
class CrossRef(Query):

    @staticmethod
    def _result(id):
        try:
            return cn.content_negotiation(id, format='bibtex', url="https://doi.org")
        except:
            raise