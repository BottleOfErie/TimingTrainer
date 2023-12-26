import tkinter as tk
import pickle
import os

cache={}

class MarkItem:
    def __init__(self,time,position,name):
        self.time=time
        self.name=name
        self.position=position
    
    def __str__(self) -> str:
        return f"{self.time}:{self.name}"

if os.path.exists("./cache.py"):
    with open("./cache.py","rb") as f:
        cache=pickle.load(f)

class MarkList(tk.Listbox):
    def __init__(self,parent):
        super(MarkList,self).__init__(parent,width=100)
        self.hasfile=False
        self.bind('<Double-Button-1>',lambda evt:MarkList.upload_mark(parent,self.marks[self.curselection()[0]]))
        # self.bind('<Double-Button-1>',lambda evt:print(self.curselection()))
        self.bind('<Double-Button-2>',lambda evt:self.delete_mark(self.curselection()))
    
    def upload_mark(parent,mark):
        parent.mark_frame=mark.time
        parent.info(f"marked:{mark.time} ms")
        parent.player.set_position(mark.position)
        parent.position.set(mark.position*1000)

    def delete_mark(self,item):
        print(item)
        del self.marks[item[0]]
        self.delete(item)

    def add_item(self,item:MarkItem):
        self.insert(tk.END,item)
        self.marks.append(item)
    
    def set_file(self,file):
        self.clear()
        self.file=file
        self.hasfile=True
        self.marks=[]
        if file in cache.keys():
            for item in cache[file]:
                self.add_item(item)
            self.marks=cache[file]
    
    def clear(self):
        if not self.hasfile:
            return
        cache[self.file]=self.marks
        with open("./cache.py","wb") as f:
            pickle.dump(cache,f,pickle.HIGHEST_PROTOCOL)
        self.marks=[]
        self.delete(0,tk.END)