import json
import urllib

from flask import session

from module.utils.dialog import byteArrayToStr
from module.utils.get_exam_crawling import get_s_data, get_m_data
from module.utils.term.term_crolling import get_term
from module.utils.term.term_slate import get_slate
from module.utils.term.term_toHTML import get_toHTML


def term(msg):
    result_crolling = get_term(msg)
    term_title = result_crolling['term_title']
    term_url = result_crolling['term_url']
    filename = result_crolling['filename']
    term_arr = term_title.split(' ')
    if term_arr[len(term_arr) - 1].find('수능') >= 0:
        year = term_arr[0]
        subject = term_arr[1]
        term_type = '수능'
    elif term_arr[len(term_arr) - 1].find('모의고사') >= 0:
        year = term_arr[0]
        month = term_arr[1]
        subject = term_arr[2]
        term_type = '모의고사'
    print('Enter Term Dialog :')
    print('result_crawling : ' + str(result_crolling))
    print('term_title : ' + term_title)
    print('term_url : ' + term_url)
    print('term_arr : ' + str(term_arr))
    if result_crolling['success'] == 'ok':
        get_slate(term_title, term_url)
        get_toHTML(term_title)
        if term_type == '수능':
            point_cut, wrong_answer = get_s_data(str(year[0:4]), str(subject))
            data = {'year': year, 'subject': subject, 'term_type': '수능', 'point_cut_dir': point_cut,
                    'wrong_answer_dir': wrong_answer}
            jsonData = bytes(json.dumps(data).encode())
            req = urllib.request.Request("http://localhost:5001/point-cut", data=jsonData)
            req.get_method = lambda: 'post'
            jsonResult = urllib.request.urlopen(req).read()
            result = json.loads(jsonResult.decode())

            req = urllib.request.Request("http://localhost:5001/wrong-answer", data=jsonData)
            req.get_method = lambda: 'post'
            jsonResult = urllib.request.urlopen(req).read()
            result = json.loads(jsonResult.decode())


        elif term_type == '모의고사':
            get_m_data(str(year[0:4]), str(month), subject)
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
    data = {'email': session['email'], 'subject': subject, 'termCount': termCount, 'filename': filename,
            'termArr': termArr}
    jsonData = bytes(json.dumps(data).encode())
    req = urllib.request.Request("http://localhost:5001/answer", data=jsonData)
    req.get_method = lambda: 'post'
    jsonResult = urllib.request.urlopen(req).read()
    result = json.loads(jsonResult.decode())
    print(result)
