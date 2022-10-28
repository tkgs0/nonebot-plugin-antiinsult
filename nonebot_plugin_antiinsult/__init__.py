try:
    import ujson as json
except ModuleNotFoundError:
    import json
from pathlib import Path
from nonebot.rule import to_me
from nonebot import get_driver, logger, on_keyword
from nonebot.message import event_preprocessor
from nonebot.exception import IgnoredException
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PokeNotifyEvent
)



superusers = get_driver().config.superusers

curse_list = Path(__file__).parent / "curse.json"
curse = json.load(open(curse_list))
curse = set(curse)

blacklist = list()



def handle_namelist(uid):
    uid = str(uid)
    blacklist.append(uid)
    return f"⚠已将用户{uid}加入临时黑名单️⚠"



anti_abuse = on_keyword(curse, rule=to_me(), priority=15, block=True)

@anti_abuse.handle()
async def _(bot: Bot, event: MessageEvent):
    user_id = event.user_id
    try:
        if isinstance(event, GroupMessageEvent):
            await bot.set_group_ban(user_id=user_id, group_id=event.group_id, duration=43200)
    except:
        msg = handle_namelist(user_id)
        print(msg)
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
def namelist_processor(event: PokeNotifyEvent):
    uid = str(event.user_id)
    if uid in superusers:
        return
    if uid in blacklist:
        logger.debug(f"用户 {uid} 在临时黑名单中, 忽略本次消息")
        raise IgnoredException("黑名单用户")
