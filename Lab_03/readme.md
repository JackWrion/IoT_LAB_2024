## BRIEF
This lab implemented simple handshaking between Gateway and the Sensors.

When Gateway sends Command, such as "Turn on LED" or "Turn off Heater", the Sensors should respond "ACK" to assure that the Sensors are still alive and working properly.

If The Gateway doesn't receive any response after 5 times resent, it will return ERROR.  

## PREREQUIREMENTS and BUILD:

This project run on WINDOW.

Installed com0com

Installed Hercules Terminal

## HOW TO USE

- 1. Create 2 virtual Port with com0com
In my case, there are 2 ports, namely COM5 and COM6.

- 2. Assign one of two ports to Hercules
My Hercules Terminal is opened with port COM5

- 3. Customize your dashboard on Adafruit
A button is assigned to feed "led"

Another button is assigned to feed "water-heater"

A slider is assigned to feed "air-conditioner"

- 4. Clone this project and run main.py
Remember change USERNAME and PASSWORD in main.py (on line 12 and 14) 

- 5. Monitoring using dashboard
Using button and slider on your dashboard to send data

Don't forget using Herculer to respond "0:ack:0"

## EXAMPLE AND DEMO
Have a look at my dashboard: https://io.adafruit.com/jackwr/dashboards/my-smart-home

Please watch video demo here: https://youtu.be/ORejBR28rXw





