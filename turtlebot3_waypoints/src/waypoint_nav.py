#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import yaml
import tf

waypoints = []

def load_waypoints():
    with open('/home/sardor/catkin_ws/src/turtlebot3_waypoints/src/waypoints.yaml', 'r') as f:
        waypoints = yaml.safe_load(f)
    print(waypoints['waypoints'])
    return waypoints['waypoints']

def move_to_goal(x, y, theta):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y

    quaternion = tf.transformations.quaternion_from_euler(0, 0, theta)
    goal.target_pose.pose.orientation.x = quaternion[0]
    goal.target_pose.pose.orientation.y = quaternion[1]
    goal.target_pose.pose.orientation.z = quaternion[2]
    goal.target_pose.pose.orientation.w = quaternion[3]

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    rospy.init_node('waypoint_nav')
    
    # Load waypoints from file
    waypoints = load_waypoints()
    
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    rospy.loginfo("Starting navigation through waypoints...")
    n = len(waypoints)
    start_idx = 0
    while True:
        waypoint = waypoints[start_idx]
        x = waypoint['x']
        y = waypoint['y']
        theta = waypoint['theta']
        rospy.loginfo("Navigating to waypoint: x={} y={} theta={}".format(x, y, theta))
        result = move_to_goal(x, y, theta)
        if result:
            rospy.loginfo("Reached waypoint: x={} y={} theta={}".format(x, y, theta))
        else:
            rospy.logerr("Failed to reach waypoint: x={} y={} theta={}".format(x, y, theta))
            break
        start_idx += 1
        start_idx %= n
    # for waypoint in waypoints:
    #     x = waypoint['x']
    #     y = waypoint['y']
    #     theta = waypoint['theta']
    #     rospy.loginfo("Navigating to waypoint: x={} y={} theta={}".format(x, y, theta))
    #     result = move_to_goal(x, y, theta)
    #     if result:
    #         rospy.loginfo("Reached waypoint: x={} y={} theta={}".format(x, y, theta))
    #     else:
    #         rospy.logerr("Failed to reach waypoint: x={} y={} theta={}".format(x, y, theta))
    #         break

    rospy.loginfo("Navigation finished.")
