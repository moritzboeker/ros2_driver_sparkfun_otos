import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'otos_paa5160e1_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
    install_requires=[
        'setuptools',
        'sparkfun-qwiic-otos',
    ],
    zip_safe=True,
    maintainer='Moritz Emanuel Boeker',
    maintainer_email='info@example.com',
    description='Publish odometry as topic and tf based on Sparkfun\'s Optical Tracking Odometry Sensor (OTOS) of type PAA5160E1',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'otos_paa5160e1_node = otos_paa5160e1_driver.otos_paa5160e1_node:main'
        ],
    },
)
