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


def filter_astocks_by_symbol(df):
    """根据 symbol 过滤返回所有 A 股数据

    df 至少应包含 symbol 列，该列类型为字符串，内容规则如下：

        SHxxxxxx    上海股票交易所代码
        SZxxxxxx    深圳股票交易所代码

    """
    sha_df = df[df.symbol.str.startswith('SH6')]
    sza_df = df[df.symbol.str.startswith('SZ00')]
    cya_df = df[df.symbol.str.startswith('SZ30')]

    return pd.concat([sha_df, sza_df, cya_df], axis=0)


def filter_bstocks_by_symbol(df):
    """根据 symbol 过滤返回所有 B 股数据

    df 至少应包含 symbol 列，该列类型为字符串，内容规则如下：

        SHxxxxxx    上海股票交易所代码
        SZxxxxxx    深圳股票交易所代码

    """
    shb_df = df[df.symbol.str.startswith('SH9')]
    szb_df = df[df.symbol.str.startswith('SZ2')]

    return pd.concat([shb_df, szb_df], axis=0)


def filter_index_by_symbol(df):
    """根据 symbol 过滤返回所有指数数据

    df 至少应包含 symbol 列，该列类型为字符串，内容规则如下：

        SHxxxxxx    上海股票交易所代码
        SZxxxxxx    深圳股票交易所代码

    """
    shindex_df = df[df.symbol.str.startswith('SH00')]
    szindex_df = df[df.symbol.str.startswith('SZ399')]

    return pd.concat([shindex_df, szindex_df], axis=0)


def filter_etf_by_symbol(df):
    """根据 symbol 过滤返回所有EFT数据

    df 至少应包含 symbol 列，该列类型为字符串，内容规则如下：

        SHxxxxxx    上海股票交易所代码
        SZxxxxxx    深圳股票交易所代码

    """
    shetf_df = df[df.symbol.str.startswith('SH51')]
    szetf1_df = df[df.symbol.str.startswith('SZ15')]
    szetf2_df = df[df.symbol.str.startswith('SZ16')]

    return pd.concat([shetf_df, szetf1_df, szetf2_df], axis=0)


def filter_cb_by_symbol(df):
    """根据 symbol 过滤返回所有可转债数据: Convertible bonds

    df 至少应包含 symbol 列，该列类型为字符串，内容规则如下：

        SHxxxxxx    上海股票交易所代码
        SZxxxxxx    深圳股票交易所代码

    """
    shcb1_df = df[df.symbol.str.startswith('SH100')]
    shcb2_df = df[df.symbol.str.startswith('SH110')]
    shcb3_df = df[df.symbol.str.startswith('SH112')]
    shcb4_df = df[df.symbol.str.startswith('SH113')]
    szcb_df = df[df.symbol.str.startswith('SZ12')]

    return pd.concat([shcb1_df, shcb2_df, shcb3_df, shcb4_df, szcb_df], axis=0)
