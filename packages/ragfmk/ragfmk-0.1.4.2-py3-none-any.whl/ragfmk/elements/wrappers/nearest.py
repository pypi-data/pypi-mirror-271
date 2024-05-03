__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import ragfmk.utils.CONST as C
import json
from numpyencoder import NumpyEncoder
from ragfmk.interfaces.INearest import INearest

""" Manages the Chunks file structure (JSON)
    Content = {"chunks": [..., ...] }
"""

class nearest(INearest):
    def __init__(self):
        self.__items = [] # simple Array which contains all the items
        self.__distances = [] # list of distances per items
        
    @property
    def items(self): 
        return self.__items 
    @items.setter
    def items(self, q):
        self.__items = q
    def __getitem__(self, item):
        """ Makes the Data column accessible via [] array
            example: df['colName']
        Args:
            item (str): attribute/column name
        Returns:
            object: data
        """
        return self.__items.__getitem__(item)
    
    @property
    def distances(self): 
        return self.__distances 
    @distances.setter
    def distances(self, q):
        self.__distances = q
        
    @property
    def jsonContent(self) -> str: 
        try:
            return json.dumps(self.__createEnveloppe(), cls=NumpyEncoder)
        except:
            return "{}"
    @jsonContent.setter
    def jsonContent(self, content):
        try:
            jsonEnv = json.loads(content)
            self.__items = jsonEnv[C.JST_NEAREST]
        except Exception as e:
            self.__items = []
            raise

    @property
    def size(self) -> items: 
        return len(self.items)
    
    def __createEnveloppe(self) -> str:
        jsonEnv = {}
        jsonEnv[C.JST_NEAREST] = self.items
        return jsonEnv
    
    def add(self, item):
        self.__items.append(item)

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
            jsonEnv = ""
            if (len(filename) >0):
                with open(filename, "r", encoding=C.ENCODING) as f:
                    jsonEnv = json.load(f)
            elif (len(content) >0):
                jsonEnv = content
            else:
                return False
            self.items = jsonEnv[C.JST_NEAREST]
            return True
        except Exception as e:
            return False