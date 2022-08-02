import rclpy
import csv
import datetime

from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

class MinimalSubscriber(Node):

    writer = None 

    def __init__(self):
        super().__init__('minimal_subscriber')

        # Initialize CSV Writer and Header
        date = datetime.datetime.now()
        filename = "ardusimple_" + str(date.day) + "-" + str(date.month) + "-" + str(date.year) + "-" + str(date.hour) + "-" + str(date.minute) + ".csv"
        self.writer = csv.writer(open(filename, "w"), delimiter=";")
        csv_header = ['timestamp sec', 'timestamp nanosec', 'latitude', 'longitude', 'status']
        self.writer.writerow(csv_header)

        # Subscribe to topic
        self.subscription = self.create_subscription(
            NavSatFix,
            'navsat_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        #self.get_logger().info('lat: "%s"' % msg.latitude)
        csv_data = [msg.header.stamp.sec, msg.header.stamp.nanosec, msg.latitude, msg.longitude, msg.status.status]
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