import sys

from fastapi import APIRouter, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

sys.path.append(".")
import config
from line.templates import Templates


line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

line_app = APIRouter()


@line_app.post("/callback")
async def callback(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()

    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameter")
    return "OK"


@handler.add(MessageEvent, message=(TextMessage,))
def handle_message(event):
    reply_token = event.reply_token
    user_message = event.message.text

    if isinstance(event.message, TextMessage):
        if "抽" in user_message:
            if "/" in user_message:
                push_filter = user_message.split("/")[1]
                if push_filter.isdigit():
                    if int(push_filter) > 99 or int(push_filter) < -10:
                        message = TextSendMessage(text="搜尋推文數只能在-10~99間！")
                    else:
                        articles = config.db.articles.aggregate(
                            [
                                {"$match": {"push_count": {"$gte": int(push_filter)}}},
                                {"$sample": {"size": 10}},
                            ]
                        )
                        message = Templates().beauty(articles=list(articles)[:10])
                else:
                    message = TextSendMessage(text="輸入內容非整數！")
            else:
                articles = config.db.articles.aggregate([{"$sample": {"size": 10}}])
                message = Templates().beauty(articles=list(articles)[:10])
            line_bot_api.reply_message(reply_token, message)
        elif "找/" in user_message:
            search_target = user_message.split("/")[1]
            articles = config.db.articles.aggregate(
                [
                    {"$match": {"title": {"$regex": search_target}}},
                    {"$sample": {"size": 10}},
                ]
            )
            message = Templates().beauty(articles=list(articles)[:10])
            line_bot_api.reply_message(reply_token, message)