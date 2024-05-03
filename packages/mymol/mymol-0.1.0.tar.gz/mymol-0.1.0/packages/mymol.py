import psutil, platform, shutil, GPUtil, wmi

class mymodule:
    class terminal:
        def print_colored(self, text, color):
            colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'reset': '\033[0m'
            }
            return(f"{colors[color]}{text}{colors['reset']}")
        def move_cursor(self, row, col):
            print(f"\033[{row};{col}H", end="")
        def clear_terminal(self):
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
        def progress_bar(self, progress, total, bar_length=20):
            percent = 100 * (progress / float(total))
            bar = '█' * int(percent / (100 / bar_length)) + '-' * (bar_length - int(percent / (100 / bar_length)))
            print(f"\r|{bar}| {percent:.2f}%", end="\r")
            if progress == total:
                print()
        def blink_text(self, text):
            import time
            blink = True
            while True:
                if blink:
                    print(f"\033[5m{text}\033[0m", end="\r")
                else:
                    print(f"{' ' * len(text)}", end="\r")
                blink = not blink
                time.sleep(0.5)
    class performance_monitor:
        def __init__(self):
            pass
        class version:
            def version():
                """Returns the version of the operating system.
                Example:
                >>> version()
                '10.0.19041'
                """
                return platform.version()
            def release():
                """Returns the release of the operating system.
                Example:
                >>> release()
                '2004'
                """
                return platform.release()
            def system():
                """Returns the system of the operating system.
                Example:
                >>> system()
                'Windows'
                """
                return platform.system()
        class cpu:
            def cpumodel():
                """Returns the model name of the CPU.
                Example:
                >>> cpumodel()
                Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz
                """
                try:
                    return wmi.WMI().Win32_Processor()[0].Name
                except:
                    return 'No CPU found.'
            def cpuusage():
                """Returns the current CPU usage as a percentage.
                Example:
                >>> cpuusage()
                4.2
                """
                try:
                    return psutil.cpu_percent()
                except:
                    return 'No CPU found.'
        class gpu():
            def gpumodel():
                """Returns the model name of the GPU.
                Example:
                >>> gpumodel()
                NVIDIA GeForce MX130
                """
                try:
                    return GPUtil.getGPUs()[0].name
                except:
                    return 'No GPU found.'
            def gpuusage():
                """Returns the current GPU usage as a percentage.
                Example:
                >>> gpuusage()
                4.2
                """
                try:
                    return GPUtil.getGPUs()[0].load*100
                except:
                    return 'No GPU found.'
        class storage():
            def __init__(self):
                self.total, self.used, self.free = shutil.disk_usage('/')
            def storagetotal(self, bytes=None):
                """Returns the total storage space in GB.
                If the bytes parameter is True, returns the total storage space in bytes.
                Example:
                >>> storagetotal()
                100.0
                >>> storagetotal(bytes)
                1000000000000
                """
                if bytes:
                    return self.total
                else:
                    return f'{self.total // (2 ** 30)} GB'
            def storageused(self, bytes=None):
                """Returns the used storage space in GB.
                If the bytes parameter is True, returns the used storage space in bytes.
                Example:
                >>> storageused()
                50.0
                >>> storageused(bytes)
                500000000000
                """
                if bytes:
                    return self.used
                else:
                    return f'{self.used // (2 ** 30)} GB'
            def storageleft(self, bytes=None):
                """Returns the free storage space in GB.
                If the bytes parameter is True, returns the free storage space in bytes.
                Example:
                >>> storageleft()
                50.0
                >>> storageleft(bytes)
                500000000000
                """
                if bytes:
                    return self.free
                else:
                    return f'{self.free // (2 ** 30)} GB'

def clear_lines(num_lines):
    """Clear the specified number of lines in the terminal."""
    for _ in range(num_lines):
        print("\033[A\033[K", end="")  # Move cursor up and clear line
    print("\033[A", end="")
    