#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import time
import rumps
import logging
import subprocess
import pyperclip

#配置日志
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename='./logs/' + time.strftime('%Y%m%d', time.localtime(time.time())) + '.log', level=logging.DEBUG, format=LOG_FORMAT, encoding='utf-8')
# logging.basicConfig(filename='./logs/my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT, encoding='utf-8')
# print(time.strftime('%Y%m%d',time.localtime(time.time())))

VERSION = '0.0.5'

STOP_ICON = '🔴'
START_ICON = '🟢'

BREW_PATH = '/opt/homebrew/bin/brew'

SERVE_HTTPD_NAME = ''
SERVE_HTTPD_STATA = ''

SERVE_PHP_NAME = ''
SERVE_PHP_STATA = ''

SERVE_MYSQL_NAME = ''
SERVE_MYSQL_STATA = ''

SERVE_REDIS_NAME = ''
SERVE_REDIS_STATA = ''

# brewPath = subprocess.Popen('which brew', shell=True, stdout=subprocess.PIPE)
# brewPath.wait()
# BREW_PATH = brewPath.stdout.readline().decode('utf-8').strip()
# if BREW_PATH == '':
#     logging.error('brew路径找不到')
# logging.info('brew path:%s', BREW_PATH)
# print(BREW_PATH)

#延迟2秒加载程序,防止开机启动加载过快导致services list读取错误.
time.sleep(2)

state = subprocess.Popen(BREW_PATH + " services list", shell=True, stdout=subprocess.PIPE)
state.wait()
for line in state.stdout.readlines()[1:]:
    result = str(line, 'utf-8').split()
    # print(result)
    # print(result[0], result[1])
    if result[0].find('httpd') != -1:
        SERVE_HTTPD_NAME = result[0]
        SERVE_HTTPD_STATA = result[1]
        logging.info('HTTPD NAME:%s  HTTPD STATA:%s', result[0], result[1])
    elif result[0].find('php') != -1:
        SERVE_PHP_NAME = result[0]
        SERVE_PHP_STATA = result[1]
        logging.info('PHP NAME:%s  PHP STATA:%s', result[0], result[1])
    elif result[0].find('mysql') != -1:
        SERVE_MYSQL_NAME = result[0]
        SERVE_MYSQL_STATA = result[1]
        logging.info('MySQL NAME:%s  MySQL STATA:%s', result[0], result[1])
    elif result[0].find('redis') != -1:
        SERVE_REDIS_NAME = result[0]
        SERVE_REDIS_STATA = result[1]
        logging.info('Redis NAME:%s  Redis STATA:%s', result[0], result[1])
    else:
        logging.warning('无法识别:%s', result[0])


class AwesomeStatusBarApp(rumps.App):

    def __init__(self, *args, **kwargs):
        super(AwesomeStatusBarApp, self).__init__(*args, **kwargs)
        self.menu.add(rumps.MenuItem(title='brew MAMP Panel'))
        self.menu.add(rumps.MenuItem(title=VERSION))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem(title='当前状态[单击控制启停]'))

        httpdICON = START_ICON if SERVE_HTTPD_STATA == 'started' else STOP_ICON
        self.menu.add(rumps.MenuItem(title='httpd', callback=self.httpd))
        self.menu['httpd'].title = httpdICON + 'httpd'

        phpICON = START_ICON if SERVE_PHP_STATA == 'started' else STOP_ICON
        self.menu.add(rumps.MenuItem(title='PHP', callback=self.php))
        self.menu['PHP'].title = phpICON + 'PHP'

        mysqlICON = START_ICON if SERVE_MYSQL_STATA == 'started' else STOP_ICON
        self.menu.add(rumps.MenuItem(title='MySQL', callback=self.mysql))
        self.menu['MySQL'].title = mysqlICON + 'MySQL'

        redisICON = START_ICON if SERVE_REDIS_STATA == 'started' else STOP_ICON
        self.menu.add(rumps.MenuItem(title='Redis', callback=self.redis))
        self.menu['Redis'].title = redisICON + 'Redis'

        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem(title='启动所有', callback=self.startAll))
        self.menu.add(rumps.MenuItem(title='停止所有', callback=self.stopAll))
        self.menu.add(rumps.MenuItem(title='重启所有', callback=self.restartAll, key='r'))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem(title='配置直达'))
        self.menu.add(rumps.MenuItem(title='📂httpd', callback=self.Configure))
        self.menu.add(rumps.MenuItem(title='📂PHP', callback=self.Configure))
        self.menu.add(rumps.MenuItem(title='📝MySQL', callback=self.Configure))
        self.menu.add(rumps.MenuItem(title='📝Redis', callback=self.Configure))
        self.menu.add(rumps.MenuItem(title='📂Hosts', callback=self.Configure))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem(title='🔢取剪切板文本长度', callback=self.textLen))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem(title='关于', callback=self.about))
        self.menu.add(rumps.separator)

    def Configure(self, sender):
        if sender.title == '📂httpd':
            subprocess.call(['open', '/opt/homebrew/etc/httpd'])
        if sender.title == '📂PHP':
            subprocess.call(['open', '/opt/homebrew/etc/php/7.4'])
        if sender.title == '📝MySQL':
            subprocess.call(['open', '/opt/homebrew/etc/my.cnf'])
        if sender.title == '📝Redis':
            subprocess.call(['open', '/opt/homebrew/etc/redis.conf'])
        if sender.title == '📂Hosts':
            subprocess.call(['open', '/private/etc'])

    def httpd(self, sender):
        global SERVE_HTTPD_STATA
        if SERVE_HTTPD_STATA == 'none':
            httpdState = subprocess.Popen(BREW_PATH + " services start " + SERVE_HTTPD_NAME, shell=True, stdout=subprocess.PIPE)
            httpdState.wait()
            for line in httpdState.stdout.readlines():
                r = str(line, 'utf-8')
                if r.find('Successfully') != -1:
                    print('httpd启动成功')
                    SERVE_HTTPD_STATA = 'started'
                    logging.info('httpd启动成功')
                    self.menu['httpd'].title = START_ICON + 'httpd'
                else:
                    logging.error('httpd启动失败:' + r)
                    rumps.alert('httpd启动失败，请查找原因。')
        else:
            httpdState = subprocess.Popen(BREW_PATH + " services stop " + SERVE_HTTPD_NAME, shell=True, stdout=subprocess.PIPE)
            for line in httpdState.stdout.readlines()[1:]:
                r = str(line, 'utf-8')
                if r.find('Successfully') != -1:
                    print('httpd停止成功')
                    SERVE_HTTPD_STATA = 'none'
                    logging.info('httpd停止成功')
                    self.menu['httpd'].title = STOP_ICON + 'httpd'
                else:
                    logging.error('httpd停止失败:' + r)
                    rumps.alert('httpd停止失败，请查找原因。')

    def php(self, sender):
        global SERVE_PHP_STATA
        if SERVE_PHP_STATA == 'none':
            phpState = subprocess.Popen(BREW_PATH + " services start " + SERVE_PHP_NAME, shell=True, stdout=subprocess.PIPE)
            phpState.wait()
            for line in phpState.stdout.readlines():
                r = str(line, 'utf-8')
                if r.find('Successfully') != -1:
                    print('PHP启动成功')
                    SERVE_PHP_STATA = 'started'
                    logging.info('PHP启动成功')
                    self.menu['PHP'].title = START_ICON + 'PHP'
                else:
                    logging.error('PHP启动失败:' + r)
                    rumps.alert('PHP启动失败，请查找原因。')
        else:
            phpState = subprocess.Popen(BREW_PATH + " services stop " + SERVE_PHP_NAME, shell=True, stdout=subprocess.PIPE)
            for line in phpState.stdout.readlines()[1:]:
                r = str(line, 'utf-8')
                if r.find('Successfully') != -1:
                    print('PHP停止成功')
                    SERVE_PHP_STATA = 'none'
                    logging.info('PHP停止成功')
                    self.menu['PHP'].title = STOP_ICON + 'PHP'
                else:
                    logging.error('PHP停止失败:' + r)
                    rumps.alert('PHP停止失败，请查找原因。')

    def mysql(self, sender):
        global SERVE_MYSQL_STATA
        if SERVE_MYSQL_STATA == 'none':
            mysqlState = subprocess.Popen(BREW_PATH + " services start " + SERVE_MYSQL_NAME, shell=True, stdout=subprocess.PIPE)
            mysqlState.wait()
            for line in mysqlState.stdout.readlines():
                r = str(line, 'utf-8')
                if r.find('Successfully') != -1:
                    print('MySQL启动成功')
                    SERVE_MYSQL_STATA = 'started'
                    logging.info('MySQL启动成功')
                    self.menu['MySQL'].title = START_ICON + 'MySQL'
                else:
                    logging.error('MySQL启动失败:' + r)
                    rumps.alert('MySQL启动失败，请查找原因。')
        else:
            mysqlState = subprocess.Popen(BREW_PATH + " services stop " + SERVE_MYSQL_NAME, shell=True, stdout=subprocess.PIPE)
            for line in mysqlState.stdout.readlines()[1:]:
                r = str(line, 'utf-8')
                if r.find('Successfully') != -1:
                    print('MySQL停止成功')
                    SERVE_MYSQL_STATA = 'none'
                    logging.info('MySQL停止成功')
                    self.menu['MySQL'].title = STOP_ICON + 'MySQL'
                else:
                    logging.error('MySQL停止失败:' + r)
                    rumps.alert('MySQL停止失败，请查找原因。')

    def redis(self, sender):
        global SERVE_REDIS_STATA
        if SERVE_REDIS_STATA == 'none':
            redisState = subprocess.Popen(BREW_PATH + " services start " + SERVE_REDIS_NAME, shell=True, stdout=subprocess.PIPE)
            redisState.wait()
            for line in redisState.stdout.readlines():
                r = str(line, 'utf-8')
                if r.find('Successfully') != -1:
                    print('Redis启动成功')
                    SERVE_REDIS_STATA = 'started'
                    logging.info('Redis启动成功')
                    self.menu['Redis'].title = START_ICON + 'Redis'
                else:
                    logging.error('Redis启动失败:' + r)
                    rumps.alert('Redis启动失败，请查找原因。')
        else:
            redisState = subprocess.Popen(BREW_PATH + " services stop " + SERVE_REDIS_NAME, shell=True, stdout=subprocess.PIPE)
            for line in redisState.stdout.readlines()[1:]:
                r = str(line, 'utf-8')
                if r.find('Successfully') != -1:
                    print('Redis停止成功')
                    SERVE_REDIS_STATA = 'none'
                    logging.info('Redis停止成功')
                    self.menu['Redis'].title = STOP_ICON + 'Redis'
                else:
                    logging.error('Redis停止失败:' + r)
                    rumps.alert('Redis停止失败，请查找原因。')

    def startAll(self, sender):
        global SERVE_HTTPD_STATA
        global SERVE_PHP_STATA
        global SERVE_MYSQL_STATA
        global SERVE_REDIS_STATA

        print('你点击了启动所有')
        if SERVE_HTTPD_STATA == 'none':
            print('正在启动httpd')
            state = subprocess.Popen(BREW_PATH + " services start " + SERVE_HTTPD_NAME, shell=True, stdout=subprocess.PIPE)
            state.wait()
            SERVE_HTTPD_STATA = 'started'
            logging.info('启动所有正在启动httpd')
            self.menu['httpd'].title = START_ICON + 'httpd'
        if SERVE_PHP_STATA == 'none':
            print('正在启动PHP')
            state = subprocess.Popen(BREW_PATH + " services start " + SERVE_PHP_NAME, shell=True, stdout=subprocess.PIPE)
            state.wait()
            SERVE_PHP_STATA = 'started'
            logging.info('启动所有正在启动php')
            self.menu['PHP'].title = START_ICON + 'PHP'
        if SERVE_MYSQL_STATA == 'none':
            print('正在启动MySQL')
            state = subprocess.Popen(BREW_PATH + " services start " + SERVE_MYSQL_NAME, shell=True, stdout=subprocess.PIPE)
            state.wait()
            SERVE_MYSQL_STATA = 'started'
            logging.info('启动所有正在启动mysql')
            self.menu['MySQL'].title = START_ICON + 'MySQL'
        if SERVE_REDIS_STATA == 'none':
            print('正在启动Redis')
            state = subprocess.Popen(BREW_PATH + " services start " + SERVE_REDIS_NAME, shell=True, stdout=subprocess.PIPE)
            state.wait()
            SERVE_REDIS_STATA = 'started'
            logging.info('启动所有正在启动redis')
            self.menu['Redis'].title = START_ICON + 'Redis'

    def stopAll(self, sender):
        global SERVE_HTTPD_STATA
        global SERVE_PHP_STATA
        global SERVE_MYSQL_STATA
        global SERVE_REDIS_STATA

        print('你点击了停止所有')
        if SERVE_HTTPD_STATA == 'started':
            print('正在停止httpd')
            state = subprocess.Popen(BREW_PATH + " services stop " + SERVE_HTTPD_NAME, shell=True, stdout=subprocess.PIPE)
            state.wait()
            SERVE_HTTPD_STATA = 'none'
            logging.info('停止所有正在停止httpd')
            self.menu['httpd'].title = STOP_ICON + 'httpd'
        if SERVE_PHP_STATA == 'started':
            print('正在停止PHP')
            state = subprocess.Popen(BREW_PATH + " services stop " + SERVE_PHP_NAME, shell=True, stdout=subprocess.PIPE)
            state.wait()
            SERVE_PHP_STATA = 'none'
            logging.info('停止所有正在停止php')
            self.menu['PHP'].title = STOP_ICON + 'PHP'
        if SERVE_MYSQL_STATA == 'started':
            print('正在停止MySQL')
            state = subprocess.Popen(BREW_PATH + " services stop " + SERVE_MYSQL_NAME, shell=True, stdout=subprocess.PIPE)
            state.wait()
            SERVE_MYSQL_STATA = 'none'
            logging.info('停止所有正在停止mysql')
            self.menu['MySQL'].title = STOP_ICON + 'MySQL'
        if SERVE_REDIS_STATA == 'started':
            print('正在停止Redis')
            state = subprocess.Popen(BREW_PATH + " services stop " + SERVE_REDIS_NAME, shell=True, stdout=subprocess.PIPE)
            state.wait()
            SERVE_REDIS_STATA = 'none'
            logging.info('停止所有正在停止redis')
            self.menu['Redis'].title = STOP_ICON + 'Redis'

    def restartAll(self, sender):
        global SERVE_HTTPD_STATA
        global SERVE_PHP_STATA
        global SERVE_MYSQL_STATA
        global SERVE_REDIS_STATA

        print('你点击了重启所有')

        print('正在重启httpd')
        state = subprocess.Popen(BREW_PATH + " services start " + SERVE_HTTPD_NAME, shell=True, stdout=subprocess.PIPE)
        state.wait()
        SERVE_HTTPD_STATA = 'started'
        logging.info('重启所有正在重启httpd')
        self.menu['httpd'].title = START_ICON + 'httpd'

        print('正在重启PHP')
        state = subprocess.Popen(BREW_PATH + " services start " + SERVE_PHP_NAME, shell=True, stdout=subprocess.PIPE)
        state.wait()
        SERVE_PHP_STATA = 'started'
        logging.info('重启所有正在重启php')
        self.menu['PHP'].title = START_ICON + 'PHP'

        print('正在重启MySQL')
        state = subprocess.Popen(BREW_PATH + " services start " + SERVE_MYSQL_NAME, shell=True, stdout=subprocess.PIPE)
        state.wait()
        SERVE_MYSQL_STATA = 'started'
        logging.info('重启所有正在重启mysql')
        self.menu['MySQL'].title = START_ICON + 'MySQL'

        print('正在重启Redis')
        state = subprocess.Popen(BREW_PATH + " services start " + SERVE_REDIS_NAME, shell=True, stdout=subprocess.PIPE)
        state.wait()
        SERVE_REDIS_STATA = 'started'
        logging.info('重启所有正在重启redis')
        self.menu['Redis'].title = START_ICON + 'Redis'

    def textLen(self, sender):
        """获取剪贴板数据"""
        data = pyperclip.paste()
        rumps.alert('剪切板长度：' + str(len(data)))

    def about(self, sender):
        rumps.alert('作者：张雷\n编译日期：2022年2月16日')
        #rumps.quit_application(sender)#退出


if __name__ == '__main__':
    AwesomeStatusBarApp('M', quit_button=rumps.MenuItem('退出', key='q')).run()