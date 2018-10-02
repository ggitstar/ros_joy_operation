#!/usr/bin/env python
import sys
import numpy as p
import rospy as rp
from sensor_msgs.msg import Joy
from joy_to_raspberrypi.msg import Controller
from std_msgs.msg import UInt16MultiArray

class JoyConvert(object):

  def __init__(self):
    self._joy_sub=rp.Subscriber('joy',Joy,self.joyCallback,queue_size=100)
  #  self._joy_pub=rp.Publisher('joy_cont',Controller,queue_size=100)
    self._joy_pub=rp.Publisher('joy_cont',UInt16MultiArray,queue_size=100)

    self.state=[0,0,0,0,0]

  def joyCallback(self,joy_msg):
    self.state[0]=int((joy_msg.axes[0]+1)*100)
    self.state[1]=int((joy_msg.axes[1]+1)*100)
    self.state[2]=int((joy_msg.axes[2]+1)*100)
    self.state[3]=int((joy_msg.axes[3]+1)*100)
    for i in range(12):
      if(joy_msg.buttons[i]):
        self.state[4]|=1<<i
      else:
        self.state[4]&=~(1<<i)
    if joy_msg.axes[4]>0:
      self.state[4]|=1<<12
    else:
      self.state[4]&=~(1<<12)

    if joy_msg.axes[4]<0:
      self.state[4]|=1<<13
    else:
      self.state[4]&=~(1<<13)

    if joy_msg.axes[5]>0:
      self.state[4]|=1<<14
    else:
      self.state[4]&=~(1<<14)

    if joy_msg.axes[5]<0:
      self.state[4]|=1<<15
    else:
      self.state[4]&=~(1<<15)

if __name__=='__main__':
  rp.init_node('Joy_cont')
  rate=rp.Rate(50)
  joy_cont=JoyConvert()
  #cont=Controller()
  cont=UInt16MultiArray()
  cont.data=[0]*5
  while not rp.is_shutdown():
#      cont.analog[0]=joy_cont.state[0]
#      cont.analog[1]=joy_cont.state[1]
#      cont.analog[2]=joy_cont.state[2]
#      cont.analog[3]=joy_cont.state[3]
#      cont.buttons=joy_cont.state[4]
      cont.data[0]=joy_cont.state[0]
      cont.data[1]=joy_cont.state[1]
      cont.data[2]=joy_cont.state[2]
      cont.data[3]=joy_cont.state[3]
      cont.data[4]=joy_cont.state[4]
      rp.loginfo(cont)
      joy_cont._joy_pub.publish(cont)
      rate.sleep()

