import slate
import codecs


def get_slate(term_title, term_url):

    # 경로 아마존 로컬로 다시 설정, txt는 hdfs로 저장 하던가
    pdf_file_name = '/Users/jiharu/Desktop/' + term_title + '.pdf'
    txt_file_name = '/Users/jiharu/Desktop/' + term_title + '.txt'

    with codecs.open(pdf_file_name, 'rb') as f:
        doc = slate.PDF(f)

    f = open(txt_file_name, "wt")

    for s in doc:
        f.write(s)

    f.close()

    return {'success': 'ok', 'term_title': term_title}

