'''
A class that enapsulate a machine learning model to build and train
a model on a digitized holy book of Quran. Train the model using word2vec
model (NGram).
'''

import pandas as pd
import nltk
import arabic_reshaper
import matplotlib.pyplot as plt 
from bidi.algorithm import get_display
from wordcloud import WordCloud
import re, sys
import pathlib
#from gensim.models import Word2Vec

from typing import List, Dict

from gensim.models.keyedvectors import KeyedVectors
#from gensim.test.utils import datapath
from pathlib import Path

LIB_DIRECTORY = pathlib.Path(__file__).parent.absolute()

class QuranContextToWords:
    
    _word2vec_model = None
    _quran_data = None
    
    def __init__(self):
        ''' Load the quran book '''
        
        try:
            # Load Quran from csv into a dataframe
            self._quran_data = pd.read_csv('train/data/quran.txt', sep='|', header='infer');
        except:
            print('Failed to load the quran book with err')
    
        
    
    def _plot_word_cloud(self, word_list: List[str], word_frequency: Dict[str, float], save_to: str):
        ''' Plot a WordCloud for top words that occured around the context word '''
        full_string = ' '.join(word_list)
        reshaped_text = arabic_reshaper.reshape(full_string)
        translated_text = get_display(reshaped_text)
        font_path = str(LIB_DIRECTORY / 'tahoma.ttf')
        # Build the Arabic word cloud
        wordc = WordCloud(font_path=font_path, background_color='white',width=2000,height=1000).generate(translated_text)
        wordc.fit_words(word_frequency)
        
        # Draw the word cloud
        plt.imshow(wordc)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        
        # save the plot to output jpeg file
        plt.savefig(save_to)
    
    
    def print_similar_word_cloud(self, one_word: str, save_to: str, topn: int):
        """Takes an Arabic word and print similar word cloud for top number of words {$topn}."""
        
        #temp_tuple = self._word2vec_model.most_similar(positive=[one_word], negative=[], topn=topn)
        model = KeyedVectors.load_word2vec_format(Path.cwd() / 'model_quran.txt', binary=False)
        temp_tuple = model.most_similar(positive=[one_word], negative=[], topn=topn)
        similar_words=[i[0] for i in temp_tuple]
        
        # Extract word weight to project it in the WordCloud plot
        word_frequency = {}
        for word_tuple in temp_tuple:
            reshaped_word = arabic_reshaper.reshape(word_tuple[0])
            key = get_display(reshaped_word)
            word_frequency[key] = word_tuple[1]
        
        self._plot_word_cloud(similar_words, word_frequency, save_to)
        
