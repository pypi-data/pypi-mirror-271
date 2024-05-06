__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"
import sys
sys.path.append("./")

import argparse
from ragfmk.ragFAISS import ragFAISS
import ragfmk.utils.CONST as C
from ragfmk.elements.wrappers.chunks import chunks

"""
    usage: RagAdhocQueryDoc [-h] 
                            -prompt {question to the LLM} 
                            -pdf {PDF file and path} 
                            [-temperature {LLM temperature}] 
                            [-chunk_size {Chunk size for char chunking, def 500}]
                            [-chunk_overlap {Chunk overlap for char chunking, def 50}] 
                            [-sep {Chunk separator}] 
                            [-nearest {Number of nearest chunks}] 
                            [-model {Ollama LLM Model}]
                            [-urlbase {Ollama URL}]
"""
ARG_PROMPT = ["prompt", "Prompt to send to the LLM"]
ARG_PDFFILE = ["pdf", "PDF file path"]
ARG_TEMP = ["temperature", "LLM Temperature parameter, by defaul 0.9"]
ARG_CHUNKSIZE = ["chunk_size", "Chunk Size"]
ARG_CHUNKOVAP = ["chunk_overlap", "Chunk Overlap"]
ARG_SEP = ["sep", "Separator for chunking"]
ARG_NEAREST = ["nearest", "Faiss Number of nearest chunks to gather for prompting"]
ARG_MODEL = ["model", "Ollama Model installed"]
ARG_URL = ["urlbase", "URL for Ollama API (default localhost)"]

def main():
    parser = argparse.ArgumentParser()
    myRag = ragFAISS()
    try:
        parser.add_argument("-" + ARG_PROMPT[0], help=ARG_PROMPT[1], required=True)
        parser.add_argument("-" + ARG_PDFFILE[0], help=ARG_PDFFILE[1], required=True)
        parser.add_argument("-" + ARG_TEMP[0], help=ARG_TEMP[1], required=False, type=float, default=C.LLM_DEFAULT_TEMPERATURE) # float(self.temperature.replace(",", "."))
        parser.add_argument("-" + ARG_CHUNKSIZE[0], help=ARG_CHUNKSIZE[1], required=False, type=int, default=C.CHKS_DEFAULT_SIZE)
        parser.add_argument("-" + ARG_CHUNKOVAP[0], help=ARG_CHUNKOVAP[1], required=False, type=int, default=C.CHKS_DEFAULT_OVERLAP)
        parser.add_argument("-" + ARG_SEP[0], help=ARG_SEP[1], required=False, default=C.CHKS_DEFAULT_SEP)
        parser.add_argument("-" + ARG_NEAREST[0], help=ARG_NEAREST[1], required=False, type=int, default=C.SM_DEFAULT_NEAREST)
        parser.add_argument("-" + ARG_MODEL[0], help=ARG_MODEL[1], required=False, default=C.OLLAMA_DEFAULT_LLM)
        parser.add_argument("-" + ARG_URL[0], help=ARG_URL[1], required=False, default=C.OLLAMA_LOCAL_URL)
        args = vars(parser.parse_args())

        # 1 - Read the pdf content
        pdf = myRag.readPDF(args[ARG_PDFFILE[0]], C.READER_VALPYPDF)
        # 2 - Chunk document
        cks = myRag.charChunk(pdf, args[ARG_SEP[0]], args[ARG_CHUNKSIZE[0]], args[ARG_CHUNKOVAP[0]])
        # 3 - Text embeddings
        cksP = chunks()
        cksP.add(args[ARG_SEP[0]])
        vPrompt = myRag.createEmbeddings(cksP)
        # 4 - Chunks embeddings
        vChunks = myRag.createEmbeddings(cks)
        # 5 - Index the chunks
        myRag.addEmbeddings(vChunks)
        # 6 - Similarity Search
        myRag.initSearchEngine()
        similars = myRag.processSearch(args[ARG_NEAREST[0]], vPrompt)
        # 7 - Build prompt
        customPrompt = myRag.buildPrompt(args[ARG_PROMPT[0]], similars)
        # 8 - Ask to the LLM ...
        resp = myRag.promptLLM(customPrompt, args[ARG_URL[0]], args[ARG_MODEL[0]], args[ARG_TEMP[0]])
    
        print(resp)

    except Exception as e:
        parser.print_help()
        print(e)
        
if __name__ == "__main__":
    main()