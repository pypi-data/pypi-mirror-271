__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import sys
sys.path.append("./")

import argparse
from ragfmk.rag import rag
import ragfmk.utils.CONST as C
from ragfmk.elements.wrappers.nearest import nearest

ARG_PROMPT = ["prompt", "Prompt to send to the LLM"]
ARG_PROMPT_TEMPLATE = ["template", "Prompt template to use when building the prompt (must contain {prompt} and {context}"]
ARG_NEARESTFILE = ["nfile", "JSON file path which contains the nearest chunks/texts"]

"""
    Build a prompt based on a template. The template must contain the {context} and {prompt} tags inside.
    By default: "Question: {prompt}\n Please answer the question based on the informations listed below: {context}"

    usage: RagPrompt [-h] 
                     -prompt {question to ask to the LLM} 
                     -nfile {list of the nearest chunks / json}
                     [-template {template string}] 
"""
def main():
    parser = argparse.ArgumentParser()
    myRag = rag()
    try:
        parser.add_argument("-" + ARG_PROMPT[0], help=ARG_PROMPT[1], required=True)
        parser.add_argument("-" + ARG_PROMPT_TEMPLATE[0], help=ARG_PROMPT_TEMPLATE[1], required=False, 
                            default = C.PROMPT_RAG_TEMPLATE)
        parser.add_argument("-" + ARG_NEARESTFILE[0], help=ARG_NEARESTFILE[1], required=True)
        args = vars(parser.parse_args())
        
        nr = nearest()
        nr.load(filename=args[ARG_NEARESTFILE[0]])
        resp = myRag.buildPrompt(args[ARG_PROMPT[0]], nr)

        print(resp)

    except Exception as e:
        parser.print_help()
        print(e)
        
if __name__ == "__main__":
    main()