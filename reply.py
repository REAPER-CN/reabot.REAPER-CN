from nonebot import on_command
from nonebot.typing import Context_T
from config import ALLOW_GROUP, SUPERUSERS
import os
import json
import re
from .landoleet_check import check_ldl, save_json, get_reply_content
import time
from random import shuffle
import requests
import logging

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

from query_reaperstash import query_theme

import pandas as pd
import numpy as np
import synonyms

SUPERUSERS = list(SUPERUSERS)[0]


def get_group_text(context):
    if '[CQ:at,qq=424789383]' in context['raw_message']:
        return True


bot = nonebot.get_bot()

reply_df = pd.read_csv(
    'https://raw.githubusercontent.com/REAPER-CN/reabot.REAPER-CN/master/reabot_reply.csv')


@bot.on_message('group')
async def _(ctx: Context_T):
    if ctx['message_type'] == 'group':
        if os.path.isfile('./landoleet.json') is False:
            await check_ldl()
        if os.path.isfile('./landoleet_mini.json') is False:
            save_json('./landoleet_mini.json', await get_reply_content())
            time.sleep(0.25)
        with open('./landoleet_mini.json') as f:
            data = json.load(f)

        if os.path.isfile('./juce_data.json') is False:
            pass
        with open('./juce_data.json') as f:
            juce_data = json.load(f)

        if ctx['group_id'] in ALLOW_GROUP:

            if get_group_text(ctx):
                ctx['raw_message'] = ctx['raw_message'].lower()
                at_qq_list_all = re.findall(
                    'cq:at,qq=[1-9]\d*', ctx['raw_message'])
                if at_qq_list_all != []:
                    at_qq_list = [
                        x for x in at_qq_list_all if '424789383' not in x]
                    at_qq_list = ['[' + x + ']' for x in at_qq_list]
                    at_qq_cqcode = ' '.join(at_qq_list)
                    at_qq_cqcode = at_qq_cqcode.replace('cq:at', 'CQ:at')
                elif at_qq_list_all == []:
                    at_qq_cqcode = ''

                msg = re.sub('\[cq.*?\]', '', ctx['raw_message'])
                msg = msg.strip()
                msg = msg.replace('reaper', '')

                def get_match_corpus(df, msg):

                    full_match_df = df[df.keyword.isin([msg])]
                    if full_match_df.shape[0] == 1:
                        if full_match_df.match_type.values[0] == 'full':
                            return full_match_df.reply_content.values[0], 'content'

                    dfs = []
                    for i, r in df.iterrows():
                        if pd.isnull(r.match_1):
                            continue
                        m1_list = r.match_1.split(',')
                        for x in m1_list:
                            if x in msg:
                                dfs.append(df.iloc[[i, ]])
                                continue
                            elif synonyms.compare(msg, x, seg=True) >= 0.7:
                                dfs.append(df.iloc[[i, ]])
                                continue

                    # logging.warning(dfs)
                    all_df = pd.concat(dfs)

                    rets = []
                    if pd.isnull(all_df.match_1_weight) is False:
                        fin_df = all_df[all_df.match_1_weight ==
                                        all_df.match_1_weight.max()]
                        if fin_df.shape[0] != 0:
                            rets.append((fin_df.corpus.values[0], 'corpus', fin_df.reply_content.values[0]))
                            return rets
                    else:
                        for i, r in all_df.iterrows():
                            rets.append((r.corpus, 'corpus', r.reply_content))
                        return rets

                pre_compare = get_match_corpus(reply_df, msg)

                def get_reply_content(pre_compare, msg):
                    if pre_compare[1] == 'content':
                        return pre_compare[0]
                    elif pre_compare[1] == 'corpus':
                        ori_list = pre_compare[0].split(',')

                        for x in ori_list:
                            point = synonyms.compare(msg, x, seg=True)
                            if point >= 0.3:
                                return pre_compare[2]
                        return None
                for x in pre_compare:
                    fin_content = get_reply_content(x, msg)
                    if fin_content != None:
                        reply_content = fin_content
                        break
                    else:
                        reply_content = None

                if reply_content is not None:
                    content = '\n' + reply_content
                    if '{}' in content:
                        content = content.format(data['version'])
                    await bot.send_group_msg(
                        group_id=ctx['group_id'],
                        message='[CQ:at,qq={}] {} {}'.format(
                            ctx['user_id'],
                            at_qq_cqcode,
                            content
                        )
                    )
