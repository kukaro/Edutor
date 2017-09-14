import subprocess


def get_toHTML(term_title):
    pdf_file_name = '/Users/jiharu/Desktop/' + term_title + '.pdf'
    htmlR_file_name = '/Users/jiharu/Desktop/' + term_title + 'R.html'
    html_file_name = '/Users/jiharu/Desktop/' + term_title + '.html'
    jar_file_name = '/Users/jiharu/Desktop/PDFToHTML.jar'
    exec_file_name = '/Users/jiharu/Desktop/htmlRDelete.exec'
    subprocess.call('java -jar ' + jar_file_name + ' "' + pdf_file_name + '" "' + htmlR_file_name + '"', shell=True)
    subprocess.call(exec_file_name + ' "' + htmlR_file_name + '" "' + html_file_name + '"', shell=True)
