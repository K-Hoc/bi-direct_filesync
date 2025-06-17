# 🌀 Bi-Directional File Sync Script

This Python script performs a **bi-directional synchronization** between two folders—typically a **local** directory and a **network/shared/server** directory. It ensures both locations contain the most recent versions of all files.

## 🔧 Features

- ✅ Bi-directional sync (local ↔ remote)
- ✅ Only copies files that are new or updated
- ✅ Automatically creates missing subdirectories
- ✅ Skips unwanted files (`.Rhistory`, `.tmp`, `.lock`)
- ✅ Clear, timestamped logging
- ✅ Accepts dynamic source and destination paths
- ✅ Ready to run as a scheduled task in Windows

---

## 🖥️ Usage

```bash
python sync.py <source_directory> <destination_directory>
````

### Example

```bash
python sync.py "C:\Users\Documents\local_Workspace\" "\\server\share\remote_Workspace\"
```

> ⚠️ Both paths must exist and be accessible when the script runs.

---

## 🗂 Ignored Files

The script skips files with the following extensions:

* `.Rhistory`
* `.tmp`
* `.lock`

You can modify this list in the script via the `IGNORED_EXTENSIONS` variable.

---

## Logging

* A `sync_log.txt` file is created in the same directory as the script.
* The log is **cleared on each run**.
* Logs include:

  * Start/end times
  * Skipped files
  * Copied files
  * Errors (e.g., permission denied)

---

## 📅 Scheduling in Windows Task Scheduler

You can schedule this script using **Task Scheduler**:

### Required:

| Field              | Value                                                   |
| ------------------ | ------------------------------------------------------- |
| **Program/script** | `C:\Path\To\Python\python.exe`                          |
| **Add arguments**  | `"C:\Path\To\sync.py" "source_path" "destination_path"` |
| **Start in**       | `C:\Path\To\ScriptDirectory` (optional but recommended) |

### Recommended Settings

* Run whether user is logged in or not
* Run with highest privileges
* Configure to stop the task if it runs longer than expected

---

## 🧪 Requirements

* Python 3.6+
* No external libraries required (only `os`, `shutil`, `logging`, `argparse`, `pathlib`)

---

## ✅ Example Use Case

You want to keep a local R project directory in sync with a shared network location, ensuring team members always have the latest files from either side.

```bash
python sync.py "C:\Users\me\R" "\\server\projects\shared\R"
```

---

## 📌 Notes

* The sync does not delete files that were removed from one side — it only **copies newer or missing files**.
* The script does not overwrite locked or in-use files.
* UNC paths must be fully accessible by the user under which the task runs.

---

## 📄 License

This script is provided as-is under the [MIT License](https://opensource.org/licenses/MIT).
