from module.utils.dialog import byteArrayToStr


def chatbot(msg):
    dialog = byteArrayToStr(msg)
    if dialog.find('한준') > 0:
        return '회장님'
    elif dialog.find('진하') > 0:
        return '임지짜입니다'
    elif dialog.find('현영') > 0:
        return '안마노예'
    else:
        return '무슨 말인지 모르겠습니다.'
