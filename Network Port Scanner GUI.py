import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import socket
import threading
from queue import Queue, Empty
from datetime import datetime

APP_BG = '#0d1117'
PANEL_BG = '#161b22'
ENTRY_BG = '#0f141a'
TEXT_BG = '#0b1220'
BORDER = '#30363d'
FG = '#e6edf3'
MUTED = '#8b949e'
ACCENT = '#58a6ff'
GREEN = '#3fb950'
YELLOW = '#d29922'
RED = '#f85149'
CYAN = '#39c5cf'

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Cyber Port Scanner - Smooth Edition')
        self.root.geometry('980x700')
        self.root.minsize(900, 620)
        self.root.configure(bg=APP_BG)

        self.scanning = False
        self.queue = Queue()
        self.open_ports = []
        self.total_ports = 0
        self.checked_ports = 0
        self.target_host = ''
        self.start_port = 1
        self.end_port = 1024
        self.worker_threads = []
        self.port_queue = Queue()
        self.start_time = None

        self.setup_style()
        self.build_ui()
        self.update_clock()
        self.process_queue()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass

        style.configure('TLabel', background=APP_BG, foreground=FG, font=('Segoe UI', 10))
        style.configure('Title.TLabel', background=APP_BG, foreground=CYAN, font=('Segoe UI', 20, 'bold'))
        style.configure('Sub.TLabel', background=APP_BG, foreground=MUTED, font=('Consolas', 10))
        style.configure('Panel.TLabelframe', background=PANEL_BG, foreground=ACCENT)
        style.configure('Panel.TLabelframe.Label', background=PANEL_BG, foreground=ACCENT, font=('Segoe UI', 10, 'bold'))
        style.configure('Cyber.TButton', font=('Segoe UI', 10, 'bold'), padding=8)
        style.map('Cyber.TButton', background=[('active', '#2f81f7')])
        style.configure('TEntry', fieldbackground=ENTRY_BG, foreground=FG, bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER, insertcolor=FG)
        style.configure('TProgressbar', troughcolor=ENTRY_BG, background=GREEN, bordercolor=BORDER, lightcolor=GREEN, darkcolor=GREEN)

    def build_ui(self):
        header = tk.Frame(self.root, bg=APP_BG)
        header.pack(fill='x', padx=14, pady=(12, 6))

        left = tk.Frame(header, bg=APP_BG)
        left.pack(side='left', fill='x', expand=True)
        ttk.Label(left, text='CYBER PORT SCANNER', style='Title.TLabel').pack(anchor='w')
        ttk.Label(left, text='Lightweight tkinter version for smooth Python IDLE execution', style='Sub.TLabel').pack(anchor='w', pady=(2, 0))

        right = tk.Frame(header, bg=APP_BG)
        right.pack(side='right')
        self.clock_label = tk.Label(right, text='', bg=APP_BG, fg=GREEN, font=('Consolas', 11, 'bold'))
        self.clock_label.pack(anchor='e')

        controls = tk.LabelFrame(self.root, text=' Scan Controls ', bg=PANEL_BG, fg=ACCENT, bd=1, relief='solid', font=('Segoe UI', 10, 'bold'))
        controls.pack(fill='x', padx=14, pady=8)

        row1 = tk.Frame(controls, bg=PANEL_BG)
        row1.pack(fill='x', padx=12, pady=(12, 8))

        tk.Label(row1, text='Target IP / Host:', bg=PANEL_BG, fg=FG, font=('Segoe UI', 10, 'bold')).pack(side='left')
        self.target_entry = tk.Entry(row1, bg=ENTRY_BG, fg=FG, insertbackground=FG, relief='flat', width=28, font=('Consolas', 11))
        self.target_entry.pack(side='left', padx=(10, 16), ipady=6)
        self.target_entry.insert(0, '127.0.0.1')

        tk.Label(row1, text='Start Port:', bg=PANEL_BG, fg=FG, font=('Segoe UI', 10, 'bold')).pack(side='left')
        self.start_entry = tk.Entry(row1, bg=ENTRY_BG, fg=FG, insertbackground=FG, relief='flat', width=8, font=('Consolas', 11))
        self.start_entry.pack(side='left', padx=(8, 16), ipady=6)
        self.start_entry.insert(0, '1')

        tk.Label(row1, text='End Port:', bg=PANEL_BG, fg=FG, font=('Segoe UI', 10, 'bold')).pack(side='left')
        self.end_entry = tk.Entry(row1, bg=ENTRY_BG, fg=FG, insertbackground=FG, relief='flat', width=8, font=('Consolas', 11))
        self.end_entry.pack(side='left', padx=(8, 0), ipady=6)
        self.end_entry.insert(0, '1024')

        row2 = tk.Frame(controls, bg=PANEL_BG)
        row2.pack(fill='x', padx=12, pady=(0, 12))

        self.start_btn = ttk.Button(row2, text='Start Scan', style='Cyber.TButton', command=self.start_scan)
        self.start_btn.pack(side='left', padx=(0, 8))

        self.stop_btn = ttk.Button(row2, text='Stop', style='Cyber.TButton', command=self.stop_scan)
        self.stop_btn.pack(side='left', padx=(0, 8))

        self.clear_btn = ttk.Button(row2, text='Clear', style='Cyber.TButton', command=self.clear_output)
        self.clear_btn.pack(side='left', padx=(0, 8))

        self.save_btn = ttk.Button(row2, text='Save Results', style='Cyber.TButton', command=self.save_results)
        self.save_btn.pack(side='left', padx=(0, 20))

        tk.Label(row2, text='Quick Range:', bg=PANEL_BG, fg=MUTED, font=('Segoe UI', 10, 'bold')).pack(side='left')

        presets = [
            ('Top 100', 1, 100),
            ('Top 1024', 1, 1024),
            ('Web Ports', 20, 100),
            ('Full 1-65535', 1, 65535),
        ]
        for text, start, end in presets:
            tk.Button(row2, text=text, command=lambda s=start, e=end: self.set_range(s, e),
                      bg=ENTRY_BG, fg=CYAN, activebackground='#1f2937', activeforeground=FG,
                      relief='flat', bd=0, padx=10, pady=6, font=('Segoe UI', 9, 'bold')).pack(side='left', padx=4)

        status = tk.Frame(self.root, bg=PANEL_BG, bd=1, relief='solid')
        status.pack(fill='x', padx=14, pady=8)

        top_status = tk.Frame(status, bg=PANEL_BG)
        top_status.pack(fill='x', padx=12, pady=(10, 6))
        self.status_label = tk.Label(top_status, text='Ready', bg=PANEL_BG, fg=YELLOW, font=('Segoe UI', 10, 'bold'))
        self.status_label.pack(side='left')
        self.progress_text = tk.Label(top_status, text='0/0 (0%)', bg=PANEL_BG, fg=MUTED, font=('Consolas', 10))
        self.progress_text.pack(side='right')

        self.progress = ttk.Progressbar(status, mode='determinate')
        self.progress.pack(fill='x', padx=12, pady=(0, 10))

        output_frame = tk.LabelFrame(self.root, text=' Scan Output ', bg=PANEL_BG, fg=ACCENT, bd=1, relief='solid', font=('Segoe UI', 10, 'bold'))
        output_frame.pack(fill='both', expand=True, padx=14, pady=(8, 14))

        self.output = scrolledtext.ScrolledText(output_frame, bg=TEXT_BG, fg=FG, insertbackground=FG,
                                                relief='flat', wrap='word', font=('Consolas', 10))
        self.output.pack(fill='both', expand=True, padx=12, pady=12)
        self.output.tag_config('header', foreground=CYAN, font=('Consolas', 11, 'bold'))
        self.output.tag_config('open', foreground=GREEN, font=('Consolas', 10, 'bold'))
        self.output.tag_config('warn', foreground=YELLOW)
        self.output.tag_config('error', foreground=RED, font=('Consolas', 10, 'bold'))
        self.output.tag_config('muted', foreground=MUTED)
        self.output.tag_config('good', foreground=GREEN)

        self.log('Cyber Port Scanner ready. Enter a target and click Start Scan.\n', 'header')

    def update_clock(self):
        self.clock_label.config(text=datetime.now().strftime('%d-%m-%Y  %H:%M:%S'))
        self.root.after(1000, self.update_clock)

    def set_range(self, start, end):
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, str(start))
        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, str(end))

    def log(self, message, tag=None):
        self.output.insert(tk.END, message, tag)
        self.output.see(tk.END)

    def clear_output(self):
        self.output.delete('1.0', tk.END)
        self.open_ports.clear()
        self.log('Output cleared.\n', 'muted')

    def validate_inputs(self):
        target = self.target_entry.get().strip()
        if not target:
            messagebox.showerror('Input Error', 'Please enter target IP or hostname.')
            return None
        try:
            start_port = int(self.start_entry.get().strip())
            end_port = int(self.end_entry.get().strip())
        except ValueError:
            messagebox.showerror('Input Error', 'Ports must be valid numbers.')
            return None
        if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
            messagebox.showerror('Input Error', 'Port range must be between 1 and 65535.')
            return None
        if start_port > end_port:
            messagebox.showerror('Input Error', 'Start port must be less than or equal to end port.')
            return None
        return target, start_port, end_port

    def start_scan(self):
        if self.scanning:
            messagebox.showwarning('Scan Running', 'A scan is already running.')
            return

        validated = self.validate_inputs()
        if not validated:
            return

        self.target_host, self.start_port, self.end_port = validated
        self.scanning = True
        self.open_ports = []
        self.checked_ports = 0
        self.total_ports = self.end_port - self.start_port + 1
        self.progress['maximum'] = self.total_ports
        self.progress['value'] = 0
        self.start_time = datetime.now()

        while not self.port_queue.empty():
            try:
                self.port_queue.get_nowait()
            except Empty:
                break
        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except Empty:
                break

        for port in range(self.start_port, self.end_port + 1):
            self.port_queue.put(port)

        self.status_label.config(text=f'Scanning {self.target_host}...', fg=CYAN)
        self.log('\n' + '=' * 70 + '\n', 'muted')
        self.log(f'Starting scan on {self.target_host} | Ports {self.start_port}-{self.end_port}\n', 'header')
        self.log(f'Start time: {self.start_time.strftime("%H:%M:%S")}\n', 'muted')

        thread_count = 50 if self.total_ports >= 200 else 20
        self.worker_threads = []
        for _ in range(thread_count):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()
            self.worker_threads.append(t)

    def stop_scan(self):
        if not self.scanning:
            self.status_label.config(text='Ready', fg=YELLOW)
            return
        self.scanning = False
        self.status_label.config(text='Stopping scan...', fg=YELLOW)
        self.log('Stopping scan...\n', 'warn')

    def worker(self):
        while self.scanning:
            try:
                port = self.port_queue.get_nowait()
            except Empty:
                break

            result = self.scan_port(self.target_host, port)
            self.queue.put(('port_done', port, result))
            self.port_queue.task_done()

    def scan_port(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.35)
        try:
            result = sock.connect_ex((host, port))
            return result == 0
        except socket.gaierror:
            return 'invalid_host'
        except Exception:
            return False
        finally:
            sock.close()

    def process_queue(self):
        try:
            while True:
                item = self.queue.get_nowait()
                if item[0] == 'port_done':
                    _, port, result = item
                    if result == 'invalid_host':
                        self.scanning = False
                        self.status_label.config(text='Invalid hostname or IP address', fg=RED)
                        self.log('Invalid hostname or IP address.\n', 'error')
                    else:
                        self.checked_ports += 1
                        self.progress['value'] = self.checked_ports
                        percent = int((self.checked_ports / self.total_ports) * 100) if self.total_ports else 0
                        self.progress_text.config(text=f'{self.checked_ports}/{self.total_ports} ({percent}%)')
                        if result is True:
                            self.open_ports.append(port)
                            self.log(f'[OPEN] Port {port}\n', 'open')

                self.queue.task_done()
        except Empty:
            pass

        if self.scanning:
            alive = any(t.is_alive() for t in self.worker_threads)
            if self.checked_ports >= self.total_ports or not alive:
                self.finish_scan(completed=self.checked_ports >= self.total_ports)

        self.root.after(80, self.process_queue)

    def finish_scan(self, completed=True):
        self.scanning = False
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        self.open_ports.sort()
        self.progress['value'] = self.checked_ports
        percent = int((self.checked_ports / self.total_ports) * 100) if self.total_ports else 0
        self.progress_text.config(text=f'{self.checked_ports}/{self.total_ports} ({percent}%)')

        if completed:
            self.status_label.config(text=f'Scan complete - {len(self.open_ports)} open port(s)', fg=GREEN)
            self.log('-' * 70 + '\n', 'muted')
            self.log(f'Scan completed in {elapsed:.2f} seconds\n', 'good')
            self.log(f'Open ports found: {len(self.open_ports)}\n', 'good')
            if self.open_ports:
                self.log('Ports: ' + ', '.join(map(str, self.open_ports)) + '\n', 'open')
            else:
                self.log('No open ports found in the selected range.\n', 'warn')
        else:
            self.status_label.config(text='Scan stopped', fg=YELLOW)
            self.log('-' * 70 + '\n', 'muted')
            self.log(f'Scan stopped after {elapsed:.2f} seconds\n', 'warn')
            self.log(f'Checked {self.checked_ports} ports, found {len(self.open_ports)} open\n', 'warn')

    def save_results(self):
        content = self.output.get('1.0', tk.END).strip()
        if not content:
            messagebox.showwarning('No Data', 'There are no scan results to save.')
            return

        default_name = f'scan_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                                 initialfile=default_name,
                                                 filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('CYBER PORT SCANNER RESULTS\n')
                f.write('=' * 70 + '\n')
                f.write(f'Target: {self.target_host}\n')
                f.write(f'Port Range: {self.start_port}-{self.end_port}\n')
                f.write(f'Saved: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
                f.write(f'Open Ports: {", ".join(map(str, self.open_ports)) if self.open_ports else "None"}\n')
                f.write('=' * 70 + '\n\n')
                f.write(content + '\n')
            messagebox.showinfo('Saved', 'Results saved successfully.')
        except Exception as e:
            messagebox.showerror('Save Error', f'Could not save file:\n{e}')


def main():
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
