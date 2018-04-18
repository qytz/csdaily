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


def get_all_csindex(only_china=True):
    all_index = []
    page_size = 50
    page_cnt = 1

    curr_page = 1
    while curr_page <= page_cnt:
        url = 'http://www.csindex.com.cn/zh-CN/indices/index?page={curr_page}&page_size={page_size}&by=desc&order=指数代码&data_type=json'.format(**locals())
        if only_china:
            url += '&class_7=7'
        resp = requests.get(url)
        ret = resp.json()
        page_cnt = ret['total_page']
        all_index.extend(ret['list'])
        curr_page += 1

    return all_index


if __name__ == '__main__':
    # print(get_all_csindex())
    data = get_all_csindex()
    import json
    with open('csindex.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
