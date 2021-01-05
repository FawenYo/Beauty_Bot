import sys
from linebot.models import FlexSendMessage

sys.path.append("..")
import config


class Templates:
    def beauty(self, articles):
        contents = {
            "type": "carousel",
            "contents": [],
        }
        for each in articles:
            content = beauty_info(article=each)
            contents["contents"].append(content)
        message = FlexSendMessage(alt_text="表特版內容", contents=contents)
        return message


def beauty_info(article):
    content = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "image",
                    "url": article["images"][0],
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "2:3",
                    "gravity": "top",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": article["title"],
                                    "size": "xl",
                                    "color": "#ffffff",
                                    "weight": "bold",
                                }
                            ],
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "filler"},
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {"type": "filler"},
                                        {
                                            "type": "text",
                                            "text": "查看文章",
                                            "color": "#ffffff",
                                            "flex": 0,
                                            "offsetTop": "-2px",
                                        },
                                        {"type": "filler"},
                                    ],
                                    "spacing": "sm",
                                    "action": {
                                        "type": "uri",
                                        "label": "action",
                                        "uri": f"{config.PTT_URL}{article['href']}",
                                    },
                                },
                                {"type": "filler"},
                            ],
                            "borderWidth": "1px",
                            "cornerRadius": "4px",
                            "spacing": "sm",
                            "borderColor": "#ffffff",
                            "margin": "xxl",
                            "height": "40px",
                        },
                    ],
                    "position": "absolute",
                    "offsetBottom": "0px",
                    "offsetStart": "0px",
                    "offsetEnd": "0px",
                    "backgroundColor": "#03303Acc",
                    "paddingAll": "20px",
                    "paddingTop": "18px",
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{article['push_count']}推",
                            "color": "#ffffff",
                            "align": "center",
                            "size": "xs",
                            "offsetTop": "3px",
                        }
                    ],
                    "position": "absolute",
                    "cornerRadius": "20px",
                    "offsetTop": "18px",
                    "backgroundColor": "#ff334b",
                    "offsetStart": "18px",
                    "height": "25px",
                    "width": "53px",
                },
            ],
            "paddingAll": "0px",
        },
    }
    return content
