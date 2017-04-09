# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 20:19:19 2017

@author: Administrator

remove lyric from the txt, for the lyric downloaded for internet
have a translation below each line what don't appeal to me aesthetically
"""

def remove_chinese():
    txt_file = open("geci.txt",'r',encoding = 'utf8')
    result_file = open("new_geci.txt",'w',encoding = 'utf8')
    
    tally = 1
    
    for line in txt_file:
        if(tally%2):
            result_file.writelines(line)
        tally+=1
    txt_file.close()
    result_file.close()

    
if __name__=='__main__':
    remove_chinese()
