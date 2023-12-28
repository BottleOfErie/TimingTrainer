import tkinter as tk

class Scoreboard(tk.Label):
    def __init__(self,parent):
        super(Scoreboard,self).__init__(parent)
    
    def get_score(delta:float):
        delta=-delta
        if delta<0:
            return 7
        times=[13,15,17,19,22,25,30]
        for i in range(len(times)):
            if delta<times[i]:
                return i
        return 7

    def clear(self):
        self.deltas=[]
        self.scores=[0,0,0,0,0,0,0,0]
    
    def add_score(self,delta):
        names=['无回','回1','回2','回3','回4','回5','回避衣','MISS']
        self.deltas.append(delta)
        s=Scoreboard.get_score(delta)
        self.scores[s]=self.scores[s]+1
        txt=f"{names[s]}"
        for i in range(len(names)):
            if i % 2 ==0:
                txt=txt+'\n'
            txt=txt+names[i]+':'+str(self.scores[i])+' '
        self.config(text=txt)