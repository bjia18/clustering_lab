from __future__ import print_function
warned_of_error = False
from sse_and_centroid import *
import csv
import nltk
from nltk.corpus import stopwords
import pygame
import simplejson
from pytagcloud import create_tag_image, make_tags

def create_cloud (oname, words,maxsize=120, fontname='Lobster'):
    '''Creates a word cloud (when pytagcloud is installed)
    Parameters
    ----------
    oname : output filename
    words : list of (value,str)
    maxsize : int, optional
        Size of maximum word. The best setting for this parameter will often
        require some manual tuning for each input.
    fontname : str, optional
        Font to use.
    '''

    # gensim returns a weight between 0 and 1 for each word, while pytagcloud
    # expects an integer word count. So, we multiply by a large number and
    # round. For a visualization this is an adequate approximation.


    #words = [(w,int(v*10000)) for w,v in words]
    tags = make_tags(words, maxsize=maxsize)
    create_tag_image(tags, oname, size=(1800, 1200), fontname=fontname)


#example of using word cloud for first 10 rows of courses
def cloud(clusters, data):
    word_counts = {}
    file=open('dimensions_keywords.csv')
    file=file.read().split('\n')
    words=[]
    for i in range(1,len(file)):
        words.append(file[i].split(',')[1:])
    for i in range(len(clusters)):
        w=[]
        c=clusters[i]
        centroid=calc_centroid(c,data)

        for j in range(len(centroid)):
            if centroid[j]>50:
                tag=0
            else:
                tag=1
            w+=words[j][tag].split(' ')
        count={}
        for j in w:
            if j in count:
                count[j]+=1
            else:
                count[j]=1

        word_counts = [(j,count/20) for j,count in count.items()]
        create_cloud('clouds/cluster_{}.png'.format(str(i)), word_counts)