#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/3 21:58
# @Author  : 黄林杰
# @File    : urlib.py
# @Software: PyCharm

import requests
response = requests.get('https://httpbin.org/get')
print(response.json())