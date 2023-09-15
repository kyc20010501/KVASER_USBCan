'''
发送与接收 Can 报文
'''

import sys
import time
from canlib import canlib, Frame

sent_channel = 0
receive_channel = 1

if (len(sys.argv)) == 2:
    sent_channel = int(sys.argv[1])

print('正在打开串口 %d' % sent_channel)

chd = canlib.ChannelData(sent_channel)
print('%d. %s (%s / %s)' % (sent_channel,
                            chd.channel_name,
                            chd.card_upc_no,
                            chd.card_serial_no))

if chd.channel_name != '':
    print('自定通道名：%s' % chd.custom_name)

ch = canlib.openChannel(sent_channel, canlib.canOPEN_ACCEPT_VIRTUAL)

print('设置波特率为 500 kb/s')
ch.setBusParams(canlib.canBITRATE_500K)

print('开启总线')
ch.busOn()

def print_frame(receive_frame):
    if receive_frame.flags & canlib.canMSG_ERROR_FRAME != 0:
        print('！！！接收到错误帧！！！')
    else:
        print('{id:0>8x}    {dlc}   {data}  {timestamp}'.format(
            id=receive_frame.id,
            dlc=receive_frame.dlc,
            data=' '.join('%02x' % i for i in receive_frame.data),
            timestamp=receive_frame.timestamp
        ))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        receive_channel = int(sys.argv[1])

chdata = canlib.ChannelData(receive_channel)
print("%d. %s (%s / %s)" % (receive_channel,
                            chdata.channel_name,
                            chdata.card_upc_no,
                            chdata.card_serial_no))

ch = canlib.openChannel(receive_channel, canlib.canOPEN_ACCEPT_VIRTUAL)

finished = False
print('   ID    DLC DATA                     Timestamp')
# 发送消息
while not finished:
    sent_frame = Frame(id_=123,
                       data=[1, 2, 3, 4, 5, 6, 7, 8],
                       dlc=8,
                       flags=0)
    ch.write(sent_frame)

    try:
        receive_frame = ch.read(timeout=50)
        print_frame(receive_frame)
    except canlib.canNoMsg as ex:
        pass
    except canlib.canError as ex:
        print(ex)
        finished = True

    time.sleep(1)

ch.busOff()
ch.close()
