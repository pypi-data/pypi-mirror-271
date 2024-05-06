__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from ragfmk.elements.simsearchengines.FAISSWrapper import FAISSWrapper
from ragfmk.rag import rag
from ragfmk.elements.wrappers.nearest import nearest
import ragfmk.utils.CONST as C

"""
    This FAISS implementation uses by default the sentence_transformer model (cf. C.EMBEDDING_MODEL) to create and manage embeddings
"""
FAISS_INDEX_MEMORY = "memory"

class ragFAISS(rag):
    def __init__(self):
        self.__myfaiss = FAISSWrapper()
        self.__indexName = FAISS_INDEX_MEMORY
        self.__storagePath = C.FAISS_DEFAULT_STORE
        super().__init__()

    @property
    def indexName(self):
        return self.__indexName
    @indexName.setter
    def indexName(self, value):
        self.__indexName = value

    @property
    def storagePath(self):
        return self.__storagePath
    @storagePath.setter
    def storagePath(self, value):
        self.__storagePath = value

    def addEmbeddings(self, vChunks):
        """ Add text chunks (embeddings) in the FAISS index
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
            vChunks (stEmbeddings): embeddings object to add into the index
        """
        self.__myfaiss.add(vChunks)
        self.addMilestone("ADDTOINDEX", "Add chunks to the FAISS Index")

    def processSearch(self, k, vPrompt) -> nearest:
        """ Makes a search in the FAISS index and returns the k mearest datasets from the prompt

        Args:
            k (int): most k nearest chunks
            vPrompt (stEmbeddings): Object embeddings for the prompt
        Returns:
            DataFrame: List of the most nearest neighbors
        """
        similars = self.__myfaiss.getNearest(vPrompt, k)
        self.addMilestone("SIMILARSEARCH", "Similarity Search executed successfully")
        return similars

    def saveIndex(self):
        """ Store the FAISS index on the disk
        Args:
            path (str): index path
        Returns:
            _type_: False if error
        """
        try:
            self.addMilestone("FAISSSTORE", "Chunks embeddings indexed and stored successfully")
            if (self.indexName != FAISS_INDEX_MEMORY):
                self.__myfaiss.save(self.storagePath, self.indexName)
            return True
        except Exception as e:
            self.log.error("Error while storing FAISS index: {}".format(e))
            return False

    def initSearchEngine(self):
        """ Load the FAISS index on the disk
        Args:
            path (str): index path
        Returns:
            _type_: False if error
        """
        try:
            self.addMilestone("FAISSLOAD", "Loading Similarity Search Engine (FAISS)")
            if (self.indexName != FAISS_INDEX_MEMORY):
                self.__myfaiss.load(self.storagePath, self.indexName)
            return True
        except Exception as e:
            self.log.error("Error while loading FAISS index: {}".format(e))
            return False