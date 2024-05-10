## BRIEF
This mini project implements SmartHome Application. It includes 4 components: Gateway, Devices, App Mobile, and Dashboard

## PREREQUIREMENTS and BUILD:

This project runs on WINDOW.

Gateway is implemented in Python Environment

App Mobile is built by Android Studio

Dashboard is utilized on Adafruit IO platfrom


## HOW TO USE

- 1. **App Mobile**

    The folder "My_Android_MQTT_App" is used to build the App. Go to the MQTTHelper class and change your Host, Username, Password, etc.

    You also can go back to LAB_04 and find documents describing my Android App.

- 2. **Gateway**

    Change your MQTT Client Host, Username, Password, etc. You also should go to Google Teachable Machine to train your own model. Otherwise, it still works but cannot recognize your face.

   Go to Lab_02 for further insights into my AI application.

    Finally, run only "**main.py**"

- 3. **Customize your dashboard on Adafruit**

    A button is assigned to feed "led"

    Another button is assigned to feed "water-heater"

    A slider is assigned to feed "air-conditioner"

- 4. **Devices**

    This depends on my Device. But briefly, you need an ESP32 module that integrates DHT11, some LEDs, and connects to WiFi. Then, it will work as an MQTT Client publish Temperature, Humdity, etc. and receives commands for monitoring LEDs or something.

- 4. **Clone this project and run main.py**

    Remember to change USERNAME and PASSWORD in main.py (on line 12 and 14) 


## EXAMPLE AND DEMO
Have a look at my dashboard: https://io.adafruit.com/jackwr/dashboards/my-smart-home

Please watch the video demo here: [https://youtu.be/ORejBR28rXw
](https://youtu.be/vw6Z-bhbDwc)




