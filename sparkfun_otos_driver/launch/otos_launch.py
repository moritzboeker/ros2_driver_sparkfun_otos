# Copyright 2026 Moritz Emanuel Boeker
# SPDX-License-Identifier: MIT
"""Launch the SparkFun OTOS driver with parameters from a YAML file."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Generate the launch description for the OTOS driver node."""
    default_params = str(
        Path(get_package_share_directory('sparkfun_otos_driver'))
        / 'config' / 'otos_params.yaml')

    return LaunchDescription([
        DeclareLaunchArgument(
            'params_file',
            default_value=default_params,
            description='Path to the ROS parameters file for the OTOS driver'),
        Node(
            package='sparkfun_otos_driver',
            executable='otos_node',
            name='otos',
            output='screen',
            parameters=[LaunchConfiguration('params_file')],
        ),
    ])
