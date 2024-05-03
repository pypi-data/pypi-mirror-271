__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import ragfmk.utils.CONST as C
import json
from numpyencoder import NumpyEncoder
from ragfmk.interfaces.IEmbeddings import IEmbeddings

"""
        Embeddings and data are stored in Python list/JSON and used with the following format :
        {0: {'text': 'The prompt or text', 
             'embedding': array([-6.65125623e-02,  ..., -1.22626998e-01]) 
            },
        1: {'text': '...',  'embedding': array([...]) },
        ...
        }
"""

class embeddings(IEmbeddings):
    def __init__(self):
        self.__content = {}

    @property
    def content(self) -> str: 
        return self.__content
    
    @property
    def jsonContent(self) -> str: 
        return json.dumps(self.__content, cls=NumpyEncoder)
    @jsonContent.setter
    def jsonContent(self, content):
        try:
            self.__content = json.loads(content)
        except Exception as e:
            self.items = {}
            raise

    @property
    def size(self):
        return len(self.__content)
        
    def encode(self, cks):
        """ to surcharge with the embeddings class
        Args:
            cks (chunks): list of chunks to embed
        Returns:
            json: vector embeddings
        """
        return None

    def __wrap(self, vectAndData):
        """ Wrap the Dataframe into a list (to have a json later)
        The Dataframe contains 2 columns: 
            1) text : with the data
            2) embedding: with the vector/embeddings calculated (as a nparray)
        Args:
            vectAndData (Dataframe): Data and embeddings
        Returns:
            {}: list for a later JSON conversion
        """
        self.__content = {}
        for i, (chunk, vector) in enumerate(vectAndData):
            line = {}
            line[C.JST_TEXT] = chunk
            line[C.JST_EMBEDDINGS] = vector
            self.__content[i] = line

    def create(self, cks) -> bool:
        """ Calculate the embeddings for list of chunks
        Args:
            cks (chunks):  chunks object
        Returns:
            str: json with data and embeddings for all chunks
        """
        try: 
            vect = self.encode(cks)
            vectAndData = zip(cks.items, vect)
            self.__wrap(vectAndData)
            return True
        except Exception as e:
            return False
        
    def save(self, filename) -> bool:
        """ Save the chunks in a file.
        Args:
            filename (_type_): JSON chunks file
        Returns:
            bool: True if ok
        """
        try:
            with open(filename, "w", encoding=C.ENCODING) as f:
                f.write(self.jsonContent)
            return True
        except Exception as e:
            return False

    def load(self, filename = "", content = "") -> bool:
        """ Load and build a chunk file (can be loaded from a json file or a json content). 
            Format required : Content = {"chunks": [..., ...] }
        Args:
            filename (str, optional): JSON chunks file. Defaults to "".
            content (str, optional): JSON chunks content. Defaults to "".
        Returns:
            bool: True if ok
        """
        try:
            self.__content = {}
            if (len(filename) >0):
                with open(filename, "r", encoding=C.ENCODING) as f:
                    self.__content = json.load(f)
            elif (len(content) >0):
                self.__content = content
            else:
                return False
            return True
        except Exception as e:
            return False