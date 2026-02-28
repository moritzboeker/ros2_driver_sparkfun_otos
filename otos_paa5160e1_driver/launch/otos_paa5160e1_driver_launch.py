from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='otos_paa5160e1_driver',
            executable='otos_paa5160e1_node',
            name='optical_odometry_driver',
            output='screen',
        ),
    ])

