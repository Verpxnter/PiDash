import pynvml
from flask import Flask, jsonify, render_template
import psutil
import shutil
import time
import RPi.GPIO as GPIO
import subprocess

app = Flask(__name__)

network_history = []

def get_temperature():
    temp = psutil.sensors_temperatures(fahrenheit=False)
    return {"temperature": temp['cpu_thermal'][0].current}

def get_gpu_temperature():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)
    temp = GPIO.input(17)
    return {"gpu_temperature": temp}


def get_ram_usage():
    memory_info = psutil.virtual_memory()
    total_mb = memory_info.total / (1024 ** 2)
    if total_mb < 1024:
        return {
            "total": f"{total_mb:.2f} MB",
            "available": f"{memory_info.available / (1024 ** 2):.2f} MB",
            "used": f"{memory_info.used / (1024 ** 2):.2f} MB",
            "free": f"{memory_info.free / (1024 ** 2):.2f} MB"
        }
    else:
        return {
            "total": f"{total_mb / 1024:.2f} GB",
            "available": f"{memory_info.available / (1024 ** 3):.2f} GB",
            "used": f"{memory_info.used / (1024 ** 3):.2f} GB",
            "free": f"{memory_info.free / (1024 ** 3):.2f} GB"
        }


def get_disk_usage():
    total, used, free = shutil.disk_usage("/")
    total_mb = total / (1024 ** 2)
    if total_mb < 1024:
        return {
            "total": f"{total_mb:.2f} MB",
            "used": f"{used / (1024 ** 2):.2f} MB",
            "free": f"{free / (1024 ** 2):.2f} MB"
        }
    else:
        return {
            "total": f"{total_mb / 1024:.2f} GB",
            "used": f"{used / (1024 ** 3):.2f} GB",
            "free": f"{free / (1024 ** 3):.2f} GB"
        }

def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq < 1000:
        return {
            "cpu": cpu_percent,
            "cpu_speed": f"{cpu_freq:.2f} MHz"
        }
    else:
        return {
            "cpu": cpu_percent,
            "cpu_speed": f"{cpu_freq / 1000:.2f} GHz"
        }

# def get_gpu_usage():
#     gpus = GPUtil.getGPUs()
#     if len(gpus) > 0:
#         gpu = gpus[0]

#         gpu_percent = gpu.load * 100
#         gpu_memory_total = gpu.memoryTotal
#         gpu_memory_used = gpu.memoryUsed
#         gpu_memory_free = gpu_memory_total - gpu_memory_used

#         # print("Raw GPU Memory Total (MB):", gpu_memory_total)
#         # print("Raw GPU Memory Used (MB):", gpu_memory_used)

#         gpu_memory_total_gb = gpu_memory_total / 1024
#         gpu_memory_used_gb = gpu_memory_used / 1024
#         gpu_memory_free_gb = gpu_memory_free / 1024

#         gpu_memory_total_formatted = f"{gpu_memory_total_gb:.2f}"
#         gpu_memory_used_formatted = f"{gpu_memory_used_gb:.2f}"
#         gpu_memory_free_formatted = f"{gpu_memory_free_gb:.2f}"

#         # print("Formatted GPU Memory (GB):", gpu_memory_total_formatted)

#         return {
#             "gpu": gpu_percent,
#             "total": f"{gpu_memory_total_formatted} GB",
#             "used": f"{gpu_memory_used_formatted} GB",
#             "gpu_memory_free": f"{gpu_memory_free_formatted} GB"
#         }
#     else:
#         gpu_percent = 0
#         gpu_memory_total = "N/A"
#         gpu_memory_used = "N/A"
#         gpu_memory_free = "N/A"

#     return {
#         "gpu": gpu_percent,
#         "total": gpu_memory_total,
#         "used": gpu_memory_used,
#         "gpu_memory_free": gpu_memory_free
#     }

def get_gpu_usage():
    output = subprocess.check_output(['vcgencmd', 'get_mem gpu'])
    gpu_memory = output.decode('utf-8').split('=')[1].strip('\n').replace('M', '') 
    gpu_memory = int(gpu_memory) 

    output_used = subprocess.check_output(['vcgencmd', 'get_mem gpu_used'])
    gpu_memory_used = output_used.decode('utf-8').split('=')[1].strip('\n').replace('M', '')  
    gpu_memory_used = int(gpu_memory_used) 

    gpu_memory_free = gpu_memory - gpu_memory_used
    gpu_memory_percent = (gpu_memory_used / gpu_memory) * 100

    def format_size(size):
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size / 1024 / 1024:.2f} MB"
        
    # print(format_size(gpu_memory * 1024 * 1024))
    # print(format_size(gpu_memory_used * 1024 * 1024))
    # print(format_size((gpu_memory - gpu_memory_used) * 1024 * 1024))
    # print(f"{gpu_memory_percent:.2f}%")

    return {
        "total": format_size(gpu_memory * 1024 * 1024), 
        "used": format_size(gpu_memory_used * 1024 * 1024),
        "free": format_size((gpu_memory - gpu_memory_used) * 1024 * 1024), 
        "gpu": f"{gpu_memory_percent:.1f}"
    }

def get_network_usage():
    net_io = psutil.net_io_counters()
    return {
        "sent": net_io.bytes_sent / (1024 ** 2),  
        "received": net_io.bytes_recv / (1024 ** 2)  
    }

def get_uptime():
    boot_time = psutil.boot_time()
    current_time = time.time()
    uptime = current_time - boot_time

    seconds = uptime % 60
    minutes = (uptime / 60) % 60
    hours = (uptime / 60 / 60) % 24
    days = uptime / 60 / 60 / 24

    days = round(days, 2)
    hours = round(hours, 2)
    minutes = round(minutes, 2)
    seconds = round(seconds, 2)
    return(uptime)

@app.route('/reboot', methods=['POST'])
def reboot():
    subprocess.call(['sudo', 'shutdown', '-r', 'now'])
    return jsonify({'message': 'System rebooting...'})

@app.route('/stop', methods=['POST'])
def stop():
    subprocess.call(['sudo', 'shutdown', '-h', 'now'])
    return jsonify({'message': 'System stopping...'})

@app.route('/stats')
def get_stats():
    global network_history

    stats = {
        "cpu": get_cpu_usage(),
        "gpu": get_gpu_usage(),
        "ram": get_ram_usage(),
        "disk": get_disk_usage(),
        "cpu_temperature": get_temperature(),
        "gpu_temperature": get_gpu_temperature(),
        "network": get_network_usage(),
        "uptime": get_uptime()
    }

    current_time = time.time() * 1000
    network_history.append({
        "time": current_time,
        "sent": stats["network"]["sent"],
        "received": stats["network"]["received"]
    })

    network_history = network_history[-30:]

    stats["network_history"] = network_history

    return jsonify(stats)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="6969")
