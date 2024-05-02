__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from sentence_transformers import SentenceTransformer
import ragfmk.utils.CONST as C
from ragfmk.elements.embeddings.embeddings import embeddings

"""
        Embeddings and data are stored in JSON and used with the following format :
        {0: {'text': 'How many jobs Joe Biden wants to create ?', 
             'embedding': array([-6.65125623e-02,  4.26685601e-01, -1.22626998e-01, -1.14275487e-02,
                                -1.76032424e-01, -2.55425069e-02,  3.19633447e-02,  1.10126780e-02,
                                -1.75059751e-01,  2.00320985e-02,  3.28031659e-01,  1.18581623e-01,
                                -9.89666581e-02,  1.68430805e-01,  1.19766712e-01, -7.14423656e-02, ...] 
            },
        1: {'text': '...', 
            'embedding': array([...]
            },
        ...
        }
"""

class stEmbeddings(embeddings):
    def __init__(self):
        super().__init__()
        
    def encode(self, cks):
        try:
            encoder = SentenceTransformer(C.EMBEDDING_MODEL)
            return encoder.encode(cks.items)
        except:
            return None
