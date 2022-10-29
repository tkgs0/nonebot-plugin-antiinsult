
# nonebot-plugin-antiinsult
  
**NoneBot 反嘴臭插件**  
  

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/tkgs0/nonebot-plugin-antiinsult.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-antiinsult">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-antiinsult.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

  
## 📖 介绍
  
**本插件为被动插件**  
  
检测到有用户 `@机器人` 并嘴臭时将其临时屏蔽(bot重启后失效)  
当bot为群管理时会请对方喝昏睡红茶(禁言)  
  
超级用户不受临时屏蔽影响 _~~但是会被昏睡红茶影响~~_ (当bot的群权限比超级用户高的时候会请超级用户喝昏睡红茶)  
  
**增删屏蔽词库:**  
聊天发送 **添加/删除屏蔽词 xxx xxx xxx ...**  
  
P.S. 你说从聊天界面查看屏蔽词库? 噢, 我亲爱的老伙计, 你怕是疯了!  
  
  
## 💿 安装
  
**使用 nb-cli 安装**  
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装  
```bash
nb plugin install nonebot-plugin-antiinsult
```
  
**使用 pip 安装**  
```bash
pip install nonebot-plugin-antiinsult
```
  
打开 nonebot2 项目的 `bot.py` 文件, 在其中写入
```python
nonebot.load_plugin('nonebot_plugin_antiinsult')
```
  
  