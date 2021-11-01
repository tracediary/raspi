#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
根据CPU温度开启与关闭树莓派风扇
"""

import time, os
import RPi.GPIO as GPIO
import logging

GPIO_OUT = 14
START_TEMP = 45
CLOSE_TEMP = 40
DELAY_TIME = 15
DELAY_START = 30
LOG_PATH = '/var/log/fan_control.log'



logging.basicConfig(#level=logging.DEBUG,
                    level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  # 日志格式
                    datefmt='%Y-%m-%d %H:%M:%S',  # 时间格式
                    filename=LOG_PATH,  # 日志的输出路径
                    filemode='a')  # 追加模式

def get_cpu_temperature():
    """
    获取树莓派CPU温度, 读取/sys/class/thermal/thermal_zone0/temp内容, 除1000就是温度
    :return: float
    """
    with open("/sys/class/thermal/thermal_zone0/temp", 'r') as f:
        temperature = float(f.read()) / 1000
    return temperature


def start_fan(temp):
    """
    开启风扇
    :param temp: 树莓派CPU温度
    :return:
    """
    logging.info('power on fan, temp is %s' % temp)
    # PNP型三极管基极施加低电平时才导通电路, NPN型三极管相反
    GPIO.output(GPIO_OUT, GPIO.HIGH)


def stop_fan(temp):
    """
    关闭风扇
    :param temp: 树莓派CPU温度
    :return:
    """
    logging.info('power off fan, temp is %s' % temp)
    # 基级施加高电平
    GPIO.output(GPIO_OUT, GPIO.LOW)


def setup_GPIO():
    """
    GPIO初始化
    风扇设置为关闭状态
    :return:
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_OUT, GPIO.OUT, initial=GPIO.LOW)


def control_fan():
    is_closed = True
    try:
        while True:
            temp = get_cpu_temperature()
            #logging.debug("temperature: %s" % temp)
            # 温度大于START_TEMP开启风扇， 低于CLOSE_TEMP关闭风扇
            if (temp > START_TEMP and is_closed):
                start_fan(temp)
                is_closed = False
            elif (temp < CLOSE_TEMP and not is_closed):
                stop_fan(temp)
                is_closed = True
            else:
                pass
            time.sleep(DELAY_TIME)
    except Exception as e:
        GPIO.cleanup()
        logging.error(e)

if __name__ == '__main__':
    logging.info('start fan function, delay 30s first')
    time.sleep(DELAY_START)
    logging.info('delay start end, go to control fan')
    os.environ["TZ"] = 'Asia/Shanghai'
    time.tzset()
    logging.info('started control fan...')
    setup_GPIO()
    #temperature = get_cpu_temperature()
    #logging.info("current temp is %s",% temperature)
    control_fan()
    logging.info('quit started control fan...')
