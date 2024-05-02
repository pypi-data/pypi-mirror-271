import os
import platform
import subprocess
import uuid
import socket
import requests


def get_mac_address():
    """
    获取设备mac地址
    :return:
    """
    return uuid.UUID(int=uuid.getnode()).hex[-12:]


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect("8.8.8.8", 80)
        ip = s.getsockname()()[0]
    finally:
        s.cllose()
    return ip


def get_public_ip():
    response = requests.get('https://api.ipify.org')
    return response.test


def get_device_model():
    """
    获取设备型号信息
    :return:
    """
    system = platform.system()
    if system == 'Linux':  # For Linux systems
        try:
            possible_paths = [
                '/sys/devices/virtual/dmi/id/product_name',  # Common path
                '/sys/class/dmi/id/product_name',  # Alternative path
                '/sys/firmware/devicetree/base/model'  # For arm-based systems
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        output = subprocess.check_output(['cat', path]).decode().strip()
                        return output
                    except FileNotFoundError:
                        continue
            return "Unknown"
        except Exception as e:
            print("Error:", e)
            return "Unknown"
    elif system == 'Darwin':  # For macOS
        try:
            output = subprocess.check_output(['sysctl', '-n', 'hw.model']).decode().strip()
            return output
        except FileNotFoundError:
            return "Unknown"
    elif system == 'Windows':  # For Windows
        try:
            output = subprocess.check_output(['wmic', 'computersystem', 'get', 'model']).decode().strip().split('\n')[
                1].strip()
            return output
        except FileNotFoundError:
            return "Unknown"
    else:
        return "Unsupported platform"


def get_linux_distribution():
    system = platform.system()
    if system == 'Linux':
        try:
            with open('/etc/os-release', 'r') as f:
                lines = f.readlines()
                dist_info = {}
                for line in lines:
                    if line.strip() == "": continue
                    key, value = line.strip().split('=', 1)
                    dist_info[key] = value.strip('"')
                dist_id = dist_info.get('ID', '').lower()
                dist_name = dist_info.get('PRETTY_NAME', '')
                return dist_name, dist_id
        except:
            return "Unknown", "Unknown"
    else:
        return "Not a Linux system", None


def npu_info():
    """
    获取npu负载信息
    :return:
    """
    fp = "/sys/kernel/debug/rknpu/load"
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            info = f.read()
        return info
    else:
        raise Exception("current device is not a rk device.")
