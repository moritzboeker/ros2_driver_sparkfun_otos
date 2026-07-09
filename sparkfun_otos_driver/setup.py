from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'sparkfun_otos_driver'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=[
        'setuptools',
        'sparkfun-qwiic-otos',
    ],
    zip_safe=True,
    maintainer='Moritz Emanuel Boeker',
    maintainer_email='moritz.boeker@public-files.de',
    description="ROS 2 driver for SparkFun's Optical Tracking Odometry Sensor "
                '(OTOS, PAA5160E1). Publishes nav_msgs/Odometry and optionally '
                'broadcasts the odom transform.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'otos_node = sparkfun_otos_driver.otos_node:main',
        ],
    },
)
