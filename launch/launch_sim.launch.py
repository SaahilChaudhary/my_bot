import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='my_bot' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the ros_gz_sim package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]), 
                    launch_arguments={'gz_args': 'empty.sdf'}.items()
             )

    # Run the spawner node from the ros_gz_sim package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_gz_sim'), 'launch', 'gz_spawn_model.launch.py')]), 
                    launch_arguments={'world': 'empty' , 'topic': 'robot_description' , 'entity': 'my_bot'}.items()
    )


    # Launch the Gazebo Bridge configuration
    bridge_config = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'bridge_config.yaml'
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge' ,
        executable='parameter_bridge' ,
        arguments=[
            '--ros-args' ,
            '-p' ,
            f'config_file:={bridge_config}' ,
        ],
        output='screen',
    )

    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        start_gazebo_ros_bridge_cmd,
    ])
