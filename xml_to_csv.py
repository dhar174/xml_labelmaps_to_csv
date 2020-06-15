import os
import glob
import pandas as pd
import re
import string
from collections import OrderedDict
import io
import csv
from itertools import zip_longest

xml_list = []
filename=[]
width=[]
height=[]
class_var=[]
xmin=[]
ymin=[]
xmax=[]
ymax=[]


for filepath in glob.iglob("**/*.xml*", recursive=True):
        nonascii = bytearray(range(0x80, 0x100))
        with open(filepath,'rb') as infile, open('double'+filepath,'wb') as outfile:
            for line in infile: # b'\n'-separated lines (Linux, OSX, Windows)
                outfile.write(line.translate(None, nonascii))
        raw=open('double'+filepath,'r')
        data=raw.read()
        raw.close()
        os.remove('double'+filepath)
        printable = set(string.printable)
        re.sub(r'[^\x00-\x7F]+',' ', data)
        data=''.join(filter(lambda x: x in printable, data))
        #print("NEW DATA=                "+data)
        
        #print(re.search('<imageName>(.+?)</imageName>',data).group(1))
        #filename.append(re.search('<imageName>(.+?)</imageName>',data).group(1).rsplit('\\.*?\\',1)[-1])
        #idx=re.search('<imageName>(.+?)</imageName>',data).rfind("\\")


        #FIND VALUE, APPEND LIST:
        try:
            f=re.search('<imageName>(.+?)</imageName>',data).group(1).rsplit('\\',1)[-1]
            filename.append(f)
##            print(f)
        except:
            filename.append('unknown')
        try:
            w=re.search('resolution x="(.+?)"',data).group(1)
            width.append(w)
##            print(w)
        except:
            width.append('na')
        try:
            h=re.search('resolution.+y="(.+?)"',data).group(1)
            height.append(h)
##            print(h)
        except:
            height.append('na')
        try:
            xmin1=re.search('word x="(.+?)"',data).group(1)
            xmin.append(xmin1)
##            print(xmin1)
        except:
            xmin.append('na')

        try:   
            ymin1=re.search('word x=".+y="(.+?)"',data).group(1)
            ymin.append(ymin1)
##            print(ymin1)
        except:
            ymin.append('na')
        try:
            xmax1=re.search('word x=".+width="(.+?)"',data).group(1)
            xmax2=str(int(xmax1)+int(xmin1))
            xmax.append(xmax2)
##            print(xmax2)
        except:
            xmax.append('na')

        try:  
            ymax1=re.search('word x=".+width="(.+?)"',data).group(1)
            ymax2=str(int(ymax1)+int(ymin1))
            ymax.append(ymax2)
##            print(ymax2)
        except:
            ymax.append('na')
        class_var.append('sign_readable')
        

#print(filename)
column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
xml_df = pd.DataFrame(xml_list, columns=column_name)
#final=zip(filename,width,height,xmin,ymin,xmax,ymax)
final=[filename,width,height,class_var,xmin,ymin,xmax,ymax]
export_data = zip_longest(*final, fillvalue = '')
print("Now Collating.....")
print(export_data)
with open('train_labels.csv', 'w',newline='') as outfile:
        fieldnames = ['filename', 'width', 'height', 'class', 'xmin','ymin','xmax','ymax']
        #my_names_dict = dict(zip(fieldnames, final))
        writer = csv.writer(outfile)
        #if nn ==0:
        #writer.writeheader()
        #nn+=1
                
        #reader =csv.DictReader(infile)
        #next(reader, None)
    
        
        #row['class']='sign_readable'
        #print(row)
        
        writer.writerow(('filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'))
        writer.writerows(export_data)
        #writer.writerows(final)

