import sys
sys.path.append("./")

from ragfmk.ragFAISS import ragFAISS
from ragfmk.elements.embeddings.stEmbeddings import stEmbeddings
from ragfmk.elements.embeddings.ollamaEmbeddings import ollamaEmbeddings
from ragfmk.rag import rag
from ragfmk.elements.wrappers.nearest import nearest
from ragfmk.elements.wrappers.chunks import chunks
import ragfmk.utils.CONST as C
import argparse

PDFFILE = "data/Following is a transcript of President Biden.pdf"
TXTFILE = "working/Following is a transcript of President Biden.txt"
RAGPROMPT = "How many jobs Joe Biden wants to create ?"
CHUNKFILE = "working/biden_chunks.json"
CHKEMBFILE = "working/biden_emb_chunks.json"
PRTEMBFILE = "working/biden_emb_prompt.json"
NEARESTFILE = "working/biden_nearest.json"
SIMPLEPROMPT = "Do you know pytorch ?"
FAISSINDEXNAME = "biden"

def search_into_index(filename, content, idx, store, k, output):
	myRag = ragFAISS()
	vPrompt = stEmbeddings()
	myRag.indexName = idx
	myRag.storagePath = store
	myRag.initSearchEngine()
	if (len(content)>0):
		vPrompt.jsonContent = content
	else:
		vPrompt.load(filename=filename)
	similars = myRag.processSearch(k, vPrompt)
	if (len(output) > 0):
		similars.save(output)
	return similars.jsonContent, myRag.milestones.getFullJSON()

def build_prompt(question, nearestfile, content, template):
    myRag = rag()
    nr = nearest()
    if (len(content)>0):
        nr.jsonContent = content
    else:
        nr.load(nearestfile)
    resp = myRag.buildPrompt(question, nr)
    return resp, myRag.milestones.getFullJSON()

def create_embeddings_prompt(question, nearestfile, content, template):
	myRag = rag()
	cks = chunks()
	cks.add(RAGPROMPT)
	embeddings = myRag.createEmbeddings(cks)
 
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-option", help="test option", required=True)
	args = vars(parser.parse_args())

	if (args["option"] == "search_into_index"):
		with open(PRTEMBFILE, "r", encoding="utf-8") as f:
			emb = f.read()
		resp, _ = search_into_index("", emb, FAISSINDEXNAME, C.FAISS_DEFAULT_STORE, 4, "")
		print(resp)

	elif (args["option"] == "build_prompt"):
		resp, _ = build_prompt()
		print(resp)

	