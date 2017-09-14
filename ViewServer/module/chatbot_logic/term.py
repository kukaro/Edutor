from module.utils.term.term_slate import get_slate
from module.utils.term.term_toHTML import get_toHTML
from module.utils.term.term_crolling import get_term
from module.utils.dialog import byteArrayToStr
from flask import session
import json
import urllib
from module.utils.term_crolling import get_term
from module.utils.term_slate import get_slate


def term(msg):
    result_crolling = get_term(msg)
    term_title = result_crolling['term_title']
    term_url = result_crolling['term_url']
    filename = result_crolling['filename']
    print('Enter Term Dialog :')
    print('term_title : ' + term_title)
    print('term_url : ' + term_url)
    if result_crolling['success'] == 'ok':
        get_slate(term_title, term_url)
        get_toHTML(term_title)
        return filename


def get_term_ready(dialog, filename):
    OK_BOX = ['ㅇㅇ', '응', '칠게', '시작', '고고', '치겠습니다', '하겠습니다', '네', '예']
    print('Get Term Ready : ')
    print(filename)
    for OK_sign in OK_BOX:
        if dialog.find(OK_sign) >= 0:
            data = get_subject(filename)
            return {'sign': True, 'subject': data['subject'], 'termCount': data['termCount']}
    return {'sign': False}


def get_subject(filename):
    if filename.find('국어') >= 0:
        if filename.find('외국어') >= 0:
            return {'subject': '외국어', 'termCount': 50}
        return {'subject': '국어', 'termCount': 50}
    elif filename.find('영어') >= 0:
        return {'subject': '영어', 'termCount': 50}
    elif filename.find('수학') >= 0:
        return {'subject': '수학', 'termCount': 10}
    elif filename.find('화학') >= 0:
        return {'subject': '화학', 'termCount': 50}
    elif filename.find('물리') >= 0:
        return {'subject': '물리', 'termCount': 50}
    elif filename.find('생물') >= 0:
        return {'subject': '생물', 'termCount': 50}
    elif filename.find('지구과학') >= 0:
        return {'subject': '지구과학', 'termCount': 50}


def get_term_input(dialog):
    print('Start Get Term Input')
    if dialog.find('번') >= 0:
        dialogList = dialog.split(' ')
        number = dialogList[0][:-1]
        ans = dialogList[1]
        return {'number': number, 'ans': ans}
    elif dialog.find('채점') >= 0 or dialog.find('완료') or dialog.find('제출') >= 0:
        return {'marking': True}
    else:
        return {'dialog': '잘못된 명령입니다.', 'callState': 'testTermOK'}


def marking_term(msg):
    termArr = []
    filename = byteArrayToStr(msg['filename'])
    subject = byteArrayToStr(msg['subject'])
    termCount = byteArrayToStr(msg['termCount'])
    for termEle in msg['termArr']:
        termArr.append(byteArrayToStr(termEle))
    print(termArr)
    print(session)
    data = {'email': session['email'], 'subject': subject, 'termCount': termCount, 'filename': filename}
    jsonData = bytes(json.dumps(data).encode())
    req = urllib.request.Request("http://localhost:5001/answer", data=jsonData)
    req.get_method = lambda: 'post'
    jsonResult = urllib.request.urlopen(req).read()
    result = json.loads(jsonResult.decode())
    print(result)
    print('Enter Term Dialog :')
    print('term_title' + term_title)
    print('term_url' + term_url)
    if result_crolling['success'] == 'ok':
        term_title = get_slate(term_title, term_url)
