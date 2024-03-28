import os,platform

os.environ['PYTHON_VLC_MODULE_PATH'] = "./vlclib"

import vlc

class Player:
    def __init__(self,*args):
        if args:
            instance=vlc.Instance(*args)
            self.media=instance.media_player_new()
        else:
            self.media=vlc.MediaPlayer()
    def play(self, path=None):
        if path:
            self.media.set_mrl(path)
        return self.media.play()
    def get_time(self):
        return self.media.get_time()
    # 拖动指定的毫秒值处播放。成功返回0，失败返回-1 (需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_time(self, ms):
        return self.media.set_time(int(ms))
    def next_frame(self):
        return self.media.next_frame()
    def get_position(self):
        return self.media.get_position()
    def set_position(self, float_val):
        return self.media.set_position(float_val)
    def get_frame_time(self):
        if self.media.get_fps()!=0:
            return 1/self.media.get_fps()
        return 1/60
    def get_fps(self):
        if self.media.get_fps()!=0:
            return self.media.get_fps()
        return 60
    def set_window(self, wm_id):
        if platform.system() == 'Windows':
            self.media.set_hwnd(wm_id)
        else:
            self.media.set_xwindow(wm_id)
    def pause(self):
        self.media.set_pause(1)
    def resume(self):
        self.media.set_pause(0)
    def stop(self):
        self.media.stop()
    # 返回当前状态：正在播放；暂停中；其他
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1
    def set_TimeChanged_callback(self, callback):
        self.media.event_manager().event_attach(vlc.EventType.MediaPlayerTimeChanged, callback)
    def set_PositionChanged_callback(self, callback):
        self.media.event_manager().event_attach(vlc.EventType.MediaPlayerPositionChanged, callback)


if __name__=="__main__":
    # path=input()
    player=Player()
    player.play("file:///E:/CloudMusic/Cloudier%20-%20FEAR%3blife.mp3")
    