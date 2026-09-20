# bootleg ros2 launch file

from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import (
    EqualsSubstitution,
    LaunchConfiguration,
)
from launch_ros.actions import Node

from launch import LaunchDescription


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_realsense",
                default_value="false",
            ),
            DeclareLaunchArgument(
                "realsense_params_filepath",
                default_value="/params/realsense_params.yaml",
            ),
            DeclareLaunchArgument(
                "use_cam2image",
                default_value="false",
            ),
            DeclareLaunchArgument(
                "do_calibration",
                default_value="false",
            ),
            DeclareLaunchArgument(
                "calibration_board",
                default_value="",
                choices=["charuco", "checkerboard", ""],
            ),
            DeclareLaunchArgument(
                "checkerboard_size",
                default_value="5x7",
            ),
            DeclareLaunchArgument(
                "checker_board_square_len",
                default_value="0.032",
            ),
            DeclareLaunchArgument("output_path", default_value="/calibration_data"),
            DeclareLaunchArgument("camera_name", default_value="camera"),
            DeclareLaunchArgument(
                "log_level",
                default_value="info",
            ),
            Node(
                package="realsense2_camera",
                namespace="",
                executable="realsense2_camera_node",
                name=LaunchConfiguration("camera_name"),
                # parameters=["/params/realsense_params.yaml"],
                remappings=[
                    (
                        (LaunchConfiguration("camera_name"), "/infra1/image_rect_raw"),
                        (LaunchConfiguration("camera_name"), "/image_raw"),
                    ),
                    (
                        (LaunchConfiguration("camera_name"), "/infra1/camera_info"),
                        (LaunchConfiguration("camera_name"), "/camera_info"),
                    ),
                ],
                arguments=[
                    "--ros-args",
                    "--log-level",
                    LaunchConfiguration("log_level"),
                    "--ros-args",
                    "--params-file",
                    LaunchConfiguration("realsense_params_filepath")
                ],
                condition=IfCondition(LaunchConfiguration("use_realsense")),
            ),
            Node(
                package="image_tools",
                namespace="",
                executable="cam2image",
                parameters=["/params/cam2image_params.yaml"],
                arguments=[
                    "--ros-args",
                    "--log-level",
                    LaunchConfiguration("log_level"),
                ],
                remappings=[
                    ("image", (LaunchConfiguration("camera_name"), "/image_raw")),
                ],
                condition=IfCondition(LaunchConfiguration("use_cam2image")),
            ),
            Node(
                package="camera_calibration",
                namespace="",
                executable="cameracalibrator",
                name="cam2image",
                arguments=[
                    "--no-service-check",
                    "--size",
                    LaunchConfiguration("checkerboard_size"),
                    "--square",
                    LaunchConfiguration("checker_board_square_len"),
                    "--pattern",
                    "charuco",
                    "--charuco_marker_size",
                    "0.0246",
                    "--aruco_dict",
                    "6x6_250",
                    "--output_path",
                    LaunchConfiguration("output_path"),
                    "--ros-args",
                    "--log-level",
                    LaunchConfiguration("log_level"),
                ],
                remappings=[
                    ("image", (LaunchConfiguration("camera_name"), "/image_raw")),
                    ("camera", LaunchConfiguration("camera_name")),
                ],
                condition=IfCondition(
                    EqualsSubstitution(
                        LaunchConfiguration("calibration_board"), "charuco"
                    )
                ),
            ),
            Node(
                package="camera_calibration",
                namespace="",
                executable="cameracalibrator",
                name="cam2image",
                arguments=[
                    "--no-service-check",
                    "--size",
                    LaunchConfiguration("checkerboard_size"),
                    "--square",
                    LaunchConfiguration("checker_board_square_len"),
                    "--ros-args",
                    "--log-level",
                    LaunchConfiguration("log_level"),
                ],
                remappings=[
                    ("image", (LaunchConfiguration("camera_name"), "/image_raw")),
                    ("camera", LaunchConfiguration("camera_name")),
                ],
                condition=IfCondition(
                    EqualsSubstitution(
                        LaunchConfiguration("calibration_board"), "checkerboard"
                    )
                ),
            ),
        ]
    )
