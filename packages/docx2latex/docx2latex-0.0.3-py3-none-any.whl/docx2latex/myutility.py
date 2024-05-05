
import re

clean_exps = {
    r'(\\cbrt)(\w+)': r'\\sqrt[3]{\2}',
    r'(\\qdrt)(\w+)': r'\\sqrt[4]{\2}',
    r'\\sfrac': r'\\frac',
    r'(\\o[i]+nt)(\w+)': r'\1{\2}',
    r'\\bullet(\w+)': r'\\bullet \1',
    r'\\sum([a-zA-Z0-9]+)': r'\\sum{\1}',
    r'\\prod([a-zA-Z0-9]+)': r'\\prod{\1}',
    r'\\amalg([a-zA-Z0-9]+)': r'\\amalg{\1}',
    r'\\lfloor([a-zA-Z0-9]+)': r'\\lfloor{\1}',
    r'\\lceil([a-zA-Z0-9]+)': r'\\lceil{\1}',
    r'\\lim\\below\{(.+)\}\{(.+)\}': r'\\lim_{\1}{\2}',
    r'\\min\\below\{(.+)\}\{(.+)\}': r'\\min_{\1}{\2}',
    r'\\max\\below\{(.+)\}\{(.+)\}': r'\\max_{\1}{\2}',
    r'\\bigcup([a-zA-Z0-9]+)': r'\\bigcup{\1}',
    r'\\bigcap([a-zA-Z0-9]+)': r'\\bigcap{\1}',
    r'\\bigvee([a-zA-Z0-9]+)': r'\\bigvee{\1}',
    r'\\bigwedge([a-zA-Z0-9]+)': r'\\bigwedge{\1}',
    r'\\degf': '&deg;F',
    r'\\degc': '&deg;C',
}


def clean_exp(exp):
    for e in clean_exps:
        exp = re.sub(e, clean_exps[e], exp)
    return exp


word_math_map = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
}




def tag_to_latex_exp(tag):
    exp = ''
    for child in tag.iter():
        if child.tag == xml_tags('m:chr'):
            exp = child.get('{http://schemas.openxmlformats.org/officeDocument/2006/math}val')
        elif child.tag == xml_tags('m:f'):
            exp = 'frac'
            break
    if exp == '':
        return linear_expression(tag)
    text = ''
    try:
        text += supported_exps[exp](tag)
    except KeyError:
        text += linear_expression(tag)
    return text


def linear_expression(tag):
  
    text = ''
    for child in tag.iter():
        child.set('docxlatex_skip_iteration', True)
        text += child.text if child.text is not None else ''
    text = clean_exp(text)
    return text


def sigma(tag):

    latex = '\\sum_{{{}}}^{{{}}}{{{}}}'
    blocks = ['', '', '']
    curr_block = 0
    for child in tag.iter():
        child.set('docxlatex_skip_iteration', True)
        if child.tag == xml_tags('m:sub'):
            curr_block = 0
        elif child.tag == xml_tags('m:sup'):
            curr_block = 1
        elif child.tag == xml_tags('m:e'):
            curr_block = 2
        blocks[curr_block] += child.text if child.text is not None else ''
    
    return latex.format(blocks[0], blocks[1], blocks[2])


def frac(tag):
    latex_code = '\\frac{{{}}}{{{}}}'
    blocks = ['', '']
    curr_block = 0
    for child in tag.iter():
        child.set('docxlatex_skip_iteration', True)
        if child.tag == xml_tags('m:num'):
            curr_block = 0
        elif child.tag == xml_tags('m:den'):
            curr_block = 1
        blocks[curr_block] += child.text if child.text is not None else ''
    return latex_code.format(blocks[0], blocks[1])


def xml_tags(tag):
    prefix, tag_root = tag.split(':')
    uri = word_math_map[prefix]
    return '{{{}}}{}'.format(uri, tag_root)


supported_exps = {
    'frac': frac,
    '∑': sigma,
}

