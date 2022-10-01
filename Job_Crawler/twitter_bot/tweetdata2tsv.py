import re, os, sys, time, random, subprocess, optparse

basepath=os.curdir 
abspath=os.path.abspath(basepath)  

for file in os.listdir(os.getcwd()):   
    if os.path.isfile(file):
        (root, ext) = os.path.splitext(file)
        if (ext.lower() == '.json'):
            print(file)
            cmd=("python data2spreadsheet.py %s" % (file))
            print (cmd)             
            os.system(cmd)

print (os.getcwd())
p=input()
