🛡️ #Cyber Port Scanner - Smooth Edition

A lightweight, multi-threaded TCP port scanner with a sleek, dark-themed graphical user interface built with Python and Tkinter. 🚀

✨ Features

🔹 Simple 3-field interface: enter a target host, start port, and end port.
⚡ Multi-threaded scanning: dynamically scales up to 50 concurrent threads for fast, non-blocking execution.
🎯 Quick Range Presets: one-click buttons to instantly set ranges for Top 100, Top 1024, Web Ports, and Full (1-65535) scans.
⏱️ Real-time progress: live progress bar, percentage counter, and integrated digital clock update seamlessly during a scan.
🛑 Stop & Clear controls: cancel a running scan gracefully at any time or clear the output window for a fresh scan.
💾 Save results: export discovered open ports and full scan logs to a timestamped .txt file.
💻 Cross-platform: runs smoothly on Windows, macOS, and Linux.

🛠️ Requirements

🐍 Python 3.x or newer
🪟 Tkinter (included in the standard Python distribution; on Debian/Ubuntu, install python3-tk)
📦 No third-party packages are required.

📥 Installation

1️⃣ Open your terminal or command prompt.
2️⃣ Download or extract the project folder to your local machine.
3️⃣ Navigate into the project folder using the "cd" command.

🚀 Usage

Run the application by typing: python port_scanner.py

🎯 Enter the Target IP / Host (e.g., 127.0.0.1 or localhost).

🔢 Set the Start Port and End Port (defaults to 1 - 1024), or click one of the Quick Range buttons.

▶️ Click Start Scan. Open ports will appear in real-time in the Scan Output pane.

⏹️ Click Stop to cancel a scan early, or 🧹 Clear to wipe the log.

📝 After a scan completes, click Save Results to write the security log to a text file.

📁 Project Structure

cyber-port-scanner/
📄 port_scanner.py (Main application containing the scanner logic and Tkinter GUI)
📖 README.md (Project documentation)

⚠️ Disclaimer

Use this tool only on hosts and networks you own or have explicit permission to scan. Unauthorized port scanning may be illegal in your jurisdiction. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.
