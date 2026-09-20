# stage 1: build as root, nothing to fight with permissions
FROM ros:jazzy-ros-base AS builder
ENV DEBIAN_FRONTEND=noninteractive

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends python3-colcon-common-extensions \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /ros_ws
COPY ./external/ src/

RUN apt-get update \
    && rosdep update \
    && rosdep install --from-paths src --ignore-src -y \
    && rm -rf /var/lib/apt/lists/*

RUN . /opt/ros/jazzy/setup.sh \
    && colcon build --packages-select camera_calibration


# stage 2: runtime image
FROM ros:jazzy-ros-base AS runtime
ARG USER_UID=1000
ARG USER_GID=1000
ARG USERNAME=user
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-pydantic \
    ros-${ROS_DISTRO}-librealsense2 \
    ros-${ROS_DISTRO}-realsense2-camera \
    ros-${ROS_DISTRO}-realsense2-description \
    ros-${ROS_DISTRO}-image-tools \
    ros-${ROS_DISTRO}-rviz2 \
    && rm -rf /var/lib/apt/lists/*

# runtime deps of the built package, read from its package.xml without copying the source in
RUN --mount=type=bind,from=builder,source=/ros_ws/src,target=/tmp/src \
    apt-get update \
    && rosdep update \
    && rosdep install --from-paths /tmp/src --ignore-src --dependency-types=exec -y \
    && rm -rf /var/lib/apt/lists/*

# same path as the builder, since install/ has absolute paths baked in
COPY --from=builder /ros_ws/install /ros_ws/install

RUN userdel -r ubuntu 2>/dev/null || true \
    && groupdel ubuntu 2>/dev/null || true \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

USER $USERNAME

COPY ./launch.py /launch.py
COPY ./params/ /params/
COPY --chmod=755 ./calib_entrypoint.sh /calib_entrypoint.sh

ENTRYPOINT ["/calib_entrypoint.sh"]
