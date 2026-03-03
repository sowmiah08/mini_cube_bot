import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    package_name = 'mini_bot_description'

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

    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', 'mini_bot_world.sdf'],
        output='screen'
    )

    return LaunchDescription([
        rsp,
        gazebo,
    ])