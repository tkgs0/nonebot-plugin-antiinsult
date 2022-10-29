try:
    import ujson as json
except ModuleNotFoundError:
    import json
from pathlib import Path
from typing import Literal
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

file_path = Path(__file__).parent / "curse.json"
data_path = Path() / "data" / "anti-insult"
curse_path = data_path / "curse.json"

curse_list = (
    json.loads(curse_path.read_text("utf-8"))
    if curse_path.is_file()
    else json.loads(file_path.read_text("utf-8"))
)

blacklist = list()



def save_curse_path() -> None:
    if not data_path.exists():
        curse_path.parent.mkdir(parents=True, exist_ok=True)

    curse_path.write_text(
        json.dumps(curse_list, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def handle_curse_list(
    arg,
    mode: Literal["add", "del"],
) -> str:
    _msg = arg.extract_plain_text().strip().split()
    if not _msg:
        return "用法: \n添加(删除)屏蔽词 xxx xxx xxx ..."
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
    blacklist.append(uid)
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



anti_abuse = on_message(rule=to_me(), priority=15, block=False)

@anti_abuse.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    for i in curse_list['curse']:
        if i in str(event.get_message()):
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
            matcher.stop_propagation()
            await anti_abuse.finish("不理你啦！バーカー", at_sender=True)



@event_preprocessor
def namelist_processor(event: MessageEvent):
    uid = str(event.user_id)
    if uid in superusers:
        return
    if uid in blacklist:
        logger.debug(f"用户 {uid} 在临时黑名单中, 忽略本次消息")
        raise IgnoredException("黑名单用户")


@event_preprocessor
def namelist_processor_poke(event: PokeNotifyEvent):
    uid = str(event.user_id)
    if uid in superusers:
        return
    if uid in blacklist:
        logger.debug(f"用户 {uid} 在临时黑名单中, 忽略本次消息")
        raise IgnoredException("黑名单用户")
