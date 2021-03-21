#coding:utf-8
#公众号：覃原
#利用百度AI平台实现在线语音识别，并输出语音文字

from aip import AipSpeech
from playsound import playsound
import time
import sys
import json
import base64

#请自己注册百度AI平台账号，然后创建语音合成项目，输入对应的密码
baidu_APP_ID='282434'
baidu_API_KEY='ohPlePZ95GdEF1w6awX'
baidu_SECRET_KEY='gI8ZBvaXHj2L1Ai3hbynEafcsNB'
client=AipSpeech(baidu_APP_ID,baidu_API_KEY,baidu_SECRET_KEY)

# 读取文件
def get_file(filepath):
    with open(filepath, 'rb') as f:
        return f.read()
# ##################
# 语音识别标准版
# ##################
def stt_1(filepath):
    try:
        # 对刚刚的合成的语音进行识别提取出文字
        result = client.asr(get_file(filepath),
                            # 语音文件格式
                            'wav',
                            # 采样率，16000、8000，固定值
                            16000,
                            # dev_pid参数表示识别的语言类型;1537：普通话；1837：四川话，更多请看百度SDK文件
                            {'dev_pid': 1537, } 
                            )
        # 判断百度语音识别是否成功
        if result['err_msg'] == 'success.':
            key = result['result'][0]
            # 将字符串转为bytes
            key_word = key.encode('utf8')
            # 一个汉字占3 bytes，减去最后一个句号并转换为str
            return ((key_word[:(len(key_word)-3)]).decode('utf8'))
        else:
            print("错误")
    except KeyError:
        print("KeyError")
        
# ##################
# 语音识别极速版
# ##################
import sys
import json
import base64
import time

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    timer = time.perf_counter
else:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
    if sys.platform == "win32":
        timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        timer = time.time

API_KEY = 'ohDPle9S5GdEjwH96awX'
SECRET_KEY = 'gI8ZBvuHj2L1LAi3hn9EafsNgB'

# 需要识别的文件
# AUDIO_FILE = 'input.wav'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
# 文件格式
FORMAT = 'wav' #AUDIO_FILE[-3:]  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
#  随便填
CUID = 'raspberry'
# 采样率
RATE = 16000  # 固定值

# 普通版
# DEV_PID = 1537  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
# ASR_URL = 'http://vop.baidu.com/server_api'
# SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有

#测试自训练平台需要打开以下信息， 自训练平台模型上线后，您会看见 第二步：“”获取专属模型参数pid:8001，modelid:1234”，按照这个信息获取 dev_pid=8001，lm_id=1234
# DEV_PID = 8001 ;   
# LM_ID = 1234 ;

# 极速版 打开注释的话请填写自己申请的appkey appSecret ，并在网页中开通极速版（开通后可能会收费）
DEV_PID = 80001
ASR_URL = 'http://vop.baidu.com/pro_api'
SCOPE = 'brain_enhanced_asr'  # 有此scope表示有极速版能力，没有请在网页里开通极速版

# 忽略scope检查，非常旧的应用可能没有
# SCOPE = False

class DemoError(Exception):
    pass

"""  TOKEN start """
TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'

def fetch_token():
    params = {'grant_type': 'client_credentials',
            'client_id': API_KEY,
            'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        #1 print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    #1 print(result_str)
    result = json.loads(result_str)
    #1 print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        #1 print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

"""  TOKEN end """

def stt_2(AUDIO_FILE) :
    try :
        token = fetch_token()
        """
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        opener = urllib2.build_opener(httpHandler)
        urllib2.install_opener(opener)
        """
        speech_data = []
        with open(AUDIO_FILE, 'rb') as speech_file:
            speech_data = speech_file.read()
        length = len(speech_data)
        if length == 0:
            raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)

        params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID}
        #测试自训练平台需要打开以下信息
        #params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID, 'lm_id' : LM_ID}
        params_query = urlencode(params)

        headers = {
            'Content-Type': 'audio/' + FORMAT + '; rate=' + str(RATE),
            'Content-Length': length
        }
        url = ASR_URL + "?" + params_query
        #1 print("url is", url)
        #1 print("header is", headers)
        # print post_data
        req = Request(ASR_URL + "?" + params_query, speech_data, headers)
        try:
            begin = timer()
            f = urlopen(req)
            result_str = f.read()
            #print("Request time cost %f" % (timer() - begin))
        except  URLError as err:
            #1 print('asr http response http code : ' + str(err.code))
            result_str = err.read()
        # json转为字典
        result_dic = json.loads(result_str)
        # 对返回结果进行检测
        if result_dic['err_msg'] == 'success.':
            # 提取出result的键值（str)
            key = result_dic['result'][0]
            # 将字符串转为bytes
            key_word = key.encode('utf8')
            # 一个汉字占3 bytes，减去最后一个句号并转换为str
            return ((key_word[:(len(key_word)-3)]).decode('utf8'))
        else:
            print("错误")
    except KeyError:
        print("KeyError")


# 标准版测试
time1 = time.time()
key_word = stt_1("demo.wav")
time2 = time.time()-time1
print("标准版：%s" % key_word ,"\n时间：%.3fs" % time2)
# 极速版测试
time1 = time.time()
key_word = stt_2("demo.wav")
time2 = time.time()-time1
print("极速版：%s" % key_word ,"\n时间：%.3fs" % time2)
