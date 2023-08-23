import os
import wave
from tkinter import *
from tkinter import filedialog
import shutil
import io
from pydub import AudioSegment

music_path = "music/"
data_path = "data/"

# def mp3_to_wav(path,file):
#     fp = open(path, 'rb')
#     data = fp.read()
#     fp.close()
#
#     aud = io.BytesIO(data)
#     sound = AudioSegment.from_file(aud, format='mp3')
#     raw_data = sound.data
#
#     l = len(raw_data)
#     f = wave.open(music_path + file + ".wav", 'wb')
#     f.setnchannels(1)
#     f.setsampwidth(2)
#     f.setframerate(16000)
#     f.setnframes(l)
#     f.writeframes(raw_data)
#     f.close()


class MY_GUI():
    texts = ''
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口
    def set_window(self):
        self.init_window_name.title("谱子生成器")  # 窗口名
        self.init_window_name.geometry('360x480+10+10')
        # self.init_window_name["bg"] = "pink"                                    #窗口背景色
        # self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        # 标签
        self.root_label1 = Label(self.init_window_name, text="已生成的歌曲")
        self.root_label1.grid(row=0, column=0)
        self.root_label2 = Label(self.init_window_name, text="当前打开的歌曲")
        self.root_label2.grid(row=1, column=40)
        self.root_label2 = Label(self.init_window_name, text=self.texts)
        self.root_label2.grid(row=2, column=40)
        # 输出框
        self.root_list = Listbox(self.init_window_name, width=33, height=35)
        self.root_list.grid(row=1, column=0, rowspan=10, columnspan=10)
        # 按钮
        # self.open_file_button = Button(self.init_window_name, text="打开文件", bg="lightblue", width=10,command=self.open_file)
        # self.open_file_button.grid(row=2, column=40)
        self.trans_file_button = Button(self.init_window_name, text="生成谱子", bg="#FF5533", width=10,command=self.trans_file)
        self.trans_file_button.grid(row=3, column=40)

    def prints(self):
        self.root_list.insert("a")

    def open_file(self):
        global file_path
        file_path = filedialog.askopenfilename(title=u'选择音乐', initialdir=(os.path.expanduser('C:/')))
        if ".wav" in file_path:
            pass
        elif ".mp3" in file_path:
            mp3_to_wav(file_path)

    def trans_file(self):
        all_file_path = filedialog.askopenfilename(title=u'选择音乐', initialdir=(os.path.expanduser('music/')))
        file_path,file_name=os.path.split(all_file_path)


        if ".wav" in file_name:
            shutil.copy(all_file_path, music_path + file_name)
        elif ".mp3" in file_name:
            # mp3_to_wav(all_file_path,file_name.split(".")[0])
            mp3_file = AudioSegment.from_mp3(file=all_file_path)
            mp3_file.set_frame_rate(mp3_file.frame_rate).export(file_name.split(".")[0]+".wav",format="wav")
        else:
            self.texts = "文件格式错误"
        print(all_file_path+" "+ file_name)



def gui_start():
    root = Tk()  # 实例化出一个父窗口
    main1 = MY_GUI(root)
    # 设置根窗口默认属性
    main1.set_window()
    root.mainloop()


gui_start()
