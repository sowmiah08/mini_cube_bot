import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'mini_bot_description'
    pkg_share = get_package_share_directory(package_name)

    world_file = os.path.join(
        pkg_share,
        'worlds',
        'mini_bot_world.sdf'
    )
#start robot state publisher
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(package_name),
                'launch',
                'rsp.launch.py'
            )
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )
#open gazebo with given worldfile
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_file],
        output='screen'
    )
#spawn robot into the gazebo file 
    spawn = Node(
        package = 'ros_gz_sim',
        executable = 'create',
        arguments = [
            '-topic' , 'robot_description','-name', 'mini_bot'
        ],
        output = 'screen'
    )
#bridge ros and gazebo so that it can listen to /cmd_vel
    bridge = Node(
        package = 'ros_gz_bridge',
        executable = 'parameter_bridge',
        arguments = [
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'
        ],
        output = 'screen'
    )

    return LaunchDescription([
        rsp,
        gazebo,
        spawn,
        bridge
    ])