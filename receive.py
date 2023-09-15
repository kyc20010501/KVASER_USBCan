"""
接收 Can 报文
"""

import sys

from canlib import canlib

def print_frame(the_frame):
    """输出信息"""
    if the_frame.flags & canlib.canMSG_ERROR_FRAME != 0:
        print("***ERROR FRAME RECEIVED***")
    else:
        print("{id:0>8X}  {dlc}  {data}  {timestamp}".format(
            id=the_frame.id,
            dlc=the_frame.dlc,
            data=' '.join('%02x' % i for i in the_frame.data),
            timestamp=the_frame.timestamp
        ))


if __name__ == '__main__':
    # 初始化
    receive_channel = 0

    # 设定canlib通道
    if len(sys.argv) == 2:
        receive_channel = int(sys.argv[1])

    chdata = canlib.ChannelData(receive_channel)
    print("%d. %s (%s / %s)" % (receive_channel, chdata.channel_name,
                                chdata.card_upc_no,
                                chdata.card_serial_no))

    # 开启CAN通道，可使用虚拟通道
    ch = canlib.openChannel(receive_channel, canlib.canOPEN_ACCEPT_VIRTUAL)

    print("Setting bitrate to 500 kb/s")
    ch.setBusParams(canlib.canBITRATE_500K)
    ch.busOn()

    # 开始监听消息
    finished = False
    print("   ID    DLC DATA                     Timestamp")
    while not finished:
        try:
            frame = ch.read(timeout=50)
            print_frame(frame)
        except canlib.canNoMsg as ex:
            pass
        except canlib.canError as ex:
            print(ex)
            finished = True

    # 关闭通道
    ch.busOff()
    ch.close()
