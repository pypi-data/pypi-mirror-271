import os
import sys
import shutil
import string
digits = string.digits + string.letters
class netis:
    def __init__(self):
        pass
    def create_file(self,text,filename,exten):
        f = open(filename + "." + exten, "a")
        f.write(text)
        f.close()   
    def delete_file(self,filename):
        os.remove(filename)
    def copy_file(self,source,destination):
        shutil.copy(source,destination)
    def move_file(self,source,destination):
        shutil.move(source,destination)
    def create_dir(self,dirname):
        os.mkdir(dirname)
    def delete_dir(self,dirname):
        shutil.rmtree(dirname)
    def copy_dir(self,source,destination):
        shutil.copytree(source,destination)
    def move_dir(self,source,destination):
        shutil.move(source,destination)
    def rename_file(self,oldname,newname):
        os.rename(oldname,newname)
    def rename_dir(self,oldname,newname):
        os.rename(oldname,newname)
    def rename_dir(self,oldname,newname):
        os.rename(oldname,newname)
    def read_file(self,filename):
        f = open(filename, "r")
        text = f.read()
        f.close()
        return text
    def write_file(self,filename,text):
        f = open(filename, "w")
        f.write(text)
        f.close()
    def read_file_lines(self,filename):
        f = open(filename, "r")
        text = f.readlines()
        f.close()
        return text