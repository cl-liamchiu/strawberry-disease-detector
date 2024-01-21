from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, VideoMessage, AudioMessage, FileMessage, LocationMessage, StickerMessage,
                            FlexSendMessage, PostbackEvent, QuickReply, QuickReplyButton, CameraAction, CameraRollAction, TemplateSendMessage, PostbackTemplateAction, MessageTemplateAction, ConfirmTemplate)
import time
import torch
import configparser
import pymongo

from functions.flexmessage import get_front_or_back_flex, get_all_diseases_flex, get_one_disease_flex, get_contact_info_flex
from functions.model_identify import front_model_identify, back_model_identify

config = configparser.ConfigParser()
config.read("config.ini")

# input your channel access token
line_bot_api = LineBotApi(config.get('LINEBot', 'channel_access_token'))
# input your channel secret
handler = WebhookHandler(config.get('LINEBot', 'channel_secret'))

app = Flask(__name__)

# input your https url create by ngrok
url_basis = config.get('LINEBot', 'url_basis')

client = pymongo.MongoClient(
    "...")

db = client['MongoClient']
col = db['Database']


@app.route("/", methods=['POST', 'GET'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    body_dict = eval(body.replace('false', 'False'))

    call_back_data = body_dict["events"][0]
    print("new_turn---------------------------------------------------\n")
    print("Request body: " + body, "\n")

    if 'postback' in call_back_data:
        print("Data: ", call_back_data, "\n")
        user_id = call_back_data['source']['userId']
        my_query = {'source': {'type': 'user', 'userId': user_id}}
        if col.find_one(my_query) == None:
            col.insert_one(call_back_data)
        else:
            new_values = {"$set": {"postback": {
                "data": call_back_data['postback']['data']}}}
            col.update_one(my_query, new_values)

    print(col.count_documents({}))
    for i in col.find():
        print(i, "\n")

    # handle webhook body, make sure the message was from LINE by using the channel secret
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

 # handle Message Event / Text message


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text

    if message == "如何使用":
        print("how to use")
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="為了避免小幫手預測錯誤，拍照時或者照片要上傳時，要先確認葉子在照片的正中間哦～\n範例如下："),
             ImageSendMessage(
                original_content_url=url_basis + "chatbot_default_images/how_example_1.jpg",
                preview_image_url=url_basis + "chatbot_default_images/how_example_1.jpg"),
             ImageSendMessage(
                original_content_url=url_basis + "chatbot_default_images/how_example_2.jpg",
                preview_image_url=url_basis + "chatbot_default_images/how_example_2.jpg"),
             TextSendMessage(text="使～用～小～技～巧～"),
             TextSendMessage(
                 text="技巧一：如果葉子兩面都有病害或蟲害，拍完正面也可以接著拍背面。\n技巧二：如果怕辨識結果不準確，可以多上傳幾張相同病蟲害照片來辨識。\n技巧三：如果覺得辨識結果有問題的話，可以聯絡專業人員。")
             ])

    elif message == "我要查看病蟲害資訊":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="可辨識的病害蟲害"),
             FlexSendMessage(alt_text="請查看訊息", contents=get_all_diseases_flex(url_basis))])

    elif message == "我要拍照":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="你要拍攝葉片正面還是葉片背面?"),
             FlexSendMessage(alt_text="請查看訊息", contents=get_front_or_back_flex('camera', url_basis))])

    elif message == "我要選擇照片":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="你要選擇葉片正面還是葉片背面?"),
             FlexSendMessage(alt_text="請查看訊息", contents=get_front_or_back_flex('photo', url_basis))])

    elif message == "我要聯絡專業人員":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="專業人員聯絡資訊"),
             FlexSendMessage(alt_text="請查看訊息", contents=get_contact_info_flex(url_basis))])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="有任何問題可以聯絡專業人員哦～"),
             TextSendMessage(text="專業人員聯絡資訊"),
             FlexSendMessage(alt_text="請查看訊息", contents=get_contact_info_flex(url_basis))])

# handle Message Event / Image message


@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    # get image from LINE Server
    message_content = line_bot_api.get_message_content(event.message.id)
    name = "{}".format(time.time())
    imgname = name + '.jpg'
    img_path = "./static/received_images/" + imgname
    # save image to local
    with open(img_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    user_id = event.source.user_id
    print("this is user_id: ", user_id)
    my_query = {'source': {'type': 'user', 'userId': user_id}}
    data = col.find(my_query)[0]['postback']['data']
    print(data)

    if data == 'photo_front':
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="辨識完成！"),
             FlexSendMessage(
                alt_text="請查看訊息",
                contents=get_one_disease_flex(
                    front_model_identify(img_path), url_basis)),
             TextSendMessage(text="目前為正面葉片辨識模式...",
                             quick_reply=QuickReply(items=[
                                 QuickReplyButton(action=CameraRollAction(label="開啟相簿"))]))])

    elif data == 'camera_front':
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="辨識完成！"),
             FlexSendMessage(
                alt_text="請查看訊息",
                contents=get_one_disease_flex(
                    front_model_identify(img_path), url_basis)),
             TextSendMessage(text="目前為正面葉片辨識模式...",
                             quick_reply=QuickReply(items=[
                                 QuickReplyButton(action=CameraAction(label="開啟相機"))]))])
    
    elif data == 'photo_back':
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="辨識完成！"),
             FlexSendMessage(
                alt_text="請查看訊息",
                contents=get_one_disease_flex(
                    back_model_identify(img_path), url_basis)),
             TextSendMessage(text="目前為背面葉片辨識模式...",
                             quick_reply=QuickReply(items=[
                                 QuickReplyButton(action=CameraRollAction(label="開啟相簿"))]))])

    elif data == 'camera_back':
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="辨識完成！"),
             FlexSendMessage(
                alt_text="請查看訊息",
                contents=get_one_disease_flex(
                    back_model_identify(img_path), url_basis)),
             TextSendMessage(text="目前為背面葉片辨識模式...",
                             quick_reply=QuickReply(items=[
                                 QuickReplyButton(action=CameraAction(label="開啟相機"))]))])


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data

    if 'camera' in data:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請拍攝葉片",
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=CameraAction(label="開啟相機"))])))
    elif 'photo' in data:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請挑選照片",
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=CameraRollAction(label="開啟相簿"))])))


if __name__ == "__main__":
    # run the server at localhost:5000
    app.run(debug=False, host="127.0.0.1", port=5000)
