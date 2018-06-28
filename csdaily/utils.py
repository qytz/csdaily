# -*- coding: utf-8 -*-
# This file is part of CSDaily.

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
import pandas as pd


FILTER_DICT = {
    'ASTOCKS': {    # A股
        'SH': '^SH6',
        'SZ': '^SZ00|^SZ30'
        },
    'BSTOCKS': {    # B股
        'SH': '^SH9',
        'SZ': '^SZ2'
        },
    'INDEX': {  # 指数
        'SH': '^SH00',
        'SZ': '^SZ399'
        },
    'ETF': {
        'SH': '^SH51',
        'SZ': '^SZ15|^SZ16'
        },
    'CB': { # 可转债
        'SH': '^SH100|^SH110|^SSH112|^SH113',
        'SZ': '^SZ12'
        },
    'ALL': {
        'SH': '^SH',
        'SZ': '^SZ'
        }
    }


def filter_by_symbol(df, symbol_type='ALL', market='ALL'):
    """根据 symbol 过滤返回符合条件的数据

    df 至少应包含 symbol 列，该列类型为字符串，内容规则如下：

        SHxxxxxx    上海股票交易所代码
        SZxxxxxx    深圳股票交易所代码

    symbol_type: ASTOCKS/BSTOCKS/INDEX/ETF/CB/ALL
        ASTOCKS: A股股票
        BSTOCKS: B股股票
        INDEX: 指数
        ETF: ETF基金
        CB: CONVERTIBLE BONDS，可转债
    market: SZ/SH/ALL
        SZ: 深圳股票交易所
        SH: 上海股票交易所
        ALL: 所有
    """
    if symbol_type == 'ALL' and market == 'ALL':
        return df
    if symbol_type not in FILTER_DICT:
        symbol_type = 'ALL'
    if market in FILTER_DICT[symbol_type]:
        pat = FILTER_DICT[symbol_type][market]
    else:
        pat = '|'.join(FILTER_DICT[symbol_type].values())
    return df[df.symbol.str.contains(pat)]
