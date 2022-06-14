# Summary of AWS DeepRacer Manual Mode APIs

## List of Exposed APIs

| HTTP Method | API | Data | Description | Link |
| -- | -- | -- | -- | -- |
| GET | api/models | | Get AI model list | |
| GET | api/drive_mode | {"drive_mode": "manual&#124;auto"} | Drive car in AI or manual mode. Looks for 'manual' otherwise AI | |
| GET | api/is_usb_connected | | Is there a USB connection? | |
| GET | api/get_battery_level | | What is battery level from 1-10 | |
| "PUT|POST" | api/manual_drive | {"angle": steering_angle, "throttle": throttle, "max_speed": max_speed} Used to steer the car. angle and throttle are both float values between -1.0 and 1.0. max_speed is float value ranging from 0.0 to 1.0 | https://github.com/aws-deepracer/aws-deepracer-webserver-pkg/blob/main/webserver_pkg/webserver_pkg/vehicle_control.py |
| PUT | api/max_nav_throttle | {"throttle": throttle_percent} | Throttle mutiplier from -1 to 1 | https://github.com/aws-deepracer/aws-deepracer-webserver-pkg/blob/main/webserver_pkg/webserver_pkg/vehicle_control.py |
| PUT | api/start_stop | {"start_stop": "start&#124;stop"} | Start or stop the car | https://github.com/aws-deepracer/aws-deepracer-webserver-pkg/blob/main/webserver_pkg/webserver_pkg/vehicle_control.py |
| GET | /route?topic=/camera_pkg/display_mjpeg&width=640&height=480 | | Video feed from the car | |



