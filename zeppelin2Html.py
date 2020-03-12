import codecs
import json
import pathlib

import click
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonConsoleLexer
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_all_styles

STYLES = list(get_all_styles())


@click.command()
@click.argument('zeppelin_file', type=click.Path(exists=True))
@click.option('-s', '--style', type=click.Choice(STYLES), default='monokai')
def convert(zeppelin_file, style):
    click.echo('Converting Zeppelin file: %s to PDF using style: %s' % (zeppelin_file, style))

    with codecs.open(zeppelin_file, 'r', 'utf-8-sig') as z:
        d_zeppelin = json.load(z)
        formatter = HtmlFormatter(full=False, style=style)
        html = ['<link rel="stylesheet" type="text/css" href="style.css">']
        for d_para in d_zeppelin['paragraphs']:
            # click.echo(d_para['id'])
            html.extend(para2Html(formatter, d_para))

        input_file = pathlib.Path(zeppelin_file)
        parent_dir = input_file.parent
        html_file = pathlib.Path(parent_dir, input_file.stem + '.html')
        with open(html_file, 'w') as f:
            f.write("\n".join(html))
        style_css = pathlib.Path(parent_dir, 'style.css')
        with open(style_css, 'w') as f:
            f.write(formatter.get_style_defs('body'))

        click.echo('Html file: %s' % html_file)
        click.echo('Css file: %s' % style_css)


def para2Html(formatter, d_para):
    lang = d_para['config']['editorSetting']['language']
    html = []
    if d_para['text']:
        if lang == 'markdown':
            html.extend([d_msg['data'] for d_msg in d_para.get('results', {}).get('msg', '')])
        else:
            html.append(highlight(d_para['text'], get_lexer_by_name(lang, stripall=True), formatter))
            for data in filter(None, map(lambda d_msg: d_msg['data'], d_para.get('results', {}).get('msg', ''))):
                html.append(highlight(data, PythonConsoleLexer(), formatter))
    return html


if __name__ == '__main__':
    convert()
