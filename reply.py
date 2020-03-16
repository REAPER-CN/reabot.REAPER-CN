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

                for i, r in reply_df.iterrows():
                    if r.keyword in ctx['raw_message']:
                        content = '\n' + r.reply_content
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

                l1 = [
                    '最强',
                    '最好',
                    '最棒',
                    '最佳',
                    'best',
                ]
                l2 = [
                    'daw',
                    '宿主',
                ]
                if any(x in ctx['raw_message'] for x in l1) and any(x in ctx['raw_message'] for x in l2):
                    content = '\r\n' \
                              '最好的DAW是REAPER'
                    await bot.send_group_msg(group_id=ctx['group_id'], message='[CQ:at,qq={}] {} {}'.format(ctx['user_id'], at_qq_cqcode, content))
