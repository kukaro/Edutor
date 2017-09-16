from module.utils.dialog import byteArrayToStr
from module.chatbot_logic.term import term, get_term_ready, get_term_input, marking_term, test_marking_term_math, \
    test_marking_term_kor, test_marking_term_eng
from flask_socketio import SocketIO, emit


def chatbot(msg):
    if 'dialog' in msg:
        dialog = byteArrayToStr(msg['dialog'])
    if 'callState' in msg:
        callState = byteArrayToStr(msg['callState'])
    if 'filename' in msg:
        filename = byteArrayToStr(msg['filename'])
    print(callState)
    print('Inner Chatbot : ')
    print(filename)
    # check state
    if callState == 'termTest':
        caller = get_term_ready(dialog, filename)
        if caller['sign']:
            print(caller['subject'])
            print(caller['termCount'])
            return {
                'dialog': '그럼 시험을 시작하겠습니다. 과목은 ' + caller['subject'] + '입니다. 총' + str(
                    caller['termCount']) + '문제 입니다. 문제의 입력은 \'n번 m\'같은 형식으로 입력하시면됩니다.'
                                           '채점시에는 \'채점\' 혹은 \'완료\'라고 입력하시면 됩니다.',
                'callState': 'testTermOK', 'subject': caller['subject'], 'termCount': str(caller['termCount'])}
        return {'dialog': '그럼 문제를 일단 저장해두겠습니다. 다음부터 동일 문제의 조회가 빨라집니다', 'callState': 'None'}
    elif callState == 'testTermOK':
        data = get_term_input(dialog)
        return data
    elif callState == 'testTermMarking':
        if 'test' in msg:
            if msg['test'] == True:
                if msg['sub'] == 'math':
                    data = test_marking_term_math(msg)
                elif msg['sub'] == 'kor':
                    data = test_marking_term_kor(msg)
                elif msg['sub'] == 'eng':
                    data = test_marking_term_eng(msg)
            else:
                data = marking_term(msg)
        else:
            data = marking_term(msg)
        print(data)
        return {'dialog': '채점이 완료되었습니다.<br>이번 시험의 점수는 ' + str(data['total']) + '입니다.<br>등급은 ' + str(
            data['grade']) + '등급 입니다', 'callState': 'myPage', 'data': data}
    # check None state
    if dialog.find('상황') >= 0 or dialog.find('점수') >= 0 or dialog.find('정보') >= 0:
        return {'dialog': '개인 정보를 불러 오겠습니다.', 'callState': 'myPage'}
    elif dialog.find('한준') >= 0:
        return {'dialog': '회장님', 'callState': 'None'}
    elif dialog.find('진하') >= 0:
        return {'dialog': '임지짜입니다', 'callState': 'None'}
    elif dialog.find('현영') >= 0:
        return {'dialog': '안마노예', 'callState': 'None'}
    elif dialog.find('모의고사') >= 0 or dialog.find('수능') >= 0:
        filename = term(dialog)
        print('filename : ')
        print(filename)
        emit('loadTerm', {'filename': filename})
        return {'dialog': '문제를 가져왔습니다.', 'callState': 'None', 'filename': filename}
    else:
        return {'dialog': '무슨 말인지 모르겠습니다.', 'callState': 'None'}
