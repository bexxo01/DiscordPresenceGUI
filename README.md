````markdown
# Discord Rich Presence GUI
  

**Version**: 0.2.0 (Work in Progress)

A small desktop application for creating and managing Discord Rich Presence profiles via a graphical interface. Built with Python 3.13, PySide6 (Qt for Python) and pypresence, it lets you define multiple “profiles” of presence data, start/stop updates, switch themes, and save/load your settings to JSON.

---

## Features

- **Multiple Profiles**: Create, copy, delete and switch between different presence configurations.  
- **Live Rich Presence**: Start and stop updating your Discord status with one click.  
- **Config Persistence**: Profiles and last-used settings are stored in `config.json`.  
- **Environment Variables**: Uses a `.env` file for sensitive data (`CLIENT_ID`, `DISCORD_TOKEN`).  
- **Light / Dark Theme**: Toggle between two color schemes.  
- **Work in Progress**: The code is under active development; some UI bindings or code paths may still contain bugs.
- If you want a more stable version you should use **Version**: 0.1.0 (still using old GUI)
- Also please note that this is actually only my second project and I still need to learn alot^^

---

## Installation

1. **Clone the repository**  
   bash
   git clone https://github.com/<your-username>/discord-presence-gui.git
   cd discord-presence-gui
````

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install pypresence python-dotenv PySide6
   ```

---

## Configuration

1. **Create a `.env` file** in the project root:

   ```
   CLIENT_ID=your_discord_application_client_id
   DISCORD_TOKEN=your_bot_token_if_needed
   ```

2. Ensure `.env` is listed in `.gitignore` (already provided).

3. **Optionally** edit the default `config.json` or let the app generate it when you first save a profile.

---

## Usage

```bash
python presence_app.py
```

1. **New Profile**: Click “New” and give it a name.
2. **Edit Fields**: Fill in Client ID (or leave blank to use `CLIENT_ID` from `.env`), State, Details, Image keys, etc.
3. **Save Profile**: Click “Save Profile” to persist settings.
4. **Start / Stop**: Use ▶ Start and ■ Stop to control your Rich Presence.
5. **Theme**: Toggle between Light and Dark mode with the “Dark Mode” / “Light Mode” button.

---

## Building a Standalone Executable

If you want to distribute a single `.exe`:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed \
  --add-data ".env;." \
  --add-data "config.json;." \
  presence_app.py
```
or

```
pyinstaller --onefile --windowed --add-data ".env;." --add-data "config.json;." presence_app.py

```

Resulting binary will appear in `dist/presence_app.exe`.

---

## Known Issues & Roadmap

* **UI Bindings**: After editing `main.ui`, you must re-run `pyside6-uic main.ui -o ui_main.py` or restart if using the dynamic loader.
* **Error Handling**: Some RPC errors may not display correctly in the GUI.
* **Profile Validation**: Currently only client ID, state/details are validated; image keys and buttons may fail silently.
* **Animations**: No built-in animations yet.
* **Future Ideas**:

  * Drag-and-drop image picker
  * Scheduler / Timers
  * Advanced theme customization

---

## Contributing

Feel free to open issues or pull requests! This project is a work in progress—any help improving stability, fixing bugs, or adding features is welcome.

---

## Disclaimer:
README was written by AI cause i'm lazy :)

## License

Distributed under the [MIT License](LICENSE).

```
```
