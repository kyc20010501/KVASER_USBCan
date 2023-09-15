"""
发送 Can 报文
"""

import sys
import time

from canlib import canlib, Frame

sent_channel = 0
# 设定发送通道
if len(sys.argv) == 2:
    sent_channel = int(sys.argv[1])

print("Opening channel %d" % sent_channel)

# 使用’ChannelData‘获取所选通道信息
chd = canlib.ChannelData(sent_channel)
print("%d. %s (%s / %s) " % (sent_channel,
                             chd.channel_name,
                             chd.card_upc_no,
                             chd.card_serial_no))

# 输出通道自定义名称（如果有的话
if chd.custom_name != '':
    print("Customized Channel Name: %s " % chd.custom_name)

# 开启can通道，虚拟通道可使用
ch = canlib.openChannel(sent_channel, canlib.canOPEN_ACCEPT_VIRTUAL)

print("Setting bitrate to 500 kb/s")
ch.setBusParams(canlib.canBITRATE_500K)

print("Going on bus")
ch.busOn()

for i in 100:
    print("Sending a message")
    frame = Frame(id_=123,
                  data=[1, 2, 3, 4, 5, 6, 7, 8],
                  dlc=8,
                  flags=0)
    ch.write(frame)
    time.sleep(1)
print("Going off bus")
ch.busOff()

print("Closing channel")
ch.close()
