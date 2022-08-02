import rclpy
import csv
from datetime import datetime, timezone, timedelta

from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

class MinimalSubscriber(Node):

    writer = None 
    first_message = False

    def __init__(self):
        super().__init__('ardusimple_extraction')

        # Initialize CSV Writer and Header
        date = datetime.now()
        filename = "ardusimple_" + str(date.day) + "-" + str(date.month) + "-" + str(date.year) + "-" + str(date.hour) + "-" + str(date.minute) + ".csv"
        self.writer = csv.writer(open(filename, "w"), delimiter=";")
        csv_header = ['timestamp sec', 'timestamp nanosec', 'timestamp readable', 'latitude', 'longitude', 'status']
        self.writer.writerow(csv_header)

        # Subscribe to topic
        self.subscription = self.create_subscription(
            NavSatFix,
            'navsat_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        if self.first_message == False:
            self.get_logger().info('first message received - please close this node with CTRL+C when the ROSBAG is finished playing.')
            self.first_message = True

        #self.get_logger().info('lat: "%s"' % msg.latitude)
        dt = datetime.fromtimestamp(msg.header.stamp.sec, tz=timezone.utc )
        ms = (msg.header.stamp.nanosec / 1000)
        dt_ms = timedelta(microseconds= ms)
        csv_data = [msg.header.stamp.sec, msg.header.stamp.nanosec, dt + dt_ms, msg.latitude, msg.longitude, msg.status.status]
        self.writer.writerow(csv_data)


def main(args=None):
    rclpy.init(args=args)


    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()