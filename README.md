# AirSim_VIO_Data_Collection
This project is used to collect VIO Data in AirSim.(High FPS and Strictly Syc)

Data Collection Steps:
1. Change your "~/Document/AirSim/settings.json" to "car.json"
2. GET IMU_GT: Change your own path in "get_imu_and_odo.py" and run "python3 get_imu_and_odo.py"
3. Use KEYBOARD to control the car: Run "python3 keyControl" and press keys to control the car.
4. Change your "~/Document/AirSim/settings.json" to "cv.json"
5. Capture Image at fixed GT Pose: Change your own path in "cv_capture_from_pose.py" and run "python3 cv_capture_from_pose.py"
6. Merge Data to a single rosbag with time offset: Change your own path in "image_topic.py" and run "python3 image_topic.py"
