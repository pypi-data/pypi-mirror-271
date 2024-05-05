from nonebot.plugin import PluginMetadata

from . import _version

__version__ = _version.__version__
__plugin_meta__ = PluginMetadata(
    name=f"❖米游社小助手插件❖\n版本 - {__version__}\n",
    description="米游社工具-每日米游币任务、游戏签到、商品兑换、免抓包登录\n",
    usage=
    "\n🔐 {HEAD}登录 ➢ 登录绑定米游社账户"
    "\n📦 {HEAD}地址 ➢ 设置收货地址ID"
    "\n🗓️ {HEAD}签到 ➢ 手动进行游戏签到"
    "\n📅 {HEAD}任务 ➢ 手动执行米游币任务"
    "\n🛒 {HEAD}兑换 ➢ 米游币商品兑换相关"
    "\n🎁 {HEAD}商品 ➢ 查看米游币商品信息(商品ID)"
    "\n📊 {HEAD}原神便笺 ➢ 查看原神实时便笺(原神树脂、洞天财瓮等)"
    "\n📊 {HEAD}铁道便笺 ➢ 查看星穹铁道实时便笺(开拓力、每日实训等)"
    "\n👁️‍🗨️ {HEAD}wb兑换 ➢ 查看微博本期超话签到的兑换码(暂支持原神和星穹铁道)"
    "\n⚙️ {HEAD}设置 ➢ 设置是否开启通知、每日任务等相关选项"
    "\n🔑 {HEAD}账号设置 ➢ 设置设备平台、是否开启每日计划任务、频道任务"
    "\n🔔 {HEAD}通知设置 ➢ 设置是否开启每日米游币任务、游戏签到的结果通知"
    "\n🖨️ {HEAD}导出Cookies ➢ 导出绑定的米游社账号的Cookies数据"
    "\n🖇️ {HEAD}用户绑定 ➢ 绑定关联其他聊天平台或其他账号的用户数据"
    "\n📨 {HEAD}私信响应 ➢ 让机器人发送一条私信给你，主要用于QQ频道"
    "\n📖 {HEAD}帮助 ➢ 查看帮助信息"
    "\n🔍 {HEAD}帮助 <功能名> ➢ 查看目标功能详细说明"
    "\n\n⚠️你的数据将经过机器人服务器，请确定你信任服务器所有者再使用。",
    extra={"version": __version__}
)

# 升级 V1 版本插件数据文件

from .model.upgrade import upgrade_plugin_data

upgrade_plugin_data()

# 在此处使用 get_driver() 防止多进程生成图片时反复调用

from .utils import CommandBegin
from nonebot import init
from nonebot import get_driver

init()  # 初始化Driver对象
get_driver().on_startup(CommandBegin.set_command_begin)

# 加载命令

from .command import *

# 加载其他代码

from .api import *
from .model import *
from .utils import *
