# 🌀 Bi-Directional File Sync Script
This Python script synchronizes files between two directories — commonly used to keep a **local folder** and a **network drive** or **remote folder** in sync. It ensures both locations contain the most recent versions of all files.

## 🧩 Features
- ✅ **Bi-directional sync** (default mode)
- ✅ **One-way sync** from a reference (`--reference`)
- ✅ **Mirror mode** (`--mirror`): deletes files/folders not present in the reference
- ✅ **Dry-run** support: simulate what would happen without modifying files
- ✅ Skips temp/locked/unwanted files (e.g., `.Rhistory`)
- ✅ Logs all actions to `sync_log.txt`
- 🧹 Safely handles permission errors without crashing

---

## 🧪 Requirements
* Python 3.6 or higher
* No external libraries required (only `os`, `shutil`, `logging`, `argparse`, `pathlib`)
* Windows (Tested with 10)

---

## 🚀 Usage
Run the script via command line or schedule it as a Windows task.

### 🔁 Bi-Directional Sync (default)
```bash
python sync.py --src "C:\Users\me\Documents\my_folder" --dst "\\server\shared\folder"
```

### ➡️ One-Way Sync Using Reference
```bash
python sync.py --src "C:\source" --dst "\\server\destination" --reference source
```
```bash
python sync.py --src "C:\source" --dst "\\server\destination" --reference destination
```

### Mirror Mode (with deletion)
```bash
python sync.py --src "C:\source" --dst "\\server\destination" --reference source --mirror
```
> ⚠️ **Warning** Files not present in the reference will be permanently deleted from the target!

### 🧪 Dry-Run (simulate actions only)
```bash
python sync.py --src "C:\source" --dst "\\server\destination" --reference source --mirror --dry-run
```

---

## ⚙️ Command-Line Arguments
| Argument      | Description                                                               |
| ------------- | ------------------------------------------------------------------------- |
| `--src`       | Source directory (e.g., local folder)                                     |
| `--dst`       | Destination directory (e.g., remote server path)                          |
| `--reference` | Optional. Set as `source` or `destination` to enable one-way syncing      |
| `--mirror`    | Optional. Deletes extra files/folders in the target to make a true mirror |
| `--dry-run`   | Optional. No changes made, logs what *would* be done                      |

---

## 🗂 Ignored Files
The script skips files with the following extensions:
* `.Rhistory`
* `.tmp`
* `.lock`
You can modify this list in the script via the `IGNORED_EXTENSIONS` variable.

---

## 📜 Logging

* A `sync_log.txt` file is created in the same directory as the script.
* The log is **cleared on each run**.
* Logs include:

  * Start and end times
  * Skipped / Copied / Deleted files
  * Errors and permission issues

---

## 📅 Scheduling with Windows Task Scheduler
To schedule automated syncing:
1. Open **Task Scheduler**
2. Create a new Task
3. In the **Actions** tab, add:
    * Program/Script: `python`
    * **Arguments**: `C:\path\to\synch_files.py "C:\src" "\\server\dst" --reference source --mirror`
    * Start in : `C:\path\to\script\directory`
4. Set **triggers** as desired (e.g. on login or every X minutes).
5. Ensure the task runs with highest privileges and correct user permissions.

---

## 📌 Notes
* Always test with `--dry-run` before using `--mirror`.
* Ensure mapped devices are accessible when scheduled (or use UNC paths).
* The script does not sync file deletions in bi-directional mode (only in mirror mode)
* Avoid syncing locked files or system directories

---

## ✨ Example
```bash
python sync.py --src "C:\Data" --dst "\\nas-server\backups\Data" --reference source --mirror
```
This will copy all newer files from `C:\Data` to the server and delete any files in the destination not present in the source.

---

## 📄 License
This script is provided as-is under the [MIT License](https://opensource.org/licenses/MIT).
