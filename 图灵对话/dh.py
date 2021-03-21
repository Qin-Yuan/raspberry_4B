#coding:utf-8
#公众号：覃原
#利用图灵AI平台实现聊天功能

import requests
import json

def tuling(text):
    # 图灵网址
    tuling_url = 'http://www.tuling123.com/openapi/api/v2'
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    tuling_date = {
                # 输入类型：0-文本(默认)，1-图片，2-音频
                "reqType":0,   
                # 用户信息
                "perception": {
                    # 文本信息（非必须）
                    "inputText": {
                        # 直接输入文本，1-128字符
                        "text": text
                    },
                    '''
                    # 图片信息（非必须）
                    "inputImage": {
                        # 图片地址
                        "url": "imageUrl"
                    },
                    '''
                    # 客户端信息（非必须）
                    "selfInfo": {
                        "location": {
                            "city": "重庆",
                            "province": "重庆",
                            "street": "南岸"
                        }
                    }
                },
                # 用户参数(必须要自己修改)
                "userInfo": {
                    "apiKey": "a114ec54bbb88ee72123d71",
                    "userId": "6672"
                }
                }
    # 访问图灵，并得到回复结果，为json格式
    reply = requests.request("post",tuling_url,json=tuling_date,headers=headers)
    # 将json格式转为字典
    reply_dict=json.loads(reply.text)
    # 提取关键字
    key_word=reply_dict["results"][0]["values"]["text"]
    #  返回
    return key_word

# 调用示例
while True:
    text = input('请说：')
    print("回答:", tuling(text))
    
