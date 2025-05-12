#!/usr/bin/env python3
import sys, os, time, threading, json
from dotenv import load_dotenv
from PySide6 import QtWidgets
from ui_main import Ui_MainWindow
from pypresence import Presence

# Load environment variables
load_dotenv()
DEFAULT_CLIENT_ID = os.getenv("CLIENT_ID")
CONFIG_FILE = "config.json"
__version__ = "0.1.0"

# Theme definitions
themes = {
    "light": {"bg": "#f0f0f0", "fg": "#000000", "entry_bg": "#ffffff"},
    "dark":  {"bg": "#2e2e2e", "fg": "#ffffff", "entry_bg": "#4a4a4a"}
}

class RPCThread(threading.Thread):
    def __init__(self, client_id, data, interval, error_callback):
        super().__init__(daemon=True)
        self.client_id = client_id
        self.data = data
        self.interval = interval
        self.error_callback = error_callback
        self.running = False
        self.rpc = None

    def run(self):
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            while self.running:
                try:
                    self.rpc.update(**self.data)
                except Exception as e:
                    self.error_callback(f"Error updating presence: {e}")
                    break
                time.sleep(self.interval)
            if self.rpc:
                self.rpc.clear()
        except Exception as e:
            self.error_callback(f"Connection error: {e}")
        finally:
            if self.rpc:
                self.rpc.close()

    def start_presence(self):
        self.running = True
        if not self.is_alive():
            self.start()

    def stop_presence(self):
        self.running = False

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Internal state
        self.rpc_thread = None
        self.profiles = {}
        self.current_theme = "light"
        self.apply_theme()

        # Connect signals
        self.ui.newProfileButton.clicked.connect(self.new_profile)
        self.ui.copyProfileButton.clicked.connect(self.copy_profile)
        self.ui.deleteProfileButton.clicked.connect(self.delete_profile)
        self.ui.saveProfileButton.clicked.connect(self.save_profile)
        self.ui.startButton.clicked.connect(self.on_start)
        self.ui.stopButton.clicked.connect(self.on_stop)
        self.ui.themeButton.clicked.connect(self.toggle_theme)
        self.ui.exitButton.clicked.connect(self.close)

        # Load saved config
        self.load_config()

    def apply_theme(self):
        t = themes[self.current_theme]
        # Set background and text color
        self.ui.centralwidget.setStyleSheet(f"background:{t['bg']}; color:{t['fg']};")
        # Style entries
        entry_style = f"background:{t['entry_bg']}; color:{t['fg']};"
        for widget in [
            self.ui.clientIdEdit, self.ui.stateEdit, self.ui.detailsEdit,
            self.ui.largeImageEdit, self.ui.largeTextEdit,
            self.ui.smallImageEdit, self.ui.smallTextEdit
        ]:
            widget.setStyleSheet(entry_style)
        # Update theme button text
        self.ui.themeButton.setText("Dark Mode" if self.current_theme == "light" else "Light Mode")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def new_profile(self):
        name, ok = QtWidgets.QInputDialog.getText(self, "New Profile", "Enter profile name:")
        if ok and name:
            if name in self.profiles:
                QtWidgets.QMessageBox.warning(self, "Error", "Profile already exists.")
            else:
                self.profiles[name] = {"client_id":"", "presence_data":{}, "update_interval":15}
                self.ui.profileComboBox.addItem(name)
                self.ui.profileComboBox.setCurrentText(name)
                self.load_profile(name)

    def copy_profile(self):
        src = self.ui.profileComboBox.currentText()
        if not src: return
        name, ok = QtWidgets.QInputDialog.getText(self, "Copy Profile", f"Name for copy of '{src}':")
        if ok and name:
            if name in self.profiles:
                QtWidgets.QMessageBox.warning(self, "Error", "Profile already exists.")
            else:
                cfg = self.profiles[src]
                self.profiles[name] = {
                    "client_id": cfg["client_id"],
                    "presence_data": dict(cfg["presence_data"]),
                    "update_interval": cfg["update_interval"]
                }
                self.ui.profileComboBox.addItem(name)
                self.ui.profileComboBox.setCurrentText(name)
                self.load_profile(name)

    def delete_profile(self):
        name = self.ui.profileComboBox.currentText()
        if not name: return
        if QtWidgets.QMessageBox.question(self, "Delete", f"Delete profile '{name}'?") == QtWidgets.QMessageBox.Yes:
            self.profiles.pop(name, None)
            idx = self.ui.profileComboBox.currentIndex()
            self.ui.profileComboBox.removeItem(idx)
            if self.profiles:
                first = next(iter(self.profiles))
                self.ui.profileComboBox.setCurrentText(first)
                self.load_profile(first)

    def load_profile(self, name):
        cfg = self.profiles[name]
        self.ui.clientIdEdit.setText(cfg.get("client_id", ""))
        pd = cfg.get("presence_data", {})
        self.ui.stateEdit.setText(pd.get("state", ""))
        self.ui.detailsEdit.setText(pd.get("details", ""))
        self.ui.largeImageEdit.setText(pd.get("large_image", ""))
        self.ui.largeTextEdit.setText(pd.get("large_text", ""))
        self.ui.smallImageEdit.setText(pd.get("small_image", ""))
        self.ui.smallTextEdit.setText(pd.get("small_text", ""))
        self.ui.intervalSpinBox.setValue(cfg.get("update_interval", 15))

    def save_profile(self):
        name = self.ui.profileComboBox.currentText()
        cid = self.ui.clientIdEdit.text().strip() or DEFAULT_CLIENT_ID
        data = {}
        for key, widget in [
            ("state", self.ui.stateEdit), ("details", self.ui.detailsEdit),
            ("large_image", self.ui.largeImageEdit), ("large_text", self.ui.largeTextEdit),
            ("small_image", self.ui.smallImageEdit), ("small_text", self.ui.smallTextEdit)
        ]:
            v = widget.text().strip()
            if v: data[key] = v
        data["start"] = int(time.time())
        interval = self.ui.intervalSpinBox.value()
        self.profiles[name] = {"client_id": cid, "presence_data": data, "update_interval": interval}
        with open(CONFIG_FILE, "w") as f:
            json.dump({"profiles": self.profiles, "last": name}, f, indent=4)
        QtWidgets.QMessageBox.information(self, "Saved", "Profile saved.")
        if self.rpc_thread and self.rpc_thread.running:
            self.rpc_thread.data = data

    def load_config(self):
        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
            self.profiles = cfg.get("profiles", {})
            for name in self.profiles:
                self.ui.profileComboBox.addItem(name)
            last = cfg.get("last")
            if last in self.profiles:
                self.ui.profileComboBox.setCurrentText(last)
                self.load_profile(last)

    def on_start(self):
        if self.rpc_thread and self.rpc_thread.running:
            return
        name = self.ui.profileComboBox.currentText()
        cid = self.ui.clientIdEdit.text().strip() or DEFAULT_CLIENT_ID
        data = {}
        for key, widget in [("state", self.ui.stateEdit), ("details", self.ui.detailsEdit)]:
            v = widget.text().strip()
            if v: data[key] = v
        data["start"] = int(time.time())
        interval = self.ui.intervalSpinBox.value()
        self.rpc_thread = RPCThread(cid, data, interval, self.show_error)
        self.rpc_thread.start_presence()
        self.ui.statusLabel.setText("Running")
        self.ui.startButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)

    def on_stop(self):
        if self.rpc_thread:
            self.rpc_thread.stop_presence()
        self.ui.statusLabel.setText("Stopped")
        self.ui.startButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)

    def show_error(self, msg):
        QtWidgets.QMessageBox.critical(self, "RPC Error", msg)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

