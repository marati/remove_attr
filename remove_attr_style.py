#!  /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from bs4 import BeautifulSoup
from urllib2 import urlopen

log_filename = None;

#Работа с параметрами командной строки
len_argv = len(sys.argv)
if len_argv > 1 and len_argv <= 3:
    param_name = sys.argv[1]
    param_value = None

    #Если у параметра задано значение
    if len_argv == 3:
        param_value = sys.argv[2]

    if param_name == "--log":
        log_filename = param_value if param_value else "log.txt"
    else:
        print("Такого параметра не существует. Попробуйте --log")
        sys.exit(1)
elif len_argv > 3:
    print("Вы ввели слишком много параметров. Скрипт принимает один параметр: --log")
    sys.exit(1)

#Ввод и разбор страницы
while 1:
    get_url = raw_input("Введите url (формат: http(s)://example): ")
    if not re.match('^(http|https)://', get_url):
       print("Вы ошиблись в формате. Повторите ввод")
    else:
        break

try:
    page = urlopen(get_url).read()
    soup_page = BeautifulSoup(page)

    tags_with_attrs = soup_page.findAll(lambda tag: len(tag.attrs) >= 1)
    for tag in tags_with_attrs:
        if "style" in tag.attrs:
            del tag['style']

    if log_filename:
        log_file = open(log_filename, 'w')
        log_file.write(soup_page.prettify().encode('utf-8'))
        log_file.close()
        print "Код страницы с удалённым атрибутом style записан в файл %s" % log_filename
    else:
        print soup_page.prettify()

except IOError, e:
    print "Ошибка при отрытии страницы %s:" % get_url, e
