# ROS2 Docker Camera Calibration
This repo lets you calibrate USB cams, and realsenses, using either opencv
chessboards or charuco boards.

This is not a ros2 package.

This repo makes use of this awesome ROS2 package:
https://docs.ros.org/en/jazzy/p/camera_calibration/doc/index.html

The project is still being tweaked as of 20260825.

## Setup
Install docker engine:
https://docs.docker.com/engine/install/

**Nvidia Container Tookit** (Optional):
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#with-apt-ubuntu-debian

```bash
docker compose build

# different nodes:
docker compose up cam2image
docker compose up realsense
docker compose up charuco-calibration
docker compose up chessboard-calibration
docker compose up rviz  # then find the realsense topic

# once calibration is done
docker cp <container_name>:/tmp/calibrationdata.tar.gz ./calibration_data/calibrationdata.tar.gz
```

TODO: add instructions for finding and printing charucoboards
TODO(?): add script for generating charuco boards and chessboards using opencv

### cam2image
This is a generic usb cam node inside the ROS2 package image_tools

https://index.ros.org/p/image_tools/#jazzy  
https://github.com/ros2/demos

You can configure this node using the params file inside ```./params/cam2image_params.yaml``` 

### realsense
TODO: test this on a fresh ubuntu install. what dependencies does one need to install?

This is a generic node for getting output from an intel realsense camera. I
personally own a D435i, so this node was made with that camera in mind.

You can configure it with ```./params/realsense_params.yaml```

### useful links
This is what I used to make advanced.json (for the realsense). I took it from the "Hand" preset:
- [Realsense Advanced Presets](https://github.com/realsenseai/librealsense/wiki/D400-Series-Visual-Presets)
