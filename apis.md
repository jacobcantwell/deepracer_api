# Summary of AWS DeepRacer Manual Mode APIs

## List of Exposed APIs

| HTTP Method | API | Data | Description | Link |
| -- | -- | -- | -- | -- |
| GET | api/models | | Get AI model list | |
| GET | api/drive_mode | {"drive_mode": "auto|manual"} | Drive car in AI or manual mode | |
| GET | api/is_usb_connected | | Is there a USB connection? | |
| GET | api/get_battery_level | | What is battery level from 1-10 | |
| PUT | api/manual_drive | {"angle": steering_angle, "throttle": throttle, "max_speed": max_speed} | Used to steer the car | https://github.com/aws-deepracer/aws-deepracer-webserver-pkg/blob/main/webserver_pkg/webserver_pkg/vehicle_control.py |
| PUT | api/max_nav_throttle | {"throttle": throttle_percent} | Throttle mutiplier from -1 to 1 | |
| PUT | api/start_stop | {"start_stop": "start|stop"} | Start or stop the car | |
| GET | /route?topic=/camera_pkg/display_mjpeg&width=640&height=480 | | Video feed from the car | |



