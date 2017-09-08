from module.utils.term_crolling import get_term
from module.utils.term_slate import get_slate


def term(msg):
    result_crolling = get_term(msg)
    term_title = result_crolling['term_title']
    term_url = result_crolling['term_url']
    print('Enter Term Dialog :')
    print('term_title' + term_title)
    print('term_url' + term_url)
    if result_crolling['success'] == 'ok':
        term_title = get_slate(term_title, term_url)
