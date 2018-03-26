# -*- coding:utf-8 -*-
"""
    @author: harvey
    @time: 2018/3/22 01:26
    @subject: 文本处理
"""
import chardet


def text_decode(content):
    """处理文本编码
    :param content: 文本内容
    :return:  unicode
    """
    coding = chardet.detect(content[:500])['encoding']
    coding = coding.lower()
    if coding == 'gb2312':
        coding = 'gbk'
    return content.decode(coding)


def text_format(content):
    """清洗段落文本
    :param content: unicode. 段落文本。
    :return: unicode.
    """

    def clean_text(text):
        return text.replace('<br>', '').strip()

    return '\n'.join(clean_text(p.replace(' ', '').strip()) for p in content)
