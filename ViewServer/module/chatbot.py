from module.utils.dialog import byteArrayToStr
from module.chatbot_logic.term import term


def chatbot(msg):
    dialog = byteArrayToStr(msg)
    if dialog.find('한준') >= 0:
        return '회장님'
    elif dialog.find('진하') >= 0:
        return '임지짜입니다'
    elif dialog.find('현영') >= 0:
        return '안마노예'
    elif dialog.find('모의고사') >= 0 or dialog.find('수능') >= 0:
        term(dialog)
        return '모의고사 기출문제 가져오겠습니다.'
    else:
        return '무슨 말인지 모르겠습니다.'


'''
2016년도 10월 국어 모의고사
'''
