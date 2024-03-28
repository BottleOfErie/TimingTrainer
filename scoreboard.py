import tkinter as tk

class Scoreboard(tk.Label):
    def __init__(self,parent):
        super(Scoreboard,self).__init__(parent)
    
    def get_score(delta:float):
        delta=-delta
        if delta<0:
            return 7
        times=[5,12,13,19,25,30,45]
        for i in range(len(times)):
            if delta<times[i]:
                return i
        return 7

    def clear(self):
        self.deltas=[]
        self.scores=[0,0,0,0,0,0,0,0]
    
    def add_score(self,delta):
        names=['小居','大居','无回','回3','回5','回避衣','看破','MISS']
        self.deltas.append(delta)
        s=Scoreboard.get_score(delta)
        self.scores[s]=self.scores[s]+1
        txt=f"{names[s]}"
        for i in range(len(names)):
            if i % 2 ==0:
                txt=txt+'\n'
            txt=txt+names[i]+':'+str(self.scores[i])+' '
        self.config(text=txt)