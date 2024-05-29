#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PointStamped
import tf
import yaml

waypoints = []

def write_yaml_to_file(py_obj):
    with open('/home/sardor/catkin_ws/src/turtlebot3_waypoints/src/waypoints.yaml', 'w',) as f :
        yaml.dump(py_obj,f,sort_keys=False) 
    print('Written to file successfully')

def waypoint_callback(msg):
    global waypoints
    position = msg.point
    quaternion = (0, 0, 0, 1)  # Default orientation

    # Storing the waypoint with a default theta
    waypoint = {
        'x': position.x,
        'y': position.y,
        'theta': 0.0
    }
    waypoints.append(waypoint)
    rospy.loginfo("Waypoint added: {}".format(waypoint))

if __name__ == '__main__':
    rospy.init_node('waypoint_collector')
    rospy.Subscriber('/clicked_point', PointStamped, waypoint_callback)
    
    rospy.loginfo("Collecting waypoints. Use the 'Publish Point' tool in RViz.")
    
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    
    file_path = './waypoints.yaml'
    
    try:
        with open(file_path, 'w') as file:
            rospy.loginfo("Writing waypoints to file: {}".format(file_path))
            write_yaml_to_file({'waypoints': waypoints})
            rospy.loginfo("Waypoints successfully written to file.")
    except Exception as e:
        rospy.logerr("Failed to write waypoints to file: {}".format(e))
    
