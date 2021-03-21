#coding:utf-8
#公众号：覃原
#用pyaudio进行语音录制，注意设置采样频率为16000,以便后面用百度语音识别

import pyaudio
import wave
from tqdm import tqdm  #进度条显示
from playsound import playsound
import time

###########################
#     pyaudio初始化       #
###########################
# pyaudio采集流参数
# 语音采集函数，output：待写入文件；time：录制时长
def record(output,time):
    # 采样点
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    # 声道
    CHANNELS = 1
    # 百度语音识别的采样频率为16000
    RATE = 16000
    # 实例化pyaudio
    p = pyaudio.PyAudio()
    # 初始化pyaudio
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    # 打开待写入的wav音频并进行初始化
    wf = wave.open(output, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    print("语音采集开始")
    for i in tqdm(range(0, int(RATE / CHUNK * time))):
        # 读取语音流
        data = stream.read(CHUNK)
        # 写入语音流
        wf.writeframes(data)
    print("语音采集结束")
    # 暂停/停止
    stream.stop_stream()
    # 终止语音流
    stream.close()
    # 终止会话
    p.terminate()
    # 关闭文件
    wf.close()
    
# 录制8秒
record("demo.wav",10)
time.sleep(1)
print("播放音频")
playsound("demo.wav")
