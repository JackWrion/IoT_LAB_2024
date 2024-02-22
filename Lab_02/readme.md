## INTRODUCTION
This lab implemented to integrate Google AI Teachable Machine and emulate UART serial sensors' data processing

## PREREQUIREMENTS and BUILD:
Firstly, these are my hardware and software version/requirements.

NOTICE: This project run on LINUX.

```
ubuntu: 23.10
python: 3.11.6
cudnn_version: 8    
cuda_version: 12.2
```

Then, install this site-packages for AI application

```
sudo apt install nvidia-cuda-toolkit
pip install tensorflow[and-cuda]
pip install keras
```

and install this for emulating virtual serial communication via UART

```
sudo apt install socat
sudo apt install minicom
```

## HOW TO USE

- 1. Open your first terminal to produce 2 virtual port (already connected with each other)
```
socat -d -d pty , rawer , echo =0 pty , rawer , echo =0
```
It will generate 2 port, according to your case, please connect correctly to appearanced ports in your terminal

- 2. Open another terminal to write sensors' data
'Cause, my case is /dev/pts/2 and dev/pts/3, so port2 will be assign to Minicom
```
sudo minicom -b 115200 -D /dev/pts/2
```
Then, you can type anything to this terminal and the data will be transmited to port3

- 3. Open main.py, in line 58, change the name of the other port (dev/pts/3)
And run main.py



## EXAMPLE AND DEMO
Have a look at my dashboard: https://io.adafruit.com/jackwr/dashboards/my-smart-home

Please watch video demo here: https://www.youtube.com/watch?v=iVC1UfYrC3M





