import re
import sys
import pickle

from redis import StrictRedis
import requests
from bs4 import BeautifulSoup
import urllib.request

titleList = []
urlList = []
solutionList = []


class EBS:
    def __init__(self):
        self.session = requests.Session()

    def login(self, id, pw):
        url = 'https://www.ebsi.co.kr/ebs/pot/potl/SSOLoginSubmit.ebs'
        data = {
            'destination': '/index.jsp',
            'userid': id,
            'passwd': pw,
            'ip_security': 'off'
        }

        r = self.session.post(url, data=data)
        return r.url == 'http://www.ebsi.co.kr/index.jsp'

    def get_list(self, year, page=1, page_size=10):
        url = 'http://www.ebsi.co.kr/ebs/xip/xipc/previousPaperListAjax.ebs'
        data = {
            'page': page,
            'order': '1',
            'yearNum': year,
            'targetCd': 'D300',
            'pageSize': page_size,
            'month1': '',
            'month2': '',
            'month3': '',
            'month4': '',
            'month5': '',
            'month6': '',
            'month7': '',
            'month8': '',
            'month9': '',
            'month10': '',
            'month11': '',
            'month12': '',
            'setSubjectList': '',
        }

        r = self.session.post(url, data=data)

        if '등록된 시험지가 없습니다.' in r.text:
            raise Exception('존재하지 않는 페이지입니다.')

        soup = BeautifulSoup(r.text, 'html.parser')

        component_re = re.compile(r"'(.+?)'")

        for row in soup.find('table', class_='boardtest').find_all('tr'):
            if row.find('td', 't_info'):
                title = row.find('td', 't_info').strong.get_text(strip=True)
                javascript = row.find('td', 'down').a['href']

                wordList = title.split(" ")
                if title.find('대학수학능력시험') != -1:
                    term_title = wordList[0] + '도 ' + wordList[3] + ' 수능기출문제'
                elif title.find('수능') != -1:
                    term_title = wordList[0] + '도 ' + wordList[5] + ' 수능기출문제'
                else:
                    term_title = wordList[0] + '도 ' + wordList[2] + ' ' + wordList[4] + ' 모의고사'

                if row.find('td', 'down').find_all('a')[1].text == '해설':
                    s_javascript = row.find('td', 'down').find_all('a')[1]['href']
                else:
                    s_javascript = row.find('td', 'down').find_all('a')[2]['href']

                base_url = 'http://wdown.ebsi.co.kr/W61001/01exam'

                download_link, *_, file_type = component_re.findall(javascript)
                download_link = '{}{}'.format(base_url, download_link)

                solution_download_link, *_, solution_file_type = component_re.findall(s_javascript)
                solution_download_link = '{}{}'.format(base_url, solution_download_link)

                titleList.append(term_title)
                urlList.append(download_link)
                solutionList.append(solution_download_link)

                # print('-' * 80)

        return titleList, urlList, solutionList

    '''
        def get_list(self, year, page=1, page_size=10):
            global titleList
            global urlList
            global solutionList
            titleList = []
            urlList = []
            solutionList = []
            url = 'http://www.ebsi.co.kr/ebs/xip/xipc/previousPaperListAjax.ebs'
            data = {
                'page': page,
                'order': '1',
                'yearNum': year,
                'targetCd': 'D300',
                'pageSize': page_size,
                'month1': '',
                'month2': '',
                'month3': '',
                'month4': '',
                'month5': '',
                'month6': '',
                'month7': '',
                'month8': '',
                'month9': '',
                'month10': '',
                'month11': '',
                'month12': '',
                'setSubjectList': '',
            }

            r = self.session.post(url, data=data)

            if '등록된 시험지가 없습니다.' in r.text:
                raise Exception('존재하지 않는 페이지입니다.')

            soup = BeautifulSoup(r.text, 'html.parser')

            component_re = re.compile(r"'(.+?)'")

            for row in soup.find('table', class_='boardtest').find_all('tr'):
                if row.find('td', 't_info'):
                    title = row.find('td', 't_info').strong.get_text(strip=True)
                    javascript = row.find('td', 'down').a['href']

                    wordList = title.split(" ")
                    if title.find('대학수학능력시험') != -1:
                        term_title = wordList[0] + '도 ' + wordList[3] + ' 수능기출문제'
                    elif title.find('수능') != -1:
                        term_title = wordList[0] + '도 ' + wordList[5] + ' 수능기출문제'
                    else:
                        term_title = wordList[0] + '도 ' + wordList[2] + ' ' + wordList[4] + ' 모의고사'

                    base_url = 'http://wdown.ebsi.co.kr/W61001/01exam'

                    download_link, *_, file_type = component_re.findall(javascript)
                    download_link = '{}{}'.format(base_url, download_link)

                    titleList.append(term_title)
                    urlList.append(download_link)

                    # print('-' * 80)

            return titleList, urlList
    '''


redis = StrictRedis()

# ebs = EBS()
# ebs.login('wlsgk0323', 'asdfgh369')

try:
    cookies = redis.get('ebs-cookies')
except:
    cookies = True

print(cookies)

ebs = EBS()
'''
if not cookies:
    if not ebs.login('wlsgk0323', 'asdfgh369'):
        print('Login failed.')
        sys.exit(1)

    redis.set('ebs-cookies', pickle.dumps(ebs.session.cookies._cookies), 60 * 30)
    print('Re-logged in')
else:
    ebs.session.cookies._cookies = pickle.loads(cookies)
    print('Loaded cookies')
'''


# def get_term(dialog):
#     for year in range(2006, 2018, 1):
#         page = 1
#         while True:
#             try:
#                 Listset = ebs.get_list(year, page)
#                 titleList = Listset[0]
#                 urlList = Listset[1]
#
#                 for i in titleList:
#                     term_title = titleList.pop()
#                     download_url = urlList.pop()
#
#                     if term_title.find(dialog) != -1:
#                         print(term_title)
#                         return term_title
#                     else:
#                         print(term_title)
#                         return 'not exist.'
#
#                         # filename = '/Users/limjinha/Desktop/testForder/' + wordList[0] + wordList[2] + wordList[4] + '.pdf'
#                         # urllib.request.urlretrieve(download_url, filename)
#             except:
#                 break
#             else:
#                 page += 1
#
#
# get_term('2015년2016대학수학능력시험국어')


def get_term(dialog):
    dialogList = dialog.split(" ")
    matched = re.match(r'^(\d+)년도$', dialogList[0])
    print('Enter Get Term Dialog:')
    print(dialogList)
    if not matched:
        return None

    year = int(matched.group(1))
    page = 1

    while True:
        try:
            Listset = ebs.get_list(year, page)
            titleList = Listset[0]
            urlList = Listset[1]
            solutionList = Listset[2]

            for i in range(len(titleList)):
                term_title = titleList[i]
                download_url = urlList[i]
                solution_download_url = solutionList[i]
                '''
                print('*****')
                print(i)

                print(term_title)
                print(download_url)
                '''
                if dialog.find('모의고사') != -1:
                    month = dialogList[1]
                    subject = dialogList[2]

                    if term_title.find(month) != -1 and term_title.find(subject) != -1:
                        print(term_title)
                        print(download_url)
                        filename = '/Users/jiharu/Desktop/' + term_title + '.pdf'
                        s_filename = '/Users/jiharu/Desktop/' + term_title + ' 해답.pdf'
                        urllib.request.urlretrieve(download_url, filename)
                        urllib.request.urlretrieve(solution_download_url, s_filename)
                        return {'success': 'ok', 'term_title': term_title, 'term_url': download_url,
                                'filename': filename}

                elif dialog.find('수능') != -1:
                    subject = dialogList[1]

                    if term_title.find(subject) != -1:
                        print(term_title)
                        print(download_url)
                        filename = '/Users/jiharu/Desktop/' + term_title + '.pdf'
                        s_filename = '/Users/jiharu/Desktop/' + term_title + ' 해답.pdf'
                        urllib.request.urlretrieve(download_url, filename)
                        urllib.request.urlretrieve(solution_download_url, s_filename)
                        return {'success': 'ok', 'term_title': term_title, 'term_url': download_url,
                                'filename': filename}



        except Exception as e:
            break
        else:
            page += 1
