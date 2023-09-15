'''
接收 Can 报文
'''

import sys

from canlib import canlib


def print_frame(frame):
    """Prints a message to screen"""
    if (frame.flags & canlib.canMSG_ERROR_FRAME != 0):
        print("***ERROR FRAME RECEIVED***")
    else:
        print("{id:0>8X}  {dlc}  {data}  {timestamp}".format(
            id=frame.id,
            dlc=frame.dlc,
            data=' '.join('%02x' % i for i in frame.data),
            timestamp=frame.timestamp
        ))


if __name__ == '__main__':
    # Initialization
    receive_channel = 0

    # Specific CANlib channel number may be specified as first argument
    # 可以将特定的 CANlib 通道号指定为第一个参数
    if len(sys.argv) == 2:
        receive_channel = int(sys.argv[1])

    chdata = canlib.ChannelData(receive_channel)
    print("%d. %s (%s / %s)" % (receive_channel, chdata.channel_name,
                                chdata.card_upc_no,
                                chdata.card_serial_no))

    # Open CAN channel, virtual channels are considered ok to use
    # 开放CAN通道，虚拟通道被认为可以使用
    ch = canlib.openChannel(receive_channel, canlib.canOPEN_ACCEPT_VIRTUAL)

    print("Setting bitrate to 500 kb/s")
    ch.setBusParams(canlib.canBITRATE_500K)
    ch.busOn()

    # Start listening for messages
    # 开始监听消息
    finished = False
    print("   ID    DLC DATA                     Timestamp")
    while not finished:
        try:
            frame = ch.read(timeout=50)
            print_frame(frame)
        except(canlib.canNoMsg) as ex:
            pass
        except (canlib.canError) as ex:
            print(ex)
            finished = True

    # Channel teardown
    ch.busOff()
    ch.close()

