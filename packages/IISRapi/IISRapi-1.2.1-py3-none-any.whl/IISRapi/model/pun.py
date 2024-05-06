import os
import sys
import torch
import re
import flair
import subprocess
from flair.models import SequenceTagger
from flair.data import Sentence
from .data import Data
class IISRpunctuation:
    def __init__(self,dev):
        self.model_path=self.get_path()
        if(dev>=0 and torch.cuda.is_available()):
            flair.device = torch.device('cuda:' + str(dev))
            print(f"Running model with GPU No.{dev}")
        else:
            flair.device = torch.device('cpu')
            print("Running model with CPU")
            
        self.model = self.load_model()
        
    def get_path(self):
        try:
            import IISRpunctuation
            path=os.path.join(os.path.dirname(IISRpunctuation.__file__),"best-model-pun.pt")
        except ModuleNotFoundError:
            print("Model file not found. Downloading model...")
            model_url="https://github.com/DH-code-space/punctuation-and-named-entity-recognition-for-Ming-Shilu/releases/download/IISRmodel/IISRpunctuation-1.0-py3-none-any.whl"
            subprocess.call(["pip", "install", model_url])
            import IISRpunctuation
            path=os.path.join(os.path.dirname(IISRpunctuation.__file__),"best-model-pun.pt")
        return path
    
    def load_model(self):
        return SequenceTagger.load(self.model_path)
        
    def __call__(self,text):
        if isinstance(text, str):
            
            if(len(text)==1):
                ret_txt=text+'。'
                punct=[('。', 0)]
                result=Data(ori_txt=text, ret_txt=ret_txt,punct=punct)
            else:
                ret_txt,punct=self.tokenize(text.split('\n'))
                result=Data(ori_txt=text, ret_txt=ret_txt,punct=punct)
            return result
        
        elif isinstance(text,Data):
            
            if(len(text.ori_txt)==1):
                ret_txt=text.ori_txt+'。'
                punct=[('。', 0)]
                result=text._replace(ori_txt=text.ori_txt,ret_txt=ret_txt,punct=punct)
                
            else:
                ret_txt,punct=self.tokenize(text.split('\n'))
                result=text._replace(ori_txt=text.ori_txt,ret_txt=ret_txt,punct=punct)
            return result

    def tokenize(self,sentences):
        pos=[]
        WINDOW_SIZE = 256
        tokenized_sentences=[]
        for text in sentences:
            text = text.strip().replace(' ', '')
            if text == "":
                continue
            with_punctuation = []
            paragraph = list(text)
            curr_seg = 0
            end_flag = False
            while curr_seg < len(paragraph) - 1:
                start = curr_seg
                end = curr_seg + WINDOW_SIZE
                if curr_seg + WINDOW_SIZE > len(paragraph):
                    end = len(paragraph)
                    end_flag = True
                tokens = Sentence(paragraph[start : end], use_tokenizer=False)
                self.model.predict(tokens)
                curr_pos = curr_seg
                for token in tokens:
                    with_punctuation.append(text[curr_pos])
                    if token.get_label("ner").value != 'C':
                        if curr_pos != end - 1:
                            with_punctuation.append(token.get_label("ner").value)
                            pos.append((token.get_label("ner").value,curr_pos))
                            if not end_flag:
                                curr_seg = curr_pos + 1
                    curr_pos += 1
                if end_flag and curr_seg != len(paragraph):
                    curr_seg = len(paragraph)
                    with_punctuation.append('\u3002')
                    pos.append(('\u3002',curr_pos))
                while curr_pos > curr_seg:
                    with_punctuation.pop()
                    curr_pos -= 1
            tokenized_sentences.append(''.join(with_punctuation))
            tokenized_string=''.join(tokenized_sentences)
            return tokenized_string,pos
'''

'''