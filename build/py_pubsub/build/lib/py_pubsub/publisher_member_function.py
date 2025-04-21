# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import LaserScan

import math


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        # Creates a publisher for the Twist of owenturtle
        self.publisher_ = self.create_publisher(Twist, '/diff_drive/cmd_vel', 10)
        timer_period = 0.5  # seconds
        # Callback function that does the controlling the the robot
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.front_sensor = None
        self.left_sensor = None

        # Creates a subscriber to the Pose of owenturtle
        self.subscription = self.create_subscription(
            LaserScan,
            '/diff_drive/scan',
            self.listener_callback,
            10)
        self.subscription

    def timer_callback(self):
        if ((self.front_sensor != None) and (self.left_sensor != None)):
            self.publisher_.publish(Twist(linear=Vector3(x=0.25, y=0.0, z=0.0)))
            if ((self.front_sensor > 2) and (self.left_sensor >= 1.5)):
                left_adjust = Twist(linear=Vector3(x=0.25, y=0.0, z=0.0), angular=Vector3(x=0.0, y=0.0, z=0.25))
                self.publisher_.publish(left_adjust)
            elif ((self.front_sensor < 2) or (self.left_sensor <= 1)):
                right_adjust = Twist(linear=Vector3(x=0.25, y=0.0, z=0.0), angular=Vector3(x=0.0, y=0.0, z=-0.25))
                self.publisher_.publish(right_adjust)

    def listener_callback(self, msg):
        left_scan = msg.ranges[-1]
        front_scan = msg.ranges[1]
        print('Left Dist: [%s] Front Dist: [%s]' % (left_scan, front_scan))
        self.front_sensor = front_scan
        self.left_sensor = left_scan


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
