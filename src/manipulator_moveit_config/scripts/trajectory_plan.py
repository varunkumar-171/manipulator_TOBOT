#!/usr/bin/python3


import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from math import radians


def all_close(goal, actual, tolerance):

    all_equal = True
    if type(goal) is list:
        for index in range(len(goal)):
            if abs(actual[index] - goal[index]) > tolerance:
                return False
    elif type(goal) is geometry_msgs.msg.PoseStamped:

        return all_close(goal.pose, actual.pose, tolerance)
    elif type(goal) is geometry_msgs.msg.Pose:

        return all_close(pose_to_list(goal), pose_to_list(actual),
                         tolerance)

    return True


class MoveGroup(object):

    def __init__(self):
        super(MoveGroup, self).__init__()

        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('move_group_python_interface_tutorial',
                        anonymous=True)


        robot = moveit_commander.RobotCommander()


        scene = moveit_commander.PlanningSceneInterface()

        group_name = 'arm'
        group = moveit_commander.MoveGroupCommander(group_name)

        display_trajectory_publisher = \
            rospy.Publisher('/move_group/display_planned_path',
                            moveit_msgs.msg.DisplayTrajectory,
                            queue_size=20)

        planning_frame = group.get_planning_frame()
        print('============ Reference frame: %s' % planning_frame)


        group_names = robot.get_group_names()
        print ('============ Robot Groups:', robot.get_group_names())

        print('============ Printing robot state')
        print(robot.get_current_state())
        
        self.box_name = ''
        self.robot = robot
        self.scene = scene
        self.group = group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = 'end_effector'
        self.group_names = group_names

    def all_close(goal, actual, tolerance):
            
            all_equal = True
            if type(goal) is list:
                for index in range(len(goal)):
                    if abs(actual[index] - goal[index]) > tolerance:
                        return False
            elif type(goal) is geometry_msgs.msg.PoseStamped:

                return all_close(goal.pose, actual.pose, tolerance)
            elif type(goal) is geometry_msgs.msg.Pose:

                return all_close(pose_to_list(goal),
                                 pose_to_list(actual), tolerance)

            return True

    def go_to_pose_goal(self):

            group = self.group

            pose_goal = geometry_msgs.msg.Pose()
            pose_goal.orientation.x = 0.000
            pose_goal.orientation.y = 0.000
            pose_goal.orientation.z = 0.707
            pose_goal.orientation.w = 0.707

            pose_goal.position.x = 0.000
            pose_goal.position.y = 0.191
            pose_goal.position.z = 1.001
            group.set_joint_value_target(pose_goal, True)

            plan = group.go(wait=True)

            group.stop()

            group.clear_pose_targets()

            current_pose = group.get_current_pose().pose
            return all_close(pose_goal, current_pose, 0.01)


def main():
    try:
        print('============ Press `Enter` to begin the tutorial by setting up the moveit_commander (press ctrl-d to exit) ...')
        input()
        arm = MoveGroup()

        print('============ Press `Enter` to execute a movement using a pose goal ...')
        input()
        arm.go_to_pose_goal()
    except rospy.ROSInterruptException:

        return
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()
