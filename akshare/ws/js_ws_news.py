# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/11/25 15:47
Desc: 金十数据 websocket 实时数据接口-新闻
https://www.jin10.com/
wss://wss-flash-1.jin10.com/
"""
import pandas as pd
import requests


def js_news(indicator: str = '最新资讯') -> pd.DataFrame:
    """
    金十数据
    https://www.jin10.com/
    :indicator: choice of {'最新资讯', '最新数据'}
    :rtype: str
    :return: 金十数据
    :rtype: pandas.DataFrame
    """
    url = 'https://m.jin10.com/flash?maxId=0'
    r = requests.get(url)
    text_data = eval(r.text)
    text_data = [item.strip() for item in text_data]
    big_df = pd.DataFrame()
    temp_df_part_one = pd.DataFrame([item.split("#") for item in text_data if item.startswith('0#1#')]).iloc[:, [2, 3]]
    temp_df_part_two = pd.DataFrame([item.split('#') for item in text_data if item.startswith('0#0#')]).iloc[:, [2, 3]]
    temp_df_part_three = pd.DataFrame([item.split('#') for item in text_data if item.startswith('1#')]).iloc[:, [8, 2, 3, 5]]
    big_df = big_df.append(temp_df_part_one, ignore_index=True)
    big_df = big_df.append(temp_df_part_two, ignore_index=True)
    big_df.columns = [
        'datetime',
        'content',
    ]
    big_df['datetime'] = pd.to_datetime(big_df['datetime'])
    big_df.sort_values('datetime', ascending=False, inplace=True)
    temp_df_part_three.columns = [
        'datetime',
        'content',
        'before',
        'now',
    ]
    temp_df_part_three
    if indicator == '最新资讯':
        return big_df
    else:
        return temp_df_part_three


if __name__ == '__main__':
    js_news_df = js_news(indicator='最新资讯')
    print(js_news_df)