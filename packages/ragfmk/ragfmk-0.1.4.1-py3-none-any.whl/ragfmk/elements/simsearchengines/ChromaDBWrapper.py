__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import chromadb
from chromadb.utils import embedding_functions
import ragfmk.utils.CONST as C
import pandas as pd
from ragfmk.elements.wrappers.nearest import nearest

""" 
    Leverage Chroma DB
    Starts server locally bveforehand: 
        $ chroma run --path D:/chromadb
"""
embFunction = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=C.CDB_DEFAULT_EMBEDDINGSMODEL_ST)

class ChromaDBWrapper:
    def __init__(self):
       self.__chroma_client = None
    
    def initServer(self, host, port):
        self.__chroma_client = chromadb.HttpClient(host=host, port=port)
        
    def initLocal(self):
        self.__chroma_client = chromadb.Client()
        
    def initPersistent(self, location):
        self.__chroma_client = chromadb.PersistentClient(path=location)
    
    @property
    def ready(self) -> bool:
        return (self.__chroma_client != None)
    
    @property
    def client(self):
        return self.__chroma_client

    def getCollection(self, name) -> chromadb.Collection:
        try:
            if (len(name)<=0):
                raise Exception ("A collection must have a name!")
            return self.__chroma_client.get_or_create_collection(name, embedding_function=embFunction)
        except Exception as e:
            return None
        
    def add(self, vItems, collectionName) -> int:
        """ Add a item list ([ str ]) in the DB
        Args:
            vItems (DataFrame): Data and embeddings
            collectionName (str): Chroma DB collection name
        """
        try:
            dfNewContent = pd.DataFrame(vItems.content).T
            collection = self.getCollection(collectionName)
            if (collection == None):
                raise Exception ("Impossible to get the collection from Chroma DB")
            collection.add(documents=dfNewContent[C.JST_TEXT].tolist(),
                           embeddings=dfNewContent[C.JST_EMBEDDINGS].tolist(),
                           ids=["id_"+ str(i) for i in range(len(dfNewContent))],
                           metadatas=[{"md_id": i} for i in range(len(dfNewContent))])               
            return collection.count()
        except Exception as e:
            raise
        
    def getNearest(self, vText, k, collectionName):
        """ Process the similarity search on the existing Chroma DB (and the given prompt)
                --> k is set to the total number of vectors within the index
                --> ann is the approximate nearest neighbour corresponding to those distances
        Args:
            vText (json): Prompt's embeddings
            k (int): Nb of nearest to return
        Returns:
            DataFrame: List of the most nearest neighbors
        """
        try:
            collection = self.getCollection(collectionName) 
            if (collection == None):
                raise Exception ("Impossible to get the collection from Chroma DB")
            result = collection.query(query_embeddings=vText.content["0"]["embedding"], n_results=k)
            nr = nearest()
            nr.items = result["documents"][0]
            nr.distances = result["distances"][0]
            return nr
        except Exception as e:
            raise