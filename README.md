# F1 Championship Generator

[Русская версия](README.ru.md)

This is a console program that simulates a Formula 1 championship. I wrote it to practise Python and because I enjoy Formula 1.

It generates qualifying and race results, weather, driver mistakes, crashes and technical failures. You can view driver and constructor standings, season statistics and a race archive, or create your own driver.

Available seasons: **1999, 2007, 2010, 2012, 2021, 2023, 2024, 2025 and 2026**.

## Install and play on Windows

Use the Windows x64 release if you want to play without installing Python. No compiler, IDE or extra packages are needed.

1. Open **Releases** on the repository page and select version **v1.0**.
2. Under **Assets**, download `F1-Championship-Generator-v1.0-Windows-x64.zip`.
3. Extract the archive to a folder where you can save files, such as a folder in Documents. Do not run the program from inside the ZIP archive.
4. Open `F1-Championship-Generator.exe`.
5. Enter a menu option number and press Enter.

All nine seasons are included in the executable. There is no installer. To remove the program, delete its extracted folder after keeping any saves you want.

The **Source code (zip)** download contains Python source files. Choose the Windows x64 ZIP listed above for the ready-to-run program. If the release asset is not available yet, use the source instructions below.

## Using the program

The main menu has four options:

- **Generate Championship**: choose a season and simulate the championship.
- **Create Your Driver**: replace one driver in a team, then simulate the season.
- **Load Championship**: open a saved championship and its race archive.
- **Exit**: close the program.

For a custom driver, you can copy another driver's ratings or enter values from 0 to 100. After the season, you can view your statistics and compare your results with your teammate. The game menus are in English.

## Saves and updates

After a championship, enter a save name or press Enter to use the default name. Each save gets a new filename, so earlier championships are kept.

Saves are stored in `saves` next to the executable. When running the source, they are stored in `saves` next to `championship.py`. The folder is created automatically after the first championship. Older saves without a display name still work.

Before updating, close the program and copy the `saves` folder somewhere safe. Extract the new release into a new folder, then copy your `saves` folder next to the new executable. The same JSON saves can be used with the source version.

## Run from source

Install Python 3.9 or newer, download the repository ZIP and extract it. Keep `championship.py`, `season_loader.py` and the `seasons` folder together.

Open a terminal in the extracted project folder and run:

```text
python championship.py
```

On Windows, you can also use `py championship.py` if Python Launcher is installed. On Linux or macOS, the command may be `python3 championship.py`. The `.exe` release is for Windows only. No extra Python packages are required to run the source.

If the Python command is not found, check that Python is installed and available in your terminal. If the executable's window closes unexpectedly, open it from a terminal to read the error. If saves cannot be written, move the extracted program to a folder you can write to.

## Limits

Results are random and do not recreate the real races. Driver ratings, track ratings, car performance and reliability are game estimates, not official measurements. Cars keep the same performance throughout a season.

Each team has two drivers for the whole championship. The six added historical presets use the drivers with the most appearances in their seats. There are no mid-season replacements, sprints, fastest-lap bonus points, half-points races or administrative penalties. McLaren can score constructor points in 2007. Michael Schumacher races the full 1999 season. The older 2023, 2025 and 2026 presets have been kept as supplied and have not been historically rebalanced for this release.

The model cannot match every team's reliability or reproduce unusual races exactly. Belgium 2021 is simulated as a normal race. The 2024 preset uses an average balance and does not reproduce changes in car performance during the year.

## Checks and building

These commands are for the source repository. Players using the executable do not need them.

Run the release checks:

```text
python -m unittest tests -v
```

Check the six added presets using the game's simulation functions:

```text
python balance.py --seasons 1000 --seed 42
```

To build the executable on Windows x64, install PyInstaller on the developer's computer and run these commands from the project folder:

```text
python -m pip install PyInstaller==6.22.3
python -m PyInstaller --noconfirm F1-Championship-Generator.spec
```

The executable is created in `dist`, with the season presets bundled inside. Python 3.14.5 and PyInstaller 6.22.3 were used for the checked release build. Users of that executable do not need Python.

See [RELEASE_REPORT.md](RELEASE_REPORT.md) for balance results, historical sources and known differences. `balance_results.json` contains the final sample results, `balance_history.json` records the balance runs, and `historical_reference.json` contains the reference statistics.
