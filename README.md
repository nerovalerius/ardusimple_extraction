# ardusimple_extraction
Extracts Location and Timestamp from the ardusimple ROS topic

## How to interpret the values
http://docs.ros.org/en/lunar/api/sensor_msgs/html/msg/NavSatStatus.html
http://docs.ros.org/en/lunar/api/sensor_msgs/html/msg/NavSatFix.html

## How to run
Play rosbag:
```ros2 bag play rosbag2_2022_07_05-11_56_57_0.db3 -s sqlite3```

Run node:
```ros2 run ros_topic_extraction ardusimple_extraction```