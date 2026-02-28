import math
import qwiic_otos
from qwiic_otos import Pose2D
import sys
import time
import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Quaternion
from nav_msgs.msg import Odometry

def quaternion_from_euler(ai, aj, ak):
    ai /= 2.0
    aj /= 2.0
    ak /= 2.0
    ci = math.cos(ai)
    si = math.sin(ai)
    cj = math.cos(aj)
    sj = math.sin(aj)
    ck = math.cos(ak)
    sk = math.sin(ak)
    cc = ci*ck
    cs = ci*sk
    sc = si*ck
    ss = si*sk

    q = Quaternion()
    q.x = cj*sc - sj*cs
    q.y = cj*ss + sj*cc
    q.z = cj*cs - sj*sc
    q.w = cj*cc + sj*ss

    return q

class OpticalOdometryDriver(Node):

    def __init__(self) -> None:
        super().__init__('optical_odometry_driver')
        self.odom_pub_ = self.create_publisher(Odometry, 'odom', 10)
        publish_frequency = 20 # [Hz]
        self.timer = self.create_timer(1/publish_frequency, self.timer_cb)
        self.otosDev = qwiic_otos.QwiicOTOS()
        self.otos_init()
        self.pose = qwiic_otos.Pose2D()
        self.vel = qwiic_otos.Pose2D()
        self.pose_std_dev = qwiic_otos.Pose2D()
        self.vel_std_dev = qwiic_otos.Pose2D()

    def otos_init(self):
        if self.otosDev.is_connected() == False:
            self.get_logger().error("The device isn't connected to the system. Please check the I2C connection.")
            self.is_ready = False
            return
        self.otosDev.begin()
        self.otosDev.setLinearUnit(self.otosDev.kLinearUnitMeters)
        self.otosDev.setAngularUnit(self.otosDev.kAngularUnitRadians)
        self.otosDev.setLinearScalar(1.0)
        self.otosDev.setAngularScalar(1.0)

        self.get_logger().info("Calibrating IMU and reset tracking")
        self.otosDev.calibrateImu()
        self.otosDev.resetTracking()
        self.get_logger().info("OTOS is ready!")
        self.is_ready = True
        return

    def publish_odom(self):
        msg = Odometry()
        msg.child_frame_id = 'base_link'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'odom'
        msg.pose.pose.position.x = self.pose.x
        msg.pose.pose.position.y = self.pose.y
        msg.pose.pose.orientation = quaternion_from_euler(0.0, 0.0, self.pose.h)
        msg.pose.covariance = [
            self.pose_std_dev.x**2, 0.0, 0.0, 0.0, 0.0, 0.0, # x     [m]
            0.0, self.pose_std_dev.y**2, 0.0, 0.0, 0.0, 0.0, # y     [m]
            0.0, 0.0, 9999.0, 0.0, 0.0, 0.0,            # z     [m]   (unknown)
            0.0, 0.0, 0.0, 9999.0, 0.0, 0.0,            # roll  [rad] (unknown)
            0.0, 0.0, 0.0, 0.0, 9999.0, 0.0,            # pitch [rad] (unknown)
            0.0, 0.0, 0.0, 0.0, 0.0, self.pose_std_dev.h**2    # yaw   [rad]
        ]
        msg.twist.twist.linear.x = self.vel.x
        msg.twist.twist.linear.y = self.vel.y
        msg.twist.twist.angular.z = self.vel.h
        msg.twist.covariance = [
            self.vel_std_dev.x**2, 0.0, 0.0, 0.0, 0.0, 0.0, # x     [m/s]
            0.0, self.vel_std_dev.y**2, 0.0, 0.0, 0.0, 0.0, # y     [m/s]
            0.0, 0.0, 9999.0, 0.0, 0.0, 0.0,            # z     [m/s]   (unknown)
            0.0, 0.0, 0.0, 9999.0, 0.0, 0.0,            # roll  [rad/s] (unknown)
            0.0, 0.0, 0.0, 0.0, 9999.0, 0.0,            # pitch [rad/s] (unknown)
            0.0, 0.0, 0.0, 0.0, 0.0, self.vel_std_dev.h**2    # yaw   [rad/s]
        ]
        self.odom_pub_.publish(msg)

    def publish_tf(self):
        pass

    def timer_cb(self):
        self.pose = self.otosDev.getPosition()
        self.vel = self.otosDev.getVelocity()
        self.pose_std_dev = self.otosDev.getPositionStdDev()
        self.vel_std_dev = self.otosDev.getVelocityStdDev()

        self.publish_odom()
        self.publish_tf()



def main(args=None):
    rclpy.init(args=args)

    ood = OpticalOdometryDriver()
    if not ood.is_ready:
        ood.get_logger().fatal("Node initialization failed.")
        ood.destroy_node()
        rclpy.shutdown()
        return
    rclpy.spin(ood)
    ood.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
