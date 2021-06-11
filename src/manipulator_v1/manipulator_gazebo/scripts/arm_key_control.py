#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import tty
import termios
import threading
import rospy
from std_msgs.msg import Float64

# input variables

ch = ''


def read_input():
    global ch
    while True:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        # interpretting input

        if ch == 'h':
            show_help()
        elif ch == 'x':
            break
        elif ch == 'q':
            cur_cmd[1] -= 0.1
            if cur_cmd[1] < -2.267:
                cur_cmd[1] = -2.267
        elif ch == 'e':
            cur_cmd[1] += 0.1
            if cur_cmd[1] < 0.697:
                cur_cmd[1] = 0.697
        elif ch == 'd':
            cur_cmd[2] -= 0.1
            if cur_cmd[2] < -6.28:
                cur_cmd[2] = -6.28
        elif ch == 'a':
            cur_cmd[2] += 0.1
            if cur_cmd[2] > 6.28:
                cur_cmd[2] = 6.28
        elif ch == 'w':
            cur_cmd[0] += 0.1
            if cur_cmd[0] > 5:
                cur_cmd[0] = 5
        elif ch == 's':
            cur_cmd[0] -= 0.1
            if cur_cmd[0] < -5:
                cur_cmd[0] = -5
        elif ch == 'r':
            cur_cmd[3] += 0.1
            if cur_cmd[3] < 6.28:
                cur_cmd[3] = 6.28
        else:
            print('Invalid input. Press h to see help.')


def show_help():
    print('w - Base Link UP')
    print('s - Base Link DOWN')
    print('d - End Link RIGHT')
    print('a - End Link LEFT')
    print('q - Mid Link LEFT')
    print('e - Mid Link RIGHT')
    print('r - Base ROTATE')
    print('h - to show this help')
    print('x - to exit')


def send_cmds():
    for i in range(0, 4):
        if prev_cmd[i] != cur_cmd[i]:
            if i == 0:
                base_piston_joint_pub.publish(cur_cmd[i])
            elif i == 1:
                midlink_joint_pub.publish(cur_cmd[i])
            elif i == 2:
                endlink_joint_pub.publish(cur_cmd[i])
            elif i == 3:
                base_joint_pub.publish(cur_cmd[i])

            # print(cur_cmd)

    rate.sleep()


if __name__ == '__main__':

    # Control variables

    prev_cmd = [0, 0, 0, 0]
    cur_cmd = [0, 0, 0, 0]

    # initialize the node

    rospy.init_node('arm_key_control', anonymous=False)

    # define publishers

    base_joint_pub = \
        rospy.Publisher('/arm/num_base_joint_position_controller/command'
                        , Float64, queue_size=1000)
    base_piston_joint_pub = \
        rospy.Publisher('/arm/num_piston_joint_position_controller/command'
                        , Float64, queue_size=1000)
    midlink_joint_pub = \
        rospy.Publisher('/arm/mid_link_joint_position_controller/command'
                        , Float64, queue_size=1000)
    endlink_joint_pub = \
        rospy.Publisher('/arm/end_link_joint_position_controller/command'
                        , Float64, queue_size=1000)

    # background daemon thread to take user input

    th_user_input = threading.Thread(target=read_input)
    th_user_input.daemon = True
    th_user_input.start()

    rate = rospy.Rate(8)
    try:
        show_help()
        while not (rospy.is_shutdown() or ch == 'x'):
            send_cmds()
    except rospy.ROSInterruptException:
        pass
    finally:
        print('Service shutdown succesfully.')


			
