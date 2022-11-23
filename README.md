<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/tkgs0/nbpt/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://raw.githubusercontent.com/tkgs0/nbpt/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-antiinsult
  
_✨ NoneBot 反嘴臭插件 ✨_
  

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/tkgs0/nonebot-plugin-antiinsult.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-antiinsult">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-antiinsult.svg" alt="pypi">
</a>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</a>

</div>

  
## 📖 介绍
  
**本插件为被动插件**  
  
检测到有用户 `@机器人` 并嘴臭时将其临时屏蔽(bot重启后失效)  
当bot为群管理时会请对方喝昏睡红茶(禁言)  
  
- 超级用户不受临时屏蔽影响 _~~但是会被昏睡红茶影响~~_  
- 当bot的群权限比超级用户高的时候, 超级用户也有机会品尝昏睡红茶  
- 被bot灌了昏睡红茶的用户不会进临时黑名单  
  
  
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
  

## 🎉 使用
### 指令表

<table> 
  <tr align="center">
    <th> 指令 </th>
    <th> 权限 </th>
    <th> 需要@ </th>
    <th> 范围 </th>
    <th> 说明 </th>
  </tr>
  <tr align="center">
    <td> ^(添加|删除)屏蔽词 xxx </td>
    <td> 主人 </td>
    <td> 否 </td>
    <td> 私聊 | 群聊 </td>
    <td rowspan="2"> 可输入多个,<br>用空格隔开 </td>
  </tr>
  <tr align="center">
    <td> 解除屏蔽 qq </td>
    <td> 主人 </td>
    <td> 否 </td>
    <td> 私聊 | 群聊 </td>
  </tr>
  <tr align="center">
    <td> 查看临时黑名单 </td>
    <td> 主人 </td>
    <td> 否 </td>
    <td> 私聊 | 群聊 </td>
    <td> </td>
  </tr>
  <tr align="center">
    <td> ^(禁用|启用)飞(妈|马|🐴|🐎)令 </td>
    <td> 主人 </td>
    <td> 否 </td>
    <td> 私聊 | 群聊 </td>
    <td> 开启/关闭对线模式 </td>
</table>


P.S. `解除屏蔽` 可以解除临时屏蔽, 也可以解除禁言(当然, 需要bot为群管理).  
  
你说从聊天界面查看屏蔽词库? 噢, 我亲爱的老伙计, 你怕是疯了!  
  
