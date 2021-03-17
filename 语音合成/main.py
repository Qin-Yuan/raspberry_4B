from aip import AipSpeech
from playsound import playsound

#请自己注册百度AI平台账号，然后创建语音合成项目，输入对应的密码
baidu_APP_ID='282434'
baidu_API_KEY='ohDPZ9SdEF1jH96awX'
baidu_SECRET_KEY='gIBvaHj2L1LAibynafncsNgB'

#请提前创建两个格式为mp3的文件

baidu_aipSpeech=AipSpeech(baidu_APP_ID,baidu_API_KEY,baidu_SECRET_KEY)

#在可选的参数中对语速，音量，人声进行调整，这里采用‘per’参数为1，表示女声
result = baidu_aipSpeech.synthesis(text = '树莓派语音合成', 
                            options={'spd':5,'vol':9,'per':0,})
#将合成的语音保存为文件
if not isinstance(result,dict):
    with open('1.mp3','wb') as f:
        f.write(result)
else:print(result)

#在可选的参数中对语速，音量，人声进行调整，这里采用‘per’参数为1，表示男声
result = baidu_aipSpeech.synthesis(text = '树莓派语音合成', 
                            options={'spd':5,'vol':9,'per':1,})
#将合成的语音保存为文件
if not isinstance(result,dict):
    with open('2.mp3','wb') as f:
        f.write(result)
else:print(result)

#使用playsound播放，注意路径名不能有中文
playsound("1.mp3")
playsound("2.mp3")
