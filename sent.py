'''
发送 Can 报文
'''

import sys
import time

from canlib import canlib, Frame

sent_channel = 0
# Specific CANlib channel number may be specified as first argument
if len(sys.argv) == 2:
    sent_channel = int(sys.argv[1])

print("Opening channel %d" % sent_channel)

# Use ChannelData to get some information about the selected channel
# 使用通道数据获取有关所选通道的一些信息
chd = canlib.ChannelData(sent_channel)
print("%d. %s (%s / %s) " % (sent_channel,
                             chd.channel_name,
                             chd.card_upc_no,
                             chd.card_serial_no))

# If the channel have a custom name, print it
if chd.custom_name != '':
    print("Customized Channel Name: %s " % chd.custom_name)

# Open CAN channel, virtual channels are considered ok to use
ch = canlib.openChannel(sent_channel, canlib.canOPEN_ACCEPT_VIRTUAL)

print("Setting bitrate to 500 kb/s")
ch.setBusParams(canlib.canBITRATE_500K)

print("Going on bus")
ch.busOn()

while True:
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
