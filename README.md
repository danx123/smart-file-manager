<div align="center">

# SmartFileManager

### Enterprise-Grade File Management for Power Users

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.5%2B-41CD52?style=flat-square&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-Proprietary-7C3AED?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-0EA5E9?style=flat-square)](https://github.com/danx123/smart-file-manager)
[![Version](https://img.shields.io/badge/Version-2.0.0-10B981?style=flat-square)](https://github.com/danx123/smart-file-manager/releases)

**[Overview](#-overview) · [Features](#-features) · [Installation](#-installation) · [Usage](#-usage) · [Smart Rename](#-smart-rename) · [Screenshots](#-screenshots) · [Contributing](#-contributing)**

---

*A professional, cross-platform desktop file manager with intelligent batch rename,  
docking panel system, activity logging, and persistent dark/light theme support.*

</div>

---

## 📋 Overview

**SmartFileManager** is a production-ready desktop application built with **Python** and **PySide6 (Qt6)**. Designed for developers, content creators, and power users who need precision control over their file system, it combines an intuitive docking interface with a powerful Smart Rename engine capable of multi-pattern batch operations, regex transformations, auto-numbering, and live preview — all without touching a command line.

Unlike traditional file managers, SmartFileManager applies its visual theme entirely through explicit QSS stylesheets and operates on Qt's Fusion base style, ensuring **zero conflict with the host operating system's theme engine** on Windows, macOS, and Linux alike.

> **Repository:** [github.com/danx123/smart-file-manager](https://github.com/danx123/smart-file-manager)

---

## ✨ Features

### 🗂️ Docking Interface
- **Drive Explorer Panel** (left) — OS-native icons, Quick Access shortcuts (Home, Desktop, Downloads, Documents, Pictures, Music, Videos), full drive/partition tree with lazy-loaded subfolders
- **File Browser** (center) — Sortable table with columns for Name, Size, Type, Modified, and Permissions; breadcrumb navigation bar; real-time search/filter
- **Smart Rename Panel** (bottom) — Tabbed interface with live preview grid and one-click application
- **Activity Log** (right) — Timestamped record of every operation, with export to `.txt`

All panels are fully dockable, floatable, closable, and restorable via **View → Panels**. Layout and state persist across sessions via `QSettings`.

### ✏️ Smart Rename Engine
- **Multi-pattern find & replace** — comma-separated rule pairs (e.g. `LK21-DE, (2023)-`)
- **Prefix / suffix injection**
- **Case conversion** — lowercase, UPPERCASE, Title Case, camelCase, snake_case
- **Extension override** — bulk-change file extensions
- **Auto-numbering** — configurable start value, zero-padding, and separator character
- **Regex mode** — full Python `re` syntax with capture group back-references
- **Special character removal** and **space replacement**
- **Live preview grid** — see every change before applying
- **Batch confirmation dialog** — review all renames in a scrollable table
- **Undo last batch** — single-click revert of the most recent rename operation

### 📁 File Operations
| Operation | Keyboard Shortcut |
|-----------|-------------------|
| Copy | `Ctrl+C` |
| Cut | `Ctrl+X` |
| Paste | `Ctrl+V` |
| Delete | `Delete` |
| Rename (single) | `F2` |
| New Folder | `Ctrl+Shift+N` |
| New File | `Ctrl+N` |
| Select All | `Ctrl+A` |
| Invert Selection | `Ctrl+I` |
| Open Terminal Here | `Ctrl+Alt+T` |
| Refresh | `F5` |
| Navigate Back / Forward | `Alt+Left / Alt+Right` |
| Navigate Up | `Alt+Up` |

### 🛠️ Built-in Tools
- **Duplicate File Finder** — MD5-based content hashing, results in Activity Log
- **Folder Size Calculator** — Recursive size aggregation with file count
- **Export Report** — Full folder listing exported as `.txt` (formatted table) or `.csv` (Excel-compatible)
- **Activity Log Export** — Save the full operation history as a plain-text file
- **File Properties Dialog** — Name, path, type, size, created/modified/accessed timestamps

### 🎨 Theming
- **Dark theme** — Deep navy/charcoal with violet accent (`#7C3AED`)
- **Light theme** — Clean white with the same violet accent
- Implemented entirely via **explicit QSS stylesheets** — no OS palette inheritance
- Built on Qt's **Fusion** base style for guaranteed cross-platform consistency
- Theme preference **saved and restored** automatically

### 💾 Persistence (QSettings)
| Setting | Stored Value |
|---------|-------------|
| Window geometry & size | ✅ |
| Dock layout & positions | ✅ |
| Floating dock state | ✅ |
| Selected theme | ✅ |
| Last visited directory | ✅ |

---

## 🔧 Installation

### Prerequisites

| Requirement | Minimum Version |
|-------------|----------------|
| Python | 3.10 |
| PySide6 | 6.5.0 |

### Install from source

```bash
# 1. Clone the repository
git clone https://github.com/danx123/smart-file-manager.git
cd smart-file-manager

# 2. (Recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the application
python SmartFileManager.py
```

### `requirements.txt`

```
PySide6>=6.5.0
```

> **Note:** On some Linux distributions, the `xcb` Qt platform plugin requires the system package `libxcb-cursor0`. Install it with:
> ```bash
> sudo apt install libxcb-cursor0    # Debian / Ubuntu
> sudo dnf install xcb-util-cursor   # Fedora / RHEL
> ```

### Optional: Build a standalone executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name SmartFileManager SmartFileManager.py
```

The compiled binary will be located at `dist/SmartFileManager` (Linux/macOS) or `dist/SmartFileManager.exe` (Windows).

---

## 🚀 Usage

### Launching

```bash
python SmartFileManager.py
```

### First-run layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Menu Bar                         Address Bar           🔍 Search   │
│  Toolbar: ◀ ▶ ▲ ↻ 🏠                                    🌙 Theme   │
├────────────────┬────────────────────────────────┬───────────────────┤
│                │  Breadcrumb: / home / user /   │                   │
│  EXPLORER      ├────────────────────────────────┤   ACTIVITY LOG   │
│                │                                │                   │
│  ⚡ QUICK      │   Name     Size  Type  Modified│  [10:30:01] ✅    │
│    Home        │   ───────────────────────────  │  Started          │
│    Desktop     │   📁 docs  <Folder>  Folder    │  [10:30:02] 📁    │
│    Downloads   │   📄 file  1.2 KB   Text       │  Navigated to /   │
│    Documents   │   ...                          │                   │
│                │                                │                   │
│  💾 DRIVES     │                                │                   │
│    Root (/)    │                                │                   │
│    /home       │                                │                   │
│    /tmp        │                                │                   │
├────────────────┴────────────────────────────────┴───────────────────┤
│  SMART RENAME                                                        │
│  Rules: [LK21-DE,        (2023)-              ]  Prefix [ ] Suffix  │
│  Preview:  Original  →  Renamed                                      │
│  [ ✅ Apply Rename ]  [ 👁 Preview All ]  [ ↩ Undo ]                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ✏️ Smart Rename

The rename engine is the core differentiator of SmartFileManager.

### Rule Syntax

Rules are entered as comma-separated pairs:

```
<pattern>, <replacement>[, <pattern2>, <replacement2>, ...]
```

An **empty replacement** (nothing between two commas) removes the matched text.

#### Examples

| Input Rules | Before | After |
|-------------|--------|-------|
| `LK21-DE, ` | `LK21-DE_Movie.mkv` | `_Movie.mkv` |
| `(2023)-, ` | `Film_(2023)_HD.mp4` | `Film__HD.mp4` |
| `Copy of , ` | `Copy of Report.pdf` | `Report.pdf` |
| `IMG_, Photo_` | `IMG_0042.jpg` | `Photo_0042.jpg` |
| `LK21-DE, , (2023)-, ` | `LK21-DE_Film_(2023).mp4` | `_Film_.mp4` |

### Regex Examples

| Pattern | Replacement | Effect |
|---------|-------------|--------|
| `\d{4}` | `` | Removes 4-digit numbers |
| `(\d{4})` | `[\1]` | Wraps year in brackets |
| `^(IMG_)` | `Photo_` | Replaces IMG_ prefix |
| `\s+` | `_` | Replaces whitespace with underscore |
| `[^\w.]` | `` | Strips all non-alphanumeric characters |

### Workflow

1. **Select files** in the browser (or select none to rename all)
2. Open **Smart Rename** panel at the bottom
3. Enter rules in the desired tab (Find & Replace / Numbering / Regex)
4. Review the **live preview grid**
5. Click **Apply Rename** → review the confirmation dialog → confirm
6. Use **Undo Last Rename** to revert if needed

---

## 📸 Screenshots
<img width="1365" height="767" alt="Screenshot 2026-03-11 232735" src="https://github.com/user-attachments/assets/844117f9-a68c-4100-be53-35f61d028b41" />

<img width="1365" height="767" alt="Screenshot 2026-03-11 232746" src="https://github.com/user-attachments/assets/d3466f05-c3c4-4da4-a84b-d610cfd8d880" />

<img width="1365" height="767" alt="Screenshot 2026-03-11 232755" src="https://github.com/user-attachments/assets/e3b9688b-d08d-4333-97a5-0b6a14bc8d70" />




---


## ⌨️ Keyboard Shortcut Reference

| Shortcut | Action |
|----------|--------|
| `Alt+Left` / `Alt+Right` | Navigate backward / forward |
| `Alt+Up` | Go up one directory level |
| `F5` | Refresh current folder |
| `F2` | Rename selected file |
| `F1` | Open Help Contents |
| `Ctrl+H` | Toggle hidden files |
| `Ctrl+A` | Select all |
| `Ctrl+I` | Invert selection |
| `Ctrl+C` / `Ctrl+X` / `Ctrl+V` | Copy / Cut / Paste |
| `Delete` | Delete selected |
| `Ctrl+N` | New file |
| `Ctrl+Shift+N` | New folder |
| `Ctrl+R` | Open Smart Rename panel |
| `Ctrl+Shift+R` | Batch Rename |
| `Ctrl+Alt+T` | Open terminal at current path |
| `Ctrl+Q` | Quit |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository at [github.com/danx123/smart-file-manager](https://github.com/danx123/smart-file-manager)
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow the existing code style and include docstrings for any new classes or public methods.

---

## 📄 License

This project is proprietary software.  
All rights reserved. Unauthorized copying, modification, distribution, or use of this software, via any medium, is strictly prohibited without explicit written permission from the author.

---

<div align="center">

**© Macan Angkasa — All Rights Reserved**

[github.com/danx123/smart-file-manager](https://github.com/danx123/smart-file-manager)

</div>
