import tkinter as tk
from player import Player
from tkinter.filedialog import askopenfilename
import pathlib
import time
import mark_list
import scoreboard

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.player = Player()
        self.title("TimingTrainer")
        self.position=tk.DoubleVar()
        self.mark_frame=-1
        self.last_time=0
        self.last_accurate_time=0
        self.delta_accumulation=0
        self.last_pause_time=0
        self.create_video_view()
        self.create_control_view()
        self.create_mark_list()
        self.bind("<space>",lambda x: self.spacebar_pressed())
    
    def info(self,infomation):
        self.info_label.config(text=infomation)
        print(infomation)

    def update_time(self):
        self.last_time=self.player.get_time()
        self.last_accurate_time=int(time.time()*1000)
        self.delta_accumulation=0

    def fetch_time(self):
        if not self.player.get_state()==1:
            return self.last_pause_time
        current_time=self.player.get_time()
        now=int(time.time()*1000)
        if(not self.last_time==0):
            self.delta_accumulation+=now-self.last_accurate_time
            current_time+=self.delta_accumulation
        return current_time

    def spacebar_pressed(self):
        if(self.player.get_state()==1):
            self.last_pause_time=self.fetch_time()
            if(self.mark_frame>-1):
                time=self.last_pause_time-self.mark_frame
                self.info(f"delta:{time} ms ({time/1000*60} frames)")
                self.scoreboard.add_score(time/1000*60)
            self.player.pause()

    def create_video_view(self):
        self._canvas = tk.Canvas(self, bg="black",width=960,height=540)
        self._canvas.pack()
        self.player.set_window(self._canvas.winfo_id())
        self.player.set_PositionChanged_callback(lambda x:self.position.set(self.player.get_position()*1000))
        self.player.set_TimeChanged_callback(lambda x:self.update_time())

    def create_control_view(self):
        frame = tk.Frame(self)
        tk.Scale(frame, from_=0, to=1000, orient=tk.HORIZONTAL,variable=self.position,command=lambda x:self.player.set_position(self.position.get()/1000), length=900).pack(side=tk.TOP)
        tk.Button(frame, text="播放/打开", command=lambda: self.click(0)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="暂停", command=lambda: self.click(1)).pack(side=tk.LEFT)
        tk.Button(frame, text="步进", command=lambda: self.click(2)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="标记", command=lambda: self.click(3)).pack(side=tk.LEFT)
        tk.Button(frame, text="保存", command=lambda: self.click(4)).pack(side=tk.LEFT)
        self.info_label=tk.Label(frame)
        self.info_label.pack(side=tk.LEFT, padx=5)
        frame.pack(side=tk.BOTTOM)
    
    def create_mark_list(self):
        frame=tk.Frame(self)
        self.scoreboard=scoreboard.Scoreboard(frame)
        self.scoreboard.pack(side=tk.LEFT)
        self.mark_list=mark_list.MarkList(frame,self)
        self.mark_list.pack(side=tk.RIGHT)
        frame.pack(side=tk.BOTTOM)

    def click(self, action):
        if action == 0:
            self.last_accurate_time=int(time.time()*1000)
            if self.player.get_state() == 0:
                self.player.resume()
            else:
                file=askopenfilename(title="打开视频文件")
                if file:
                    self.mark_frame=-1
                    self.last_time=0
                    self.last_accurate_time=0
                    self.delta_accumulation=0
                    self.last_pause_time=0
                    self.position.set(0)
                    self.mark_list.set_file(pathlib.Path(file).name)
                    self.scoreboard.clear()
                    self.player.play(pathlib.Path(file).as_uri())
        elif action == 1:
            if self.player.get_state() == 1:
                self.last_pause_time=self.fetch_time()
                self.player.pause()
        elif action == 2:
            if(self.player.get_state()==0):
                self.player.next_frame()
                self.last_pause_time+=self.player.get_frame_time()*1000
        elif action == 3:
            if self.player.get_state() in [0,1]:
                self.mark_frame=self.fetch_time()
                self.mark_list.add_item(mark_list.MarkItem(self.mark_frame,self.player.get_position(),str(self.mark_list.size())))
                self.info(f"marked:{self.mark_frame} ms")
        elif action == 4:
            self.mark_list.save()
            self.info(f"Saved")
            


if "__main__" == __name__:
    app = App()
    app.mainloop()