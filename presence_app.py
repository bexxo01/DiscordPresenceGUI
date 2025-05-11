#!/usr/bin/env python3
import threading
import time
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pypresence import Presence
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID     = os.getenv("CLIENT_ID")

CONFIG_FILE = "config.json"
__version__ = "0.1.0"


themes = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "entry_bg": "#ffffff"
    },
    "dark": {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "entry_bg": "#4a4a4a"
    }
}


class RPCThread(threading.Thread):
    def __init__(self, client_id, presence_data, update_interval, error_callback):
        super().__init__(daemon=True)
        self.client_id = client_id
        self.presence_data = presence_data
        self.update_interval = update_interval
        self.rpc = None
        self.running = False
        self.error_callback = error_callback

    def run(self):
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            while self.running:
                try:
                    self.rpc.update(**self.presence_data)
                except Exception as e:
                    self.error_callback(f"Error updating presence: {e}")
                    break
                time.sleep(self.update_interval)
            if self.rpc:
                self.rpc.clear()
        except Exception as e:
            self.error_callback(f"Error connecting to Discord: {e}")
        finally:
            if self.rpc:
                self.rpc.close()

    def start_presence(self):
        self.running = True
        if not self.is_alive():
            self.start()

    def stop_presence(self):
        self.running = False


class PresenceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Discord Rich Presence Controller")
        self.configure(padx=10, pady=10)
        self.rpc_thread = None
        self.profiles = {}
        self.current_profile = None
        self.current_theme = "light"

        # Styling
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.apply_theme(self.current_theme)

        # Build UI
        self.build_profile_ui()
        self.build_config_ui()
        self.build_control_ui()

        # Load saved profiles/config
        self.load_config()

        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def apply_theme(self, name):
        t = themes[name]
        self.configure(bg=t['bg'])
        self.style.configure('.', background=t['bg'], foreground=t['fg'])
        self.style.configure('TEntry', fieldbackground=t['entry_bg'], foreground=t['fg'])
        self.option_add('*Background', t['bg'])
        self.option_add('*Foreground', t['fg'])
        self.option_add('*Entry.Background', t['entry_bg'])
        self.option_add('*Entry.Foreground', t['fg'])

    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme(self.current_theme)
        btn_text = 'Light Mode' if self.current_theme == 'dark' else 'Dark Mode'
        self.theme_btn.config(text=btn_text)

    def build_profile_ui(self):
        prof_frame = ttk.LabelFrame(self, text="Profiles", padding=5)
        prof_frame.grid(row=0, column=0, sticky="ew", pady=(0,10))
        self.profile_var = tk.StringVar()
        self.profile_cb = ttk.Combobox(prof_frame, textvariable=self.profile_var,
                                       state="readonly", width=30)
        self.profile_cb.grid(row=0, column=0, padx=5)
        self.profile_cb.bind("<<ComboboxSelected>>", lambda e: self.on_profile_select())
        ttk.Button(prof_frame, text="New", command=self.new_profile).grid(row=0, column=1, padx=2)
        ttk.Button(prof_frame, text="Copy", command=self.copy_profile).grid(row=0, column=2, padx=2)
        ttk.Button(prof_frame, text="Delete", command=self.delete_profile).grid(row=0, column=3, padx=2)

    def new_profile(self):
        name = simpledialog.askstring("New Profile", "Enter new profile name:")
        if name:
            if name in self.profiles:
                messagebox.showerror("Error", "Profile already exists.")
            else:
                self.profiles[name] = {
                    "client_id": "",
                    "presence_data": {},
                    "update_interval": 15
                }
                self.refresh_profiles()
                self.profile_var.set(name)
                self.load_profile(name)

    def copy_profile(self):
        src = self.profile_var.get()
        if not src:
            return
        name = simpledialog.askstring("Copy Profile", f"Enter name for copy of '{src}':")
        if name:
            if name in self.profiles:
                messagebox.showerror("Error", "Profile already exists.")
            else:
                cfg = self.profiles[src]
                # deep copy
                self.profiles[name] = {
                    "client_id": cfg["client_id"],
                    "presence_data": dict(cfg["presence_data"]),
                    "update_interval": cfg["update_interval"]
                }
                self.refresh_profiles()
                self.profile_var.set(name)
                self.load_profile(name)

    def delete_profile(self):
        name = self.profile_var.get()
        if not name:
            return
        if messagebox.askyesno("Delete", f"Delete profile '{name}'?"):
            del self.profiles[name]
            self.refresh_profiles()
            if self.profiles:
                new = next(iter(self.profiles))
                self.profile_var.set(new)
                self.load_profile(new)
            else:
                self.current_profile = None
                self.clear_fields()

    def refresh_profiles(self):
        names = list(self.profiles.keys())
        self.profile_cb['values'] = names

    def on_profile_select(self):
        name = self.profile_var.get()
        if name:
            self.load_profile(name)

    def load_profile(self, name):
        self.current_profile = name
        cfg = self.profiles.get(name, {})
        self.client_id_var.set(cfg.get("client_id", ""))
        pdata = cfg.get("presence_data", {})
        self.state_var.set(pdata.get("state", ""))
        self.details_var.set(pdata.get("details", ""))
        self.large_image_var.set(pdata.get("large_image", ""))
        self.large_text_var.set(pdata.get("large_text", ""))
        self.small_image_var.set(pdata.get("small_image", ""))
        self.small_text_var.set(pdata.get("small_text", ""))
        for i, (lbl_var, url_var) in enumerate(self.btn_vars):
            btns = pdata.get("buttons", [])
            if i < len(btns):
                lbl_var.set(btns[i]["label"])
                url_var.set(btns[i]["url"])
            else:
                lbl_var.set("")
                url_var.set("")
        self.interval_var.set(cfg.get("update_interval", 15))

    def clear_fields(self):
        for var in [self.client_id_var, self.state_var, self.details_var,
                    self.large_image_var, self.large_text_var,
                    self.small_image_var, self.small_text_var]:
            var.set("")
        for lbl_var, url_var in self.btn_vars:
            lbl_var.set("")
            url_var.set("")
        self.interval_var.set(15)

    def build_config_ui(self):
        cfg = ttk.LabelFrame(self, text="Configuration", padding=10)
        cfg.grid(row=1, column=0, sticky="ew")
        labels = [
            ("Client ID *", 'client_id_var'),
            ("State", 'state_var'),
            ("Details", 'details_var'),
            ("Large Image Key", 'large_image_var'),
            ("Large Text", 'large_text_var'),
            ("Small Image Key", 'small_image_var'),
            ("Small Text", 'small_text_var'),
        ]
        for i, (text, varname) in enumerate(labels):
            ttk.Label(cfg, text=text+":").grid(row=i, column=0, sticky="w", pady=2)
            setattr(self, varname, tk.StringVar())
            ttk.Entry(cfg, textvariable=getattr(self, varname), width=40).grid(
                row=i, column=1, pady=2)

        btn_frame = ttk.LabelFrame(cfg, text="Buttons (max 2)", padding=5)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky="ew")
        self.btn_vars = []
        for i in range(2):
            lbl_var = tk.StringVar()
            url_var = tk.StringVar()
            self.btn_vars.append((lbl_var, url_var))
            ttk.Entry(btn_frame, textvariable=lbl_var, width=15).grid(row=i, column=0, padx=5)
            ttk.Entry(btn_frame, textvariable=url_var, width=30).grid(row=i, column=1, padx=5)

        ttk.Label(cfg, text="Update Interval (s):").grid(
            row=len(labels)+1, column=0, sticky="w")
        self.interval_var = tk.IntVar(value=15)
        ttk.Spinbox(cfg, from_=5, to=3600, textvariable=self.interval_var,
                    width=5).grid(row=len(labels)+1, column=1, sticky="w")
        ttk.Button(cfg, text="Save profile", command=self.save_config).grid(
            row=len(labels)+2, column=0, columnspan=2, pady=10)

    def build_control_ui(self):
        ctl = ttk.Frame(self, padding=10)
        ctl.grid(row=2, column=0, sticky="ew")
        ttk.Label(ctl, text="Status:").grid(row=0, column=0, sticky="w")
        self.status_var = tk.StringVar(value="Stopped")
        ttk.Label(ctl, textvariable=self.status_var,
                  font=("Arial",12,"bold")).grid(row=0,column=1,padx=(5,20))

        self.start_btn = ttk.Button(ctl, text="▶ Start", command=self.start_presence)
        self.start_btn.grid(row=0, column=2, padx=5)

        self.stop_btn = ttk.Button(ctl, text="■ Stop", command=self.stop_presence, state="disabled")
        self.stop_btn.grid(row=0, column=3, padx=5)

        self.theme_btn = ttk.Button(ctl, text="Dark Mode", command=self.toggle_theme)
        self.theme_btn.grid(row=0, column=4, padx=5)

        self.exit_btn = ttk.Button(ctl, text="✖ Exit", command=self.on_exit)
        self.exit_btn.grid(row=0, column=5, padx=5)

    def gather_config(self):
        client_id = self.client_id_var.get().strip()
        data = {}
        for key, var in [
            ("state", self.state_var),
            ("details", self.details_var),
            ("large_image", self.large_image_var),
            ("large_text", self.large_text_var),
            ("small_image", self.small_image_var),
            ("small_text", self.small_text_var),
        ]:
            val = var.get().strip()
            if val:
                data[key] = val
        data["start"] = int(time.time())
        buttons = []
        for lbl_var, url_var in self.btn_vars:
            lbl = lbl_var.get().strip()
            url = url_var.get().strip()
            if lbl and url:
                buttons.append({"label": lbl, "url": url})
        if buttons:
            data["buttons"] = buttons
        interval = self.interval_var.get()
        return client_id, data, interval

    def validate_config(self, client_id, data):
        if not client_id:
            messagebox.showerror("Error", "Client ID required.")
            return False
        if not data.get("state") and not data.get("details"):
            messagebox.showerror("Error", "Enter State or Details.")
            return False
        return True

    def start_presence(self):
        if self.rpc_thread and self.rpc_thread.running:
            self.show_error("Already running.")
            return
        name = self.profile_var.get()
        client_id, data, interval = self.gather_config()
        if not self.validate_config(client_id, data):
            return
        # Update in-memory profile
        self.profiles[name] = {
            "client_id": client_id,
            "presence_data": data,
            "update_interval": interval
        }
        self.save_all_config()

        # Start thread
        self.rpc_thread = RPCThread(client_id, data, interval, self.show_error)
        self.rpc_thread.start_presence()
        self.status_var.set("Running")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

    def stop_presence(self):
        if self.rpc_thread:
            self.rpc_thread.stop_presence()
        self.status_var.set("Stopped")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def save_config(self):
        name = self.profile_var.get()
        client_id, data, interval = self.gather_config()
        self.profiles[name] = {
            "client_id": client_id,
            "presence_data": data,
            "update_interval": interval
        }
        self.save_all_config()
        messagebox.showinfo("Saved", "Profile saved.")
        # Dynamically update presence_data if running
        if self.rpc_thread and self.rpc_thread.running:
            self.rpc_thread.presence_data = data

    def save_all_config(self):
        data = {
            "profiles": self.profiles,
            "last_profile": self.profile_var.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_config(self):
        if os.path.isfile(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
            self.profiles = cfg.get("profiles", {})
            self.refresh_profiles()
            last = cfg.get("last_profile")
            if last in self.profiles:
                self.profile_var.set(last)
                self.load_profile(last)
            elif self.profiles:
                first = next(iter(self.profiles))
                self.profile_var.set(first)
                self.load_profile(first)

    def show_error(self, message):
        messagebox.showerror("RPC Error", message)

    def on_exit(self):
        if self.rpc_thread and self.rpc_thread.running:
            self.rpc_thread.stop_presence()
        self.destroy()


if __name__ == "__main__":
    app = PresenceApp()
    app.mainloop()

