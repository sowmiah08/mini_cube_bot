from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    pkg_mini_bot = FindPackageShare('mini_bot_description')

    default_model_path = PathJoinSubstitution(
        [pkg_mini_bot, 'urdf', 'mini_bot.urdf.xacro']
    )

    default_rviz_config_path = PathJoinSubstitution(
        [pkg_mini_bot, 'rviz', 'urdf.rviz']
    )

    gui_arg = DeclareLaunchArgument(
        'gui', default_value='true',
        description='Enable joint_state_publisher_gui'
    )

    model_arg = DeclareLaunchArgument(
        'model', default_value=default_model_path,
        description='Absolute path to robot URDF file'
    )

    rviz_arg = DeclareLaunchArgument(
        'rvizconfig', default_value=default_rviz_config_path,
        description='RViz config file'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', LaunchConfiguration('model')])
        }]
    )

    joint_state_publisher = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=None
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        output='screen'
    )

    return LaunchDescription([
        gui_arg,
        model_arg,
        rviz_arg,
        robot_state_publisher,
        joint_state_publisher,
        rviz
    ])
