## 关于brew MAMP Panel

我个人还是比较喜欢将PHP开发环境在本地进行的，服务器部署还是首选docker。

由于刚从Windows转MacOS用Homebrew安装了apache2，php，mysql，redis后发现没可视化控制面板实在不方便，MAMP PRO好用但正版太贵了，也没有买断。
后来在网上找了到款LaunchRocket看介绍都很不错，结果发现作者已经8年不维护了，已经不兼容新版Homebrew安装PHP运行环境的控制了。

索性自己趁着过年空闲时间自己做一款吧，就有了大家现在见到的《brew MAMP Panel》。

目前功能还是很适合自己的，后续也会加入一些其他功能进行完善，也欢迎大家一起进行完善。

## 运行界面

[![HADC6A.png](https://s4.ax1x.com/2022/02/02/HADC6A.png)](https://imgtu.com/i/HADC6A)

## 不够完善的地方

1. 不知道为什么在idea中which brew可以找到brew命令路径，但是经过py2app打包后就返回空了，没办法只能写死路径。
2. 未做开机自启动，目前只能通过手动加入登陆项实现开机自启动，找了半天文档都没找到python在Mac下如何做开机自启。
3. 未做当前系统内通过brew安装多PHP识别，后续版本会兼容。

## Installation
- clone the repo
- cd into the repo directory
- pip install -r requirements.txt
- python3 setup.py py2app
- Copy dist/chargemon.app to /Applications