__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import ragfmk.utils.CONST as C
from ragfmk.interfaces.IPrompt import IPrompt
from jinja2 import Template

class prompt(IPrompt):
    def __init__(self, question, similarItems):
        self.__question = question
        self.__similarItems = similarItems  # list (nearest)
        self.__template = C.PROMPT_RAG_JINJA_TEMPLATE

    @property
    def template(self):
        return self.__template
    @template.setter
    def template(self, t):
        self.__template = t
        
    @property
    def question(self):
        return self.__question
    @question.setter
    def question(self, q):
        self.__question = q
    
    @property
    def similarItems(self):
        return self.__similarItems
    @similarItems.setter
    def similarItems(self, q):
        self.__similarItems = q

    def loadTemplate(self, filename):
        try:
            with open(filename, "r", encoding=C.ENCODING) as f:
                self.__template = f.read()
            return True
        except Exception as e:
            return False

    def build(self):
        try:
            if (len(self.template) == 0):
                raise Exception ("A JINJA2 template must be specified.")
            if (len(self.question) == 0):
                raise Exception ("The RAG question for the prompt must be filled out.")
            if (self.similarItems.size == 0):
                raise Exception ("The number of context informations (chunks) cannot be empty.")
            j2_template = Template(self.template)
            data = { C.TPL_QUESTION: self.question, 
                     C.TPL_NEAREST: self.similarItems }
            return j2_template.render(data)
        except Exception as e:
            raise