1. turtlebot_waypoints package contains 2 scripts:
    a. `waypoint_collector.py` - This script collects clicked points on rviz and saves those points at `waypoints.yaml`
    b. `waypoint_nav.py` - This script loads clicked points from `waypoints.yaml` file and commands to go to these points 

2. To be able to use this package:
    1. Install this package inside of `catkin_ws/src/`
    2. Run `cd ~/catkin_ws && catkin_make` 
    3. Initialize ros and launch navigation
    4. run `rosrun turtlebot3_waypoints waypoint_collector.py` and choose points from rviz by using 'Publish Point' plugin on rviz
    5. Exit from the process.
    6. run `rosrun turtlebot3_waypoints waypoint_nav.py` and it will move to the points forming loop
3. Link to the presentation - https://www.youtube.com/watch?v=mP1sVwK_3HU
