# coding: utf-8

import HTMLParser

from re import compile as regexp_compile, DOTALL, escape


regexp_tags = regexp_compile(r'(<[ \t]*([a-zA-Z0-9!"./_-]*)[^>]*>)', flags=DOTALL)
regexp_comment = regexp_compile(r'<!--.*?-->', flags=DOTALL)
regexp_spaces_start = regexp_compile('([\n]+)[ \t]*',
        flags=DOTALL)
regexp_spaces_end = regexp_compile('[ \t]*\n', flags=DOTALL)
regexp_newlines = regexp_compile('[\n]{3,}', flags=DOTALL)
regexp_spaces = regexp_compile('[ \t]{2,}', flags=DOTALL)
regexp_punctuation = regexp_compile('[ \t]*([' + escape('!,.:;?') + '])',
        flags=DOTALL)
breakline_tags = ['table', '/table', 'tr', 'div', '/div', 'h1', '/h1', 'h2',
                  '/h2', 'h3', '/h3', 'h4', '/h4', 'h5', '/h5', 'h6', '/h6',
                  'br', 'br/']
double_breakline = ['table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
html_parser = HTMLParser.HTMLParser()

def clean(text):
    text = regexp_spaces_start.sub(r'\1', text)
    text = regexp_spaces_end.sub('\n', text)
    text = regexp_newlines.sub('\n\n', text)
    text = regexp_spaces.sub(' ', text)
    text = regexp_punctuation.sub(r'\1', text)
    return text.strip()

def parse_html(html, remove_tags=None, remove_inside=None,
               replace_space_with=' ', replace_newline_with='\n'):
    html = regexp_comment.sub('', html.replace('\n', ''))
    data = regexp_tags.split(html)
    content_between = data[::3]
    complete_tags = data[1::3]
    tag_names = [x.lower() for x in data[2::3]]
    for index, tag_name in enumerate(tag_names):
        if not tag_name.strip():
            continue
        search_tag = tag_name
        if tag_name and tag_name[0] == '/':
            search_tag = tag_name[1:]
        if remove_tags and search_tag not in remove_inside:
            if tag_name in breakline_tags:
                if search_tag in double_breakline:
                    complete_tags[index] = 2 * replace_newline_with
                else:
                    complete_tags[index] = replace_newline_with
            else:
                complete_tags[index] = replace_space_with
        if remove_inside and tag_name in remove_inside:
            remove_to = tag_names.index('/' + tag_name, index)
            total_to_remove = remove_to - index + 1
            complete_tags[index:remove_to + 1] = [''] * total_to_remove
            content_between[index + 2:remove_to + 1] = \
                    [''] * (total_to_remove - 2)
            content_between[index + 1] = '\n'
    complete_tags.append('')
    result = ''.join(sum(zip(content_between, complete_tags), tuple()))
    result = html_parser.unescape(result)
    return clean(result)

def remove_html_tags(html):
    return parse_html(html, True, ['script', 'style'])
