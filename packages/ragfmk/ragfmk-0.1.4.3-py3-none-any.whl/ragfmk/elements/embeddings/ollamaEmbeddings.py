__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import requests
import json

import src.ragfmk.utils.CONST as C
from src.ragfmk.elements.embeddings.embeddings import embeddings

"""
        Embeddings and data are stored in Python list/JSON and used with the following format :
        {"0": {
                'text': 'The prompt or text', 
                'embedding': array([-6.65125623e-02,  
                                    ..., 
                                    -1.22626998e-01]) 
              },
        "1": {
                'text': '...',  
                'embedding': array([...]) 
              },
        ...,
        "x" : { ... }
        }
"""

class ollamaEmbeddings(embeddings):
    def __init__(self):
        self.__embeddingsModel = C.OLLAMA_DEFAULT_EMB
        self.__urlbase = C.OLLAMA_LOCAL_URL
        super().__init__()

    @property
    def model(self) -> str: 
        return self.__embeddingsModel
    @model.setter
    def model(self, model):
        self.__embeddingsModel = model

    @property
    def urlbase(self) -> str: 
        return self.__urlbase
    @urlbase.setter
    def urlbase(self, url):
        self.__urlbase = url

    def _getEmbeddings(self, prompt):
        try:
            url = self.urlbase + "/embeddings"
            params = {"model": self.model,
                      "prompt": prompt}
            response = requests.post(url, json=params)
            if (response.status_code == 200):
                response_text = response.text
                data = json.loads(response_text)
                return data["embedding"]
            else:
                raise Exception("Error while reaching out to the Web Service: {}", str(response.status_code, response.text))
        except Exception as e:
            return str(e)

    def encode(self, cks):
        """ to surcharge with the embeddings class
        Args:
            cks (array []): list of chunks to create embeddings for each  
        Returns:
            numpy.ndarray: vector embeddings
        """
        try:
            return self._getEmbeddings(cks.items)
        except:
            return None