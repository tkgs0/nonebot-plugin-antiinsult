import asyncio
try:
    import ujson as json
except ModuleNotFoundError:
    import json
from pathlib import Path
from typing import Literal
from random import random, choice
from nonebot.rule import to_me
from nonebot import get_driver, logger, on_message, on_command
from nonebot.matcher import Matcher
from nonebot.message import event_preprocessor
from nonebot.permission import SUPERUSER
from nonebot.exception import IgnoredException
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    GroupMessageEvent,
    PokeNotifyEvent
)
from nonebot.params import CommandArg



superusers = get_driver().config.superusers

cursepath = Path(__file__).parent / "curse.json"
curse_path = Path() / "data" / "anti-insult" / "curse.json"
curse_path.parent.mkdir(parents=True, exist_ok=True)

curse_list = (
    json.loads(curse_path.read_text("utf-8"))
    if curse_path.is_file()
    else json.loads(cursepath.read_text("utf-8"))
)

flymopath = Path(__file__).parent / "flymo.json"
flymo_path = Path() / "data" / "anti-insult" / "flymo.json"

flymo_list = (
    json.loads(flymo_path.read_text('utf-8'))
    if flymo_path.is_file()
    else json.loads(flymopath.read_text("utf-8"))
)

blacklist = {'user': []}



def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False



def save_curse_path() -> None:
    curse_path.write_text(
        json.dumps(curse_list, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )



def save_flymo_path() -> None:
    flymo_path.write_text(
        json.dumps(flymo_list, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )



def handle_curse_list(
    arg,
    mode: Literal["add", "del"],
) -> str:
    _msg = arg.extract_plain_text().strip().split()
    if not _msg:
        return "用法: \n添加(删除)屏蔽词 词1 词2 词3 ..."
    if mode == "add":
        curse_list['curse'].extend(_msg)
        curse_list['curse'] = list(set(curse_list['curse']))
        _mode = "添加"
    elif mode == "del":
        curse_list['curse'] = [msg for msg in curse_list['curse'] if msg not in _msg]
        _mode = "删除"
    save_curse_path()
    return f"已{_mode} {len(_msg)} 个屏蔽词"



def handle_namelist(uid):
    uid = str(uid)
    blacklist['user'].append(uid)
    return f"⚠已将用户{uid}加入临时黑名单️⚠"



add_curse = on_command("添加屏蔽词", permission=SUPERUSER, priority=1, block=True)

@add_curse.handle()
async def _(arg: Message = CommandArg()):
    msg = handle_curse_list(arg, "add")
    await add_curse.finish(msg)



del_curse = on_command("删除屏蔽词", permission=SUPERUSER, priority=1, block=True)

@del_curse.handle()
async def _(arg: Message = CommandArg()):
    msg = handle_curse_list(arg, "del")
    await del_curse.finish(msg)



enable_flymo = on_command(
    '启用飞妈令',
    aliases={'启用飞马令','启用飞🐴令','启用飞🐎令'},
    permission=SUPERUSER,
    priority=1,
    block=True
)

@enable_flymo.handle()
async def _():
    flymo_list['enable'] = True
    save_flymo_path()
    await enable_flymo.finish('Done.')



disable_flymo = on_command(
    '禁用飞妈令',
    aliases={'禁用飞马令','禁用飞🐴令','禁用飞🐎令'},
    permission=SUPERUSER,
    priority=1,
    block=True
)

@disable_flymo.handle()
async def _():
    flymo_list['enable'] = False
    save_flymo_path()
    await disable_flymo.finish('Done.')



anti_abuse = on_message(rule=to_me(), priority=15, block=False)

@anti_abuse.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    for i in curse_list['curse']:
        if i in str(event.get_message()):
            matcher.stop_propagation()
            if flymo_list['enable']:
                await asyncio.sleep(random()+1)
                await anti_abuse.finish(choice(flymo_list['flymo']), at_sender=True)
            user_id = event.user_id
            try:
                if isinstance(event, GroupMessageEvent):
                    await bot.set_group_ban(
                        user_id=user_id,
                        group_id=event.group_id,
                        duration=43200
                    )
            except:
                msg = handle_namelist(user_id)
                logger.info(msg)
            await anti_abuse.finish("不理你啦！バーカー", at_sender=True)



@event_preprocessor
def namelist_processor(event: MessageEvent):
    uid = str(event.user_id)
    if uid in superusers:
        return
    if uid in blacklist['user']:
        logger.debug(f"用户 {uid} 在临时黑名单中, 忽略本次消息")
        raise IgnoredException("黑名单用户")


@event_preprocessor
def namelist_processor_poke(event: PokeNotifyEvent):
    uid = str(event.user_id)
    if uid in superusers:
        return
    if uid in blacklist['user']:
        logger.debug(f"用户 {uid} 在临时黑名单中, 忽略本次消息")
        raise IgnoredException("黑名单用户")






namelist_del = on_command("解除屏蔽", aliases={"摘口球"}, permission=SUPERUSER, priority=1, block=True)

@namelist_del.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    uids = (
        [at.data['qq'] for at in event.get_message()['at']]
        if event.get_message()['at']
        else arg.extract_plain_text().strip().split()
    )
    if not uids:
        await namelist_del.finish("用法: \n解除屏蔽 qq qq1 qq2 ...")
    for uid in uids:
        if not is_number(uid):
            await namelist_del.finish("参数错误, id必须是数字..")
        try:
            if isinstance(event, GroupMessageEvent):
                await bot.set_group_ban(
                    group_id=event.group_id,
                    user_id=int(uid),
                    duration=0
                )
        except:
            pass
    blacklist['user'] = [uid for uid in blacklist['user'] if uid not in uids]
    await namelist_del.finish(f"已尝试从小黑屋释放 {len(uids)} 个用户: \n{', '.join(uids)}")



check_namelist = on_command("查看临时黑名单", permission=SUPERUSER, priority=1, block=True)

@check_namelist.handle()
async def _():
    await check_namelist.finish(f"当前已临时屏蔽{len(blacklist['user'])}个用户: \n{', '.join(blacklist['user'])}")
