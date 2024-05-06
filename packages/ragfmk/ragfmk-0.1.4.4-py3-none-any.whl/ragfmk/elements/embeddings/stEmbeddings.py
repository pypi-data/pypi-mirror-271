__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from sentence_transformers import SentenceTransformer
import ragfmk.utils.CONST as C
from ragfmk.elements.embeddings.embeddings import embeddings

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

class stEmbeddings(embeddings):
    def __init__(self):
        self.__embeddingsModel = C.EMBEDDING_MODEL
        super().__init__()

    @property
    def model(self) -> str: 
        return self.__embeddingsModel
    @model.setter
    def model(self, model):
        self.__embeddingsModel = model

    def encode(self, cks):
        """ to surcharge with the embeddings class
        Args:
            cks ( array []): list of chunks to create embeddings for each  
        Returns:
            numpy.ndarray: vector embeddings
        """
        try:
            encoder = SentenceTransformer(self.__embeddingsModel)
            return encoder.encode(cks.items)
        except:
            return None
