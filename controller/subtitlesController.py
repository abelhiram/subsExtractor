import pysrt
import pandas as pd
import re
import os

class subtitlesController():

    def __init__(self):
        self.out_list =[]
        self.subtitle_matrix = []
        

    def __getSubtitlesMatrix(self,**kwargs):
        files = kwargs["files"] if kwargs["file"]==[None] else kwargs["file"]
        subtitles_object = [pysrt.open(path) for path in files]
    
        for episode in subtitles_object:
            subtitle_temp_list = [word.text.split() for word in episode]
            self.subtitle_matrix.append(subtitle_temp_list)
            subtitle_temp_list=[]

    
    def __extractWords(self):
        expressions_to_avoid = ["</i>","<i>","♪</i>","<i>♪","-","♪"," "]
        replace_dict = {'.': '', '-': '',',':'','?':'','</i>':'','<i>':'','!':'',"\"":''} 
        replace_dict = dict((re.escape(key), value) for key, value in replace_dict.items()) 
        pattern = re.compile("|".join(replace_dict.keys()))

        for episode in self.subtitle_matrix:
            for subtitle_list in episode:
                individualWord=[pattern.sub(lambda m: replace_dict[re.escape(m.group(0))], word).upper() 
                                            for word in subtitle_list if word not in expressions_to_avoid] 
                for word in individualWord:
                    self.out_list.append(word)
        

    def ToDataFrame(self,folder=None,file=None):
        self.out_list =[]
        self.subtitle_matrix = []
        self.__getSubtitlesMatrix(files =self.getAllFiles(folder) if folder !=None else None,
                                  file=file if file!=None else [None])
        self.__extractWords()
        ocurrences = pd.Series(self.out_list).value_counts()
        df = pd.DataFrame(ocurrences)
        df.to_csv('word_census.csv')


    def getAllFiles(self,folder):
        allfiles =[]
        for root,dirs,season in os.walk(f'./{folder}/'):
            if season != []:
                for episode in season:
                    allfiles.append(root.replace("\\""","/")+"/"+episode)
        return allfiles
    

    def folderNames(self,directory):
        folders = [folder for folder in os.listdir(f'./{directory}')]
        return folders
                
        
        