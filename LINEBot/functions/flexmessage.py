diseases_name = ["anthracnose", "leaf_blight",
                 "angular_leaf_spot", "lepidoptera_larvae", "tetranychus"]

diseases_name_dict = {
    "anthracnose": "炭疽病",
    "leaf_blight": "葉枯病",
    "angular_leaf_spot": "角斑病",
    "lepidoptera_larvae": "鱗翅目幼蟲危害",
    "tetranychus": "葉蟎危害",
    "health_f": "健康正面葉片",
    "health_r": "健康背面葉片"
}


def get_diseases_photo(disease_name, url_basis):
    return f"{url_basis}chatbot_default_images/{disease_name}.jpg"


def get_all_diseases_flex(url_basis):
    all_dieseases_flex = {
        "type": "carousel",
        "contents": []
    }

    for disease_name in diseases_name:
        all_dieseases_flex["contents"].append(
            get_one_disease_flex(disease_name, url_basis))

    return all_dieseases_flex


def get_one_disease_flex(disease_name, url_basis):
    one_disease_flex = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "image",
                            "url": get_diseases_photo(disease_name, url_basis),
                            "gravity": "top",
                            "size": "full",
                            "aspectMode": "cover"
                        }
                    ],
                    "position": "relative"
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
                                    "text": diseases_name_dict[disease_name],
                                    "size": "xl",
                                    "color": "#ffffff",
                                    "weight": "bold",
                                    "align": "start"
                                }
                            ]
                        }
                    ],
                    "position": "relative",
                    "offsetBottom": "none",
                    "offsetStart": "none",
                    "offsetEnd": "none",
                    "backgroundColor": "#03303ACC",
                    "paddingAll": "20px",
                    "paddingTop": "18px",
                    "offsetTop": "none"
                }
            ],
            "paddingAll": "0px"
        }
    }

    return one_disease_flex


def get_front_or_back_flex(type, url_basis):
    if type == 'camera':
        text = '我要拍'
    else:
        text = '我要選擇'

    front_or_back_flex = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "image",
                                    "url": f"{url_basis}chatbot_default_images/health_f.jpg",
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "3:4"
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
                                                    "text": "正面",
                                                    "align": "center",
                                                    "color": "#FFFFFF"
                                                }
                                            ],
                                            "borderWidth": "1px",
                                            "borderColor": "#FFFFFF",
                                            "cornerRadius": "4px",
                                            "margin": "none",
                                            "spacing": "none",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "width": "100px",
                                            "offsetStart": "16px"
                                        }
                                    ],
                                    "position": "absolute",
                                    "offsetBottom": "none",
                                    "offsetStart": "none",
                                    "offsetEnd": "none",
                                    "paddingAll": "8px",
                                    "backgroundColor": "#03303ACC",
                                    "spacing": "sm",
                                    "margin": "xxl",
                                    "height": "40px"
                                }
                            ],
                            "action": {
                                "type": "postback",
                                "label": "front",
                                "data": f"{type}_front",
                                "displayText": f"{text}正面"
                            }
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "image",
                                    "url": f"{url_basis}chatbot_default_images/health_r.jpg",
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "3:4"
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
                                                    "text": "背面",
                                                    "align": "center",
                                                    "color": "#FFFFFF"
                                                }
                                            ],
                                            "borderWidth": "1px",
                                            "borderColor": "#FFFFFF",
                                            "cornerRadius": "4px",
                                            "margin": "none",
                                            "spacing": "none",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "width": "100px",
                                            "offsetStart": "16px"
                                        }
                                    ],
                                    "position": "absolute",
                                    "offsetBottom": "none",
                                    "offsetStart": "none",
                                    "offsetEnd": "none",
                                    "paddingAll": "8px",
                                    "backgroundColor": "#03303ACC",
                                    "spacing": "sm",
                                    "margin": "xxl",
                                    "height": "40px"
                                }
                            ],
                            "action": {
                                "type": "postback",
                                "label": "back",
                                "data": f"{type}_back",
                                "displayText": f"{text}背面"
                            },
                            "margin": "xs"
                        }
                    ]
                }
            ],
            "paddingAll": "none",
            "backgroundColor": "#03303ACC"
        }
    }

    return front_or_back_flex


def get_contact_info_flex(url_basis):

  contact_info_flex = {
  "type": "bubble",
  "size": "mega",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "image",
                "url": f"{url_basis}chatbot_default_images/person.png",
                "aspectMode": "cover",
                "size": "full"
              }
            ],
            "cornerRadius": "100px",
            "width": "72px",
            "height": "72px",
            "borderWidth": "1px",
            "borderColor": "#000000"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "contents": [
                  {
                    "type": "span",
                    "text": "Dr.Strawberry",
                    "weight": "bold",
                    "color": "#000000"
                  }
                ],
                "size": "sm",
                "wrap": True
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "1,140,753 Like",
                    "size": "sm",
                    "color": "#bcbcbc",
                    "contents": [
                      {
                        "type": "span",
                        "text": "Phone",
                        "style": "italic"
                      },
                      {
                        "type": "span",
                        "text": " "
                      },
                      {
                        "type": "span",
                        "text": "0987654321"
                      }
                    ]
                  }
                ],
                "spacing": "sm",
                "margin": "md"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "1,140,753 Like",
                    "size": "sm",
                    "color": "#bcbcbc",
                    "contents": [
                      {
                        "type": "span",
                        "text": "E-mail",
                        "style": "italic"
                      },
                      {
                        "type": "span",
                        "text": " "
                      },
                      {
                        "type": "span",
                        "text": "strawberry@gmail.com"
                      }
                    ],
                    "wrap": True
                  }
                ],
                "spacing": "sm",
                "margin": "md"
              }
            ]
          }
        ],
        "spacing": "xl",
        "paddingAll": "20px"
      }
    ],
    "paddingAll": "0px"
  }
}

  return contact_info_flex
