__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from ragfmk.rag import rag
from ragfmk.elements.simsearchengines.ChromaDBWrapper import ChromaDBWrapper
import ragfmk.utils.CONST as C

class ragChromaDB(rag):
    def __init__(self):
        self.__mycdb = ChromaDBWrapper()
        self.__collectionName = "default"
        self.__hostname = C.CDB_DEFAULT_HOST
        self.__port = C.CDB_DEFAULT_PORT
        super().__init__()
        
    @property
    def collectionName(self):
        return self.__collectionName
    @collectionName.setter
    def collectionName(self, value):
        self.__collectionName = value
    
    @property
    def hostname(self):
        return self.__hostname
    @hostname.setter
    def hostname(self, value):
        self.__hostname = value

    @property
    def port(self):
        return self.__port
    @port.setter
    def port(self, value):
        self.__port = value

    def initSearchEngine(self):
        self.__mycdb.initServer(self.hostname, self.port)

    def addEmbeddings(self, vChunks) -> int:
        """ Add text chunks (embeddings) in the Chroma DB
            Format:
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
        Args:
            vChunks (embeddings): embeddings object
        """
        ret = self.__mycdb.add(vChunks, self.__collectionName)
        self.addMilestone("ADDTOINDEX", "Add chunks to the Chroma DB Index")
        return ret
    
    def processSearch(self, k, vPrompt):
        """ Makes a search in the FAISS index and returns the k mearest datasets from the prompt
        Args:
            k (int): most k nearest chunks
            vPrompt (embeddings): prompt embeddings
        Returns:
            nearest: Object with List of the most nearest neighbors
        """
        similars = self.__mycdb.getNearest(vPrompt, k, self.__collectionName)
        self.addMilestone("SIMILARSEARCH", "Similarity Search executed successfully")
        return similars