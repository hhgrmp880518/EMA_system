from __future__ import unicode_literals
import execjs
import math
import requests, json
import threading, time
import os
import unicodedata
from explanatoryTool import*
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from configparser import ConfigParser


require_list = {}

class media_data():
    def __init__(self, text: str, post_time: float, StepsText: list, finish: bool=False):
        self.text = text
        self.StepsText = StepsText
        self.post_time = post_time
        finish = False

class hintcolors:
    Success = '\033[1;38;5;81m[Success] \033[0m'
    Clear = '\033[1;38;5;226m[Clear] \033[0m'
    Failed = '\033[1;38;5;196m[Failed] \033[0m'

# 導入 .js
def js_from_file(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result

# EMA 動畫產生器
class animation(explanatoryTools):
    def construct(self):
        StepsText = list(require_list.values())[0].StepsText
        size = list(range(math.ceil(len(StepsText)**0.5)))
        locate = []
        unit_height = (config.frame_height-1.5)/len(size)
        unit_width = config.frame_width/len(size)
        for i in size:
            for j in size:
                locate.append([0.5+unit_width*i, 2.5+unit_height*j])
        length = unit_width-1
        question = list(require_list.values())[0].text
        self.ask(question, position=[4, 0.5, 0], font_size=36, bold=True)
        
        for i in range(len(StepsText)):
            command = StepsText[i][0]
            nums = StepsText[i][1]

            if command == 'add':
                self.numberLineAdd(nums[0], nums[1], position=[locate[i][0], locate[i][1], 0.0], length=length)
            elif command == 'sub':
                self.numberLineSub(nums[0], nums[1], position=[locate[i][0], locate[i][1], 0.0], length=length)
            elif command == 'mul':
                if nums[1] < 11:
                    self.numberLineMul(nums[0], nums[1], position=[locate[i][0], locate[i][1], 0.0], length=length)
                else:
                    1+'1'
            elif command == 'ans':
                self.ans(nums[0], position=[locate[i][0], locate[i][1], 0.0])
        self.wait(5)
        print('good')

# EMA 封面產生器
class image(explanatoryTools):
    def construct(self):
        title = list(require_list.values())[0].text
        if len(title) <11:
            scale = 1 
            scale = math.sqrt((12/(len(title)+2)))
        self.title(title, font_size=96*scale, bold=True)
        print('good')

# 將Flask框架導向目前運行程式的位置
app = Flask(__name__)

# 設定 Channel Access Token 與 Channel Secret
# 設定檔是 config.ini
line_bot_config = ConfigParser()
line_bot_config.read('config.ini')
line_bot_api = LineBotApi(line_bot_config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(line_bot_config.get('line-bot', 'channel_secret'))
WebhookUrl = line_bot_config.get('line-bot', 'webhook_url')

# 建立 "/callback" 的路由被訪問的行為
@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature 頭部 (header) 資訊
    signature = request.headers['X-Line-Signature']
    
    # 取得 HTTP 請求的內容
    body = request.get_data(as_text=True)

    # 紀錄 HTTP 請求的內容
    app.logger.info("Request body: " + body)
    
    try:
        #print('body:{}\nsignature:{}'.format(body, signature))
        # 使用 handler 處理訊息
        handler.handle(body, signature)
    
    # 若驗證簽章失敗，則回應狀態碼 400
    except InvalidSignatureError:
        abort(400)

    # 回傳狀態碼 200，表示處理成功
    return 'OK'

# 當接收到文字訊息時，進行 quick_reply() 函式
@handler.add(MessageEvent, message=TextMessage)
def quick_reply(event):

    # 如果使用者不是連線測試，則將使用者的訊息記錄在 require_list 中
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.source.user_id in list(require_list.keys()):
            # 回覆提醒使用者不要連續要求
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='前一部影片還沒生成完畢\n稍後再傳新的問題')
            )
        else:
            try:
                mathsteps = execjs.compile(js_from_file('./mathsteps.js'))
                text = unicodedata.normalize('NFKC', event.message.text)
                StepsText = mathsteps.call('steps', text)
                text = text.replace('*','×').replace('-','−').replace(' ','')+' = ?'
                require_list[event.source.user_id] = media_data(text, time.time(), StepsText)

                # 回覆使用者正在產生影片
                if len(list(require_list.keys())) < 3:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='影片產生中，請等一下')
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='目前等待生成的影片繁多，請等一下')
                    )
            except:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='輸入的資料暫時不支援生成')
                )

# 渲染 EMA 封面和動畫
def EMA_generator(user_id):
    
    # 設定 manim 的 config 選項
    config_dict = {
        'quality': 'medium_quality',
        'disable_caching': True,
        'video_dir': 'static',
        'images_dir': 'static',
        'output_file': user_id,
        'flush_cache': True,
    }

    # 使用指定的 manim 的 config 選項
    with tempconfig(config_dict):
        # 呼叫 image() 來產生 EMA 封面
        image1 = image()
        image1.render()  # 執行封面渲染

    # 使用指定的 manim 的 config 選項
    with tempconfig(config_dict):
        animation1 = animation()
        # 呼叫 animation() 來產生 EMA 動畫
        animation1.render()  # 執行動畫渲染

if __name__ == '__main__':
    # 將 LINE Bot 的應用放入執行緒獨立運作
    line_bot = threading.Thread(target=app.run)
    line_bot.start()

    while True:
        if require_list != {}:
            # 抓取使用者資料 (user_id)、題目輸入(text)
            user_id = list(require_list.keys())[0]
            text = require_list[user_id].text
            StepText = require_list[user_id].StepsText
            print('\033[1;38;5;82m[START] \033[0muser_id:{}, text:{}'.format(user_id, text))
            try:
                # 製作 EMA 封面和動畫
                EMA_generator(user_id)

                # 傳送設定
                headers = {'Authorization':'Bearer {}'.format(line_bot_config.get('line-bot', 'channel_access_token')),
                        'Content-Type':'application/json'}
                body = {'to':user_id,
                        'messages':[{"type": "video", "originalContentUrl": "{}/static/{}.mp4".format(WebhookUrl, user_id), "previewImageUrl": "{}/static/{}.png".format(WebhookUrl, user_id)}]}
                
                # 傳送 EMA 檔案
                requests.request('POST', 'https://api.line.me/v2/bot/message/push',
                                headers=headers,
                                data=json.dumps(body).encode('utf-8'))

                print('{}user_id:{}, text:{}'.format(hintcolors.Success, user_id, text))
                # 清除已完成的要求
                require_list.pop(user_id)
                print('{}user_id:{}, text:{}'.format(hintcolors.Clear, user_id, text))
            except:
                headers = {'Authorization':'Bearer {}'.format(line_bot_config.get('line-bot', 'channel_access_token')),
                        'Content-Type':'application/json'}
                body = {'to':user_id,
                        'messages':[{"type": "text", "text": "😢對不起，\n　我們遇到了預期外的錯誤\n\n⚠️暫時不要傳送相同題目⚠️\n\n如果您願意回報異常情形給開發團隊，請填寫以下表單：\n🔗https://forms.gle/LsX35K63vBwTyHQC8"}]}
                
                # 傳送 EMA 檔案
                requests.request('POST', 'https://api.line.me/v2/bot/message/push',
                                headers=headers,
                                data=json.dumps(body).encode('utf-8'))
                print('{}user_id:{}, text:{}'.format(hintcolors.Failed, user_id, text))
                require_list.pop(user_id)
                print('{}user_id:{}, text:{}'.format(hintcolors.Clear, user_id, text))

            print(require_list)
        else:
            # 等待 1 秒
            time.sleep(1)