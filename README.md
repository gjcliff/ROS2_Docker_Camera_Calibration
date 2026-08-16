# Realsense D435i Camera Calibration
This repo lets you calibrate your realsense of this specific model using either
opencv chessboards or charuco boards.

## Setup
Install docker engine:
https://docs.docker.com/engine/install/

```bash
docker compose build
docker compose up realsense
docker compose up realsense rviz
docker compose up realsense calibration
```

### useful links
[Realsense Advanced Presets](https://github.com/realsenseai/librealsense/wiki/D400-Series-Visual-Presets)
