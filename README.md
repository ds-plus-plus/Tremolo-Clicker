# Tremolo-Clicker
Created in early 2022 as a personal passion project, Tremolo Clicker is a thread-safe, randomised auto clicker. It was developed with the intent of generating humanised delays between inputs, utilising a custom algorithm to bypass heuristic detection.

## Tech Stack
**Language:** Python 3.x
**GUI Framework:** PyQt6
**OS Interfacing:** `pywin32` (win32api, win32con)

## Installation 
1. Clone the repository:
```bash
git clone https://github.com/ds-plus-plus/Tremolo-Clicker.git
```

2. Install the required dependencies:
```bash
pip install PyQt6 pywin32
```

3. Run the `main.py` script
```bash
python main.py
```

## Usage
- Adjust the Minimum and Maximum CPS sliders to define the target frequency boundary.
- Enable Simulate Random Pauses to introduce occasional, longer delays simulating physical fatigue.
- Toggle the script on and off globally using the DEL key.
- Hold Mouse Button 5 (Forward Side Button) while the script is active to trigger the input loop.

## Future Enhancements 
While this was originally a small passion project, the architecture was built to support future expansions. 

Planned features include: 
- **Customisable Keybinds:** Migrating the trigger key from a hardcoded hardware call (Mouse Button 5) to a user-defined input dynamically loaded from `config.json`.
- **Cross-Platform Linux Support:** initially targeting X11 display servers (via `xdotool` or `python-uinput`). Wayland support will be more difficult due to Wayland's strict security model regarding simulated inputs, however, I still intend on implementing Wayland support in the future.
