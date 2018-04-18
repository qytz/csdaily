# -*- coding: utf-8 -*-
# This file is part of csdaily.

# Copyright (C) 2018-present qytz <hhhhhf@foxmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import requests
from lxml import html
from urllib.parse import urljoin


def get_all_cnindex():
    all_index = []
    page_size = 50
    page_cnt = 1

    categories = {
            'szxl': [   # 深证系列  key
                'gmzs', # 规模指数  val
                'hyzs', # 行业
                'fgzs', # 风格
                'ztzs', # 主题
                'clzs', # 策略
                'dzzs', # 定制
                'zhzs', # 综合
                'jjzs', # 基金
                'zqzs', # 债券
                ],
            'jcxl': [   # 国证系列
                'gmzs', # 规模指数
                'hyzs', # 行业
                'fgzs', # 风格
                'ztzs', # 主题
                'qyzs', # 区域
                'clzs', # 策略
                'dzzs', # 定制
                'zhzs', # 综合
                'jjzs', # 基金
                'zqzsxl', # 债券
                'dzczs', # 多资产
                'kjzsxl',   # 跨境
                ]
        }
    for series in categories:
        for cat in categories[series]:
            url = 'http://www.cnindex.com.cn/zstx/{series}/{cat}/'.format(**locals())
            resp = requests.get(url)
            tree = html.fromstring(resp.content.decode('utf-8'))
            for row in tree.xpath('/html/body//table/tr'):
                tds = row.xpath('./td//text()')
                if len(tds) < 6:
                    continue
                elif tds[0] == '指数名称':
                    continue
                ref_url = row.xpath('./td//a/@href')
                if ref_url:
                    ref_url = ref_url[0]
                else:
                    ref_url = ''
                all_index.append(
                        {
                            'index_name': tds[0],
                            'index_code': tds[1],
                            'base_date': tds[2],
                            'base_point': tds[3],
                            'online_date': tds[4],
                            'num': tds[5],
                            'url': urljoin(url, ref_url),
                            'series': series,
                            'category': cat
                        })

    return all_index


if __name__ == '__main__':
    # print(get_all_cnindex())
    data = get_all_cnindex()
    import json
    with open('cnindex.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
