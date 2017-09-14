import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

data = {
            'base_ExamPointCut_url': 'http://www.mimacstudy.com/mockTest/MCKmockAnalysisExamPointCut.ds?groupNo=',
            'base_ExamWrongAnswer_url': 'http://www.mimacstudy.com/mockTest/MCKmockAnalysisExamWrongAnswer.ds?groupNo=',

            's_url': 'http://www.mimacstudy.com/mockTest/UNmockAnalysisExamAnalysys.ds?groupNo=214&requestMenuId=MNMN_M009',
            'm_url': 'http://www.mimacstudy.com/mockTest/MCKmockAnalysisExamAnalysys.ds?requestMenuId=M000000044',

            '국어': '&grade=&examRelm=1#mainView',
            '수학가형': '&grade=&examRelm=2&examSubj=21#mainView',
            '수학나형': '&grade=&examRelm=2&examSubj=24#mainView',
            '영어': '&grade=&examRelm=3#mainView',
            '한국지리': '&grade=&examRelm=41&examSubj=4A#mainView',
            '세계지리': '&grade=&examRelm=41&examSubj=4B#mainView',
            '동아시아사': '&grade=&examRelm=41&examSubj=4E#mainView',
            '세계사': '&grade=&examRelm=41&examSubj=4F#mainView',
            '법과정치': '&grade=&examRelm=41&examSubj=4G#mainView',
            '생활과윤리': '&grade=&examRelm=41&examSubj=4H#mainView',
            '경제': '&grade=&examRelm=41&examSubj=4I#mainView',
            '사회문화': '&grade=&examRelm=41&examSubj=4J#mainView',
            '윤리와사상': '&grade=&examRelm=41&examSubj=4K#mainView',
            '물리': '&grade=&examRelm=42&examSubj=4L#mainView',
            '화학': '&grade=&examRelm=42&examSubj=4M#mainView',
            '생명과학': '&grade=&examRelm=42&examSubj=4N#mainView',
            '지구과학': '&grade=&examRelm=42&examSubj=4O#mainView',
            '물리2': '&grade=&examRelm=42&examSubj=4P#mainView',
            '화학2': '&grade=&examRelm=42&examSubj=4Q#mainView',
            '생명과학2': '&grade=&examRelm=42&examSubj=4R#mainView',
            '지구과학2': '&grade=&examRelm=42&examSubj=4S#mainView',
            '한국사': '&grade=&examRelm=6#mainView'
        }

def get_html(url, maxbuf=10485760):
    res = urlopen(url)
    html = res.read(maxbuf)
    res.close()
    return html

def get_s_data(year, subject):
    html = get_html(data['s_url'])
    soup = BeautifulSoup(html, "html.parser")

    for row in soup.find("div", class_="defarea").find("select").find_all("option"):
        name = row.text
        value = row['value']

        if name.find(year) != -1:
            ExamPointCut_url = data['base_ExamPointCut_url'] + value
            ExamWrongAnswer_url = data['base_ExamWrongAnswer_url'] + value + data[subject]

            print(name)
            print(ExamPointCut_url)
            print(ExamWrongAnswer_url)

            filename1 = '/Users/limjinha/Desktop/' + year + "년도 " + subject + " 수능 등급컷.csv"
            filename2 = '/Users/limjinha/Desktop/' + year + "년도 " + subject + " 수능 오답률.csv"
            getExamPointCut(year, '11월', subject, ExamPointCut_url, filename1)
            getExamWrongAnswer(year, '11월', subject, ExamWrongAnswer_url, filename2)
            break

def get_m_data(year, month, subject):
    html = get_html(data['m_url'])

    soup = BeautifulSoup(html, "html.parser")
    for row in soup.find("div", class_="defarea").find("select").find_all("option"):
        name = row.text
        value = row['value']

        if name.find(year) != -1 and name.find(month) != -1:
            ExamPointCut_url = data['base_ExamPointCut_url'] + value
            ExamWrongAnswer_url = data['base_ExamWrongAnswer_url'] + value + data[subject]

            print(name)
            print(ExamPointCut_url)
            print(ExamWrongAnswer_url)

            filename1 = '/Users/limjinha/Desktop/' + year + "년도 " + month + " " + subject + " 모의고사 등급컷.csv"
            filename2 = '/Users/limjinha/Desktop/' + year + "년도 " + month + " " + subject + " 모의고사 오답률.csv"
            getExamPointCut(year, month, subject, ExamPointCut_url, filename1)
            getExamWrongAnswer(year, month, subject, ExamWrongAnswer_url, filename2)

            break

def getExamPointCut(year, month, subject, ExamPointCut_url, filename):
    html = get_html(ExamPointCut_url)
    soup = BeautifulSoup(html, "html.parser")

    f = open(filename, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(['등급'.encode(), '원점수'.encode(), '표준점수'.encode(), '백분위'.encode()])
    for row in soup.find_all("div", class_="div430"):
        if row.div.h3.text.find(subject) != -1:
            for i in row.find("table", class_="scoretable").find_all('tr'):
                if i.find_all('td'):
                    print(i.find_all('td'))
                    rank = i.find_all('td')[0].text
                    o_score = i.find_all('td')[1].text
                    s_score = i.find_all('td')[2].text
                    percent = i.find_all('td')[3].text

                    wr.writerow([rank, o_score, s_score, percent])

def getExamWrongAnswer(year, month, subject, ExamWrongAnswer_url, filename):
    html = get_html(ExamWrongAnswer_url)
    soup = BeautifulSoup(html, "html.parser")

    f = open(filename, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow([
                '문항번호'.encode(), '배점'.encode(), '정답'.encode(), '오답률'.encode(),
                '정답률'.encode(), '선택비율1'.encode(), '선택비율2'.encode(), '선택비율3'.encode(),
                '선택비율4'.encode(), '선택비율5'.encode(), '난이도'.encode()
                 ])

    for row in soup.find("table").find_all('tr'):
        if row.find_all('td'):
            i = row.find_all('td')
            print(i)

            wr.writerow([i[0].text, i[1].text, i[2].text, i[3].text, i[4].text, i[5].text,
                         i[6].text, i[7].text, i[8].text, i[9].text, i[10].text])


# get_s_data('2016', '국어')