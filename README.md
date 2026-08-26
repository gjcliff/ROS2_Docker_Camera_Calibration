# ROS2 Docker Camera Calibration
This repo lets you calibrate USB cams, and realsenses, using either opencv
chessboards or charuco boards.

It makes use of this awesome ROS2 package:
https://docs.ros.org/en/jazzy/p/camera_calibration/doc/index.html

This project is still being tweaked as of 20260819.

## Setup
Install docker engine:
https://docs.docker.com/engine/install/

**Nvidia Container Tookit** (Optional(?)):
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#with-apt-ubuntu-debian

```bash
docker compose build
docker compose up realsense
docker compose up usb_cam
docker compose up realsense rviz
docker compose up realsense calibration

# once calibration is done
docker cp <container_name>:/tmp/calibrationdata.tar.gz ./calibration_data/calibrationdata.tar.gz
```

### useful links
This is what I used to make advanced.json (for the realsense). I took it from the "Hand" preset:
- [Realsense Advanced Presets](https://github.com/realsenseai/librealsense/wiki/D400-Series-Visual-Presets)
