#!/usr/bin/env python
# coding=utf-8
#
# Author:
# Created Time: 2016年07月25日 星期一 23时55分55秒

import click
from pyquery import PyQuery as pq


__version__ = "0.1"

STYLE = {
    'fore':
    {   # 前景色
     'black'    : 30,   #  黑色
     'red'      : 31,   #  红色
     'green'    : 32,   #  绿色
     'yellow'   : 33,   #  黄色
     'blue'     : 34,   #  蓝色
     'purple'   : 35,   #  紫红色
     'cyan'     : 36,   #  青蓝色
     'white'    : 37,   #  白色
     },

    'back' :
    {   # 背景
     'black'     : 40,  #  黑色
     'red'       : 41,  #  红色
     'green'     : 42,  #  绿色
     'yellow'    : 43,  #  黄色
     'blue'      : 44,  #  蓝色
     'purple'    : 45,  #  紫红色
     'cyan'      : 46,  #  青蓝色
     'white'     : 47,  #  白色
     },

    'mode' :
    {   # 显示模式
     'mormal'    : 0,   #  终端默认设置
     'bold'      : 1,   #  高亮显示
     'underline' : 4,   #  使用下划线
     'blink'     : 5,   #  闪烁
     'invert'    : 7,   #  反白显示
     'hide'      : 8,   #  不可见
     },

    'default' :
    {
        'end' : 0,
    },
}


def use_style(string, mode='', fore='', back=''):
    mode = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'] else ''
    fore = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'] else ''
    back = '%s' % STYLE['back'][back] if back in STYLE['back'] else ''
    style = ';'.join([s for s in [mode, fore, back] if s])
    style = '\033[%sm' % style if style else ''
    end = '\033[%sm' % STYLE['default']['end'] if style else ''
    return '%s%s%s' % (style, string, end)


def get(selector, parent, default=""):
    item = pq(selector, parent)
    if len(item) == 1:
        val = item[0].text
    else:
        val = default
        return val


@click.command()
@click.option('--word', default=None, required=True, help='搜索关键词')
@click.option('--page', default="1", required=False, help='当前页码')
@click.option('--pagesize', default="30", required=False, help='每页显示条数')
@click.version_option(version=__version__, )
def cli(word, page, pagesize):
    surl = u"http://stackoverflow.com/search?page=" \
        + page + "&tab=relevance&pagesize=" + pagesize + "&q=" + word
    d = pq(url=surl)
    results = d("div.search-result")
    print "len = ", len(results)

    for res in results:
        # 投票数
        vote = get("span.vote-count-post strong", res, "0")

        # 回答数
        answer = get("div.answered-accepted strong", res, "0")

        # 标题
        title = pq("div.result-link span a", res)[0].text.strip()
        href = pq("div.result-link span a", res)[0].get("href")
        href = "http://stackoverflow.com" + href

        desc = pq("div.excerpt", res).text().strip()

        print
        print use_style(title, back="green")
        print href
        print vote
        print "vote =", use_style(vote, back="red"), \
            " answer =", use_style(answer, back="red")
        print desc


if __name__ == "__main__":
    cli()