# PiDash
Welcome to `PyDash` — a sleek and simple real-time system monitoring dashboard for your Raspberry Pi (or any Linux-based system). Track your **CPU, RAM, Disk, GPU stats, network usage,** and **uptime** like a pro. Perfect for keeping an eye on your Pi's performance and getting instant insights on system health!

## 1. Introduction
`PyDash` is a Flask-powered web app that displays live stats of your system, including CPU usage, RAM consumption, Disk space, and GPU performance. It's designed with Raspberry Pi in mind, but you can use it on most Linux systems.

You can also use PyDash to reboot or shut down your system directly from the `dashboard`! No need to **SSH** every time — just a click of a button, and you're in control.

## 2. Features
- **CPU Stats**: Get detailed info on `CPU usage` and frequency.
- **RAM Overview**: See the total, used, available, and free memory of your system.
- **Disk Usage**: Monitor total, used, and free disk space.
- **GPU Info**: For Raspberry Pi users, get insights into GPU memory usage.
- **Network Traffic**: Check how much data has been sent and received.
- **Temperature**: Monitor `CPU` and `GPU temperatures` (Pi users will love this).
- **Uptime**: See how long your system has been running since the last reboot.
- **Remote Control**: Reboot or shut down your system remotely with a simple click!

## 3. How It Works
- **CPU Monitoring**: Displays current CPU percentage and frequency (GHz or MHz).
- **GPU Tracking**: For Raspberry Pi, it grabs GPU memory stats using `vcgencmd`. (More GPU details can be added for other systems using `pynvml`).
- **RAM and Disk**: Real-time stats on your memory and storage, with clean and simple formatting.
- **Network Data**: Shows cumulative network data sent/received in megabytes.
- **System Uptime**: Calculates the time since your last reboot.

Once installed, just open your browser, and you'll see all the juicy system stats in real-time.

## 4. Installation and Setup
Make sure you have Python 3.x installed and follow these steps to get started:

### ╳ Clone The Repository
```bash
git clone https://github.com/verpxnter/PyDash.git
cd PyDash
```

### ╳ Install the Requirements
```bash
pip install -r requirements.txt
```

### ╳ Run the Application
```bash
python app.py
```

### ╳ Connect to the Pannel
Just go into ur Browser and go on:
```bash
http://<IP_HERE>:6969
```

## 5. Requirements
- **Python 3.x**: Make sure it's installed.
- **Flask**: For the web framework.
- **psutil**: To monitor system performance (CPU, RAM, disk).
- **RPi.GPIO**: To access Raspberry Pi's GPIO (used for reading GPU temp).
- **shutil**: For disk usage.
- **subprocess**: For executing system commands like rebooting or getting GPU memory usage.


## 6. Final Words
This project is meant for **fun** and to help you `monitor` your system’s performance. Enjoy using `PyDash` on your Raspberry Pi, and feel free to tweak it to your needs.

**So now, just have fun with it and enojoy!!!!**
