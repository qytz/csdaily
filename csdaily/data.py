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
import os
import time
import asyncio
import logging
from datetime import date

import aiohttp
import pandas as pd
from sqlalchemy import create_engine

from .cli import FinApp, CSDaily


logger = logging.getLogger(__file__)


@CSDaily.subcommand('data')
class DataApp(FinApp):
    async def get_daily_stocks_xq(self, session, data_type='stock'):
        """
        获取每日行情概览信息，只能获取当天的
        返回一个 pd.DataFrame
        出错，返回 None

        data_type
            stock: 沪深股票
            cb: 可转债
            eft: ETF基金

        https://xueqiu.com/stock/cata/stocklist.json
        https://xueqiu.com/fund/quote/list.json

        股票代码
        =================
        上海证券交易所

            首位代码    产品定义
            0       国债／指数
            00      上证指数、沪深300指数、中证指数
            １      债券
            ２      回购
            ３      期货
            ４      备用
            ５      基金／权证
            ６      A股
            ７      非交易业务（发行、权益分配）
            ８      备用
            ９      B股

        深圳证券交易所
            00      A股证券
            002~004 中小板
            1       债券
            2       B股
            30      创业板证券
            39      综合指数、成份指数

        """
        headers = {
            # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) '
            #               'Gecko/20100101 Firefox/54.0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) '
                          'Gecko/20100101 Firefox/54.0',
        }
        await session.get('https://xueqiu.com', headers=headers)

        quotes = []
        page_size = 90
        curr_page = page_cnt = 1
        params = {
            '_': 0,
            'order': 'desc',
            'orderby': 'percent',
            'page': curr_page,
            'size': page_size,
            }
        quotes_url = 'https://xueqiu.com/stock/cata/stocklist.json'
        if data_type == 'stock':
            params['type'] = '11,12'
        elif data_type == 'cb':
            params['exchange'] = 'CN'
            params['industry'] = '可转债'
        elif data_type == 'etf':
            params['parent_type'] = 13
            params['type'] = 135
            params['orderBy'] = 'percent'
            quotes_url = 'https://xueqiu.com/fund/quote/list.json'

        logger.info('start download xueqiu daily quotes for %s...', data_type)
        while curr_page <= page_cnt:
            logger.info('Fetching %s/%s page', curr_page, page_cnt)
            params['page'] = curr_page
            params['_'] = int(time.time() * 1000)
            resp = await session.get(quotes_url, params=params, headers=headers)
            resp_json = await resp.json()
            if data_type in ('stock', 'cb'):
                if not resp_json['success']:
                    logger.error('Get daily quotes for %s failed: %s', data_type, resp_json)
                    break
                total_cnt = resp_json['count']['count']
            elif data_type in ('etf',):
                if 'error_code' in resp_json:
                    logger.error('Get daily quotes for %s failed: %s', data_type, resp_json)
                    break
                total_cnt = resp_json['count']
            page_cnt = total_cnt // page_size + 1 if total_cnt % page_size != 0 else 0
            quotes.extend(resp_json['stocks'])
            curr_page += 1
        if not quotes:
            logger.warn('no data downloaded for %s, return None', data_type)
            pd.DataFrame()
        logger.info('download xueqiu daily quotes for %s finish', data_type)
        df = pd.DataFrame(quotes)
        df['day'] = date.today()
        # set index
        df.set_index(['symbol', 'day'], inplace=True)
        df.drop_duplicates(inplace=True)
        # convert to numertic types
        return df.apply(pd.to_numeric, errors='ignore')

    async def update_data_daily(self):
        day = str(date.today())
        db_dir = os.path.join(self._data_dir, 'daily_quotes')
        os.makedirs(db_dir, exist_ok=True)
        db_file = os.path.join(db_dir, f'{day}.db')
        engine = create_engine('sqlite:///' + db_file)
        logger.info('start downloading, data will be saved to %s', db_file)
        async with aiohttp.ClientSession() as session:
            df = await self.get_daily_stocks_xq(session, data_type='stock')
            if not df.empty:
                df.to_sql('stock_quotes', engine, chunksize=1000, if_exists='append', index=True)
            df = await self.get_daily_stocks_xq(session, data_type='cb')
            if not df.empty:
                df.to_sql('cb_quotes', engine, chunksize=1000, if_exists='append', index=True)
            df = await self.get_daily_stocks_xq(session, data_type='etf')
            if not df.empty:
                df.to_sql('etf_quotes', engine, chunksize=1000, if_exists='append', index=True)
        logger.info('all data has be saved to %s', db_file)

    def main(self, *args):
        self._data_dir = os.path.join(self._root_dir, 'origin_data')
        os.makedirs(self._data_dir, exist_ok=True)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.update_data_daily())


if __name__ == '__main__':
    DataApp()
