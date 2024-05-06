__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from abc import ABC, abstractmethod

class IEmbeddings(ABC):
    
    @property
    def content(self): 
        pass
    
    @property
    @abstractmethod
    def jsonContent(self):
        pass
    @jsonContent.setter
    def jsonContent(self, content):
        pass
    
    @property
    @abstractmethod
    def size(self):
        pass
    
    @abstractmethod
    def encode(self, cks):
        pass
    
    @abstractmethod
    def create(self, cks):
        pass
    
    @abstractmethod
    def save(self, filename):
        pass
    
    @abstractmethod
    def load(self, filename = "", content = ""):
        pass