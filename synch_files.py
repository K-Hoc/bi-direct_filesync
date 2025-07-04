import os
import shutil
import logging
import argparse
from pathlib import Path
from datetime import datetime

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description="Bi-directional file sync")
parser.add_argument("--src", help="Source directory", required=True)
parser.add_argument("--dst", help="Destination directory", required=True)
parser.add_argument(
    "-r",
    "--reference",
    choices=["source", "destination"],
    help="If specified, only syncs from one side to the other."
)
parser.add_argument(
    "--mirror",
    action="store_true",
    help="If set, makes the destination an exact mirror of the reference: deletes files!"
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Preview actions without making changes"
)
args = parser.parse_args()

LOCAL_DIR = Path(args.src)
REMOTE_DIR = Path(args.dst)

# List of file extensions to skip during syncing (commonly locked or unneeded files)
IGNORED_EXTENSIONS = [".Rhistory", ".tmp", ".lock"]

# Setup logging to file
log_file = Path(__file__).with_name("sync_log.txt")
logging.basicConfig(
    filename=log_file,
    filemode='w', # w means overwrite each time
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def delete_extra_files(reference_dir: Path, target_dir: Path):
    """
    🧹 Deletes files and folders in target_dir that do not exist in reference_dir.
    This is used for true mirroring.
    """
    for root, dirs, files in os.walk(target_dir, topdown=False):
        rel_path = Path(root).relative_to(target_dir)
        ref_path = reference_dir / rel_path

        # Delete files not in reference
        for file in files:
            target_file = Path(root) / file
            ref_file = ref_path / file
            if not ref_file.exists():
                if (args.dry_run):
                    logging.info(f"[Dry-run] Would delete file: {target_file}")
                else:
                    try:
                        target_file.unlink()
                        logging.info(f"Deleted extra file: {target_file}")
                    except Exception as e:
                        logging.error(f"Failed to delete file {target_file}: {e}")

        # Delete empty dirs not in reference
        for dir in dirs:
            target_subdir = Path(root) / dir
            ref_subdir = ref_path / dir
            if not ref_subdir.exists():
                if (args.dry_run):
                    logging.info(f"[Dry-run] Would delete directory:{target_subdir}")
                else:
                    try:
                        shutil.rmtree(target_subdir)
                        logging.info(f"Deleted extra directory: {target_subdir}")
                    except Exception as e:
                        logging.error(f"Failed to delete directory {target_subdir}: {e}")

def copy_file(src: Path, dst: Path):
    """
    📂 Copy a single file from src to dst.
    - Skips files in IGNORED_EXTENSIONS.
    - Automatically creates destination folders if they don't exist.
    - Logs or prints issues instead of crashing the whole sync.
    """
    try:
        # Skip unwanted files based on extension
        if any(src.name.endswith(ext) for ext in IGNORED_EXTENSIONS):
            logging.info(f"Skipped ignored file: {src}")
            return
        
        # Handling dry run (so just logging what would happen)
        if (args.dry_run):
            logging.info(f"[Dry-run] Would copy: {src} -> {dst}")
            return
        
        # Ensure the destination folder exists
        dst.parent.mkdir(parents=True, exist_ok=True)

        # Perform the copy (preserves metadata like modification time)
        shutil.copy2(src, dst)
        logging.info(f"Copied: {src} → {dst}")

    except PermissionError:
        logging.warning(f"Permission denied: {src}")
    except Exception as e:
        logging.error(f"Failed to copy {src} to {dst}: {e}")

def sync_dirs(src_dir: Path, dst_dir: Path):
    """
    🔁 Sync files from src_dir to dst_dir.
    - Recursively walks through the source directory.
    - Only copies files that are new or more recently modified.
    """
    for root, dirs, files in os.walk(src_dir):
        # Relative subdirectory from the source root
        rel_path = Path(root).relative_to(src_dir)
        for file in files:
            src_file = Path(root) / file # / file appends the filename to the path in a safe way
            dst_file = dst_dir / rel_path / file

            try:
                # Copy if destination file doesn't exist or is older than source
                if not dst_file.exists() or os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                    copy_file(src_file, dst_file)
            except Exception as e:
                logging.error(f"Error comparing {src_file} and {dst_file}: {e}")

def bi_directional_sync(dir1: Path, dir2: Path):
    """
    🔄 Perform a two-way sync:
    - First sync dir1 → dir2
    - Then sync dir2 → dir1
    This keeps both directories up to date with each other.
    """
    logging.info(f"Syncing from {dir1} to {dir2}")
    sync_dirs(dir1, dir2)

    logging.info(f"Syncing from {dir2} to {dir1}")
    sync_dirs(dir2, dir1)

if __name__ == "__main__":
    # Record and show when the sync starts
    start_time = datetime.now()
    logging.info("=== Sync started ===")

    # Check if both paths exist before syncing
    if not LOCAL_DIR.exists():
        logging.error(f"Local path not found: {LOCAL_DIR}")
    elif not REMOTE_DIR.exists():
        logging.error(f"Remote path not found: {REMOTE_DIR}")
    else:
        if (args.reference == "source"):
            logging.info("Reference mode: syncing source -> destination only")
            sync_dirs(LOCAL_DIR, REMOTE_DIR)
            if (args.mirror):
                logging.info("Mirror mode: deleting extra files in destination")
                delete_extra_files(LOCAL_DIR, REMOTE_DIR)
        elif (args.reference == "destination"):
            logging.info("Reference mode: syncing destination -> source only")
            sync_dirs(REMOTE_DIR, LOCAL_DIR)
            if (args.mirror):
                logging.info("Mirror mode: deleting extra files in destination")
                delete_extra_files(LOCAL_DIR, REMOTE_DIR)
        else:
            logging.info("Bi-directional sync mode")
            # Start the bi-directional sync
            bi_directional_sync(LOCAL_DIR, REMOTE_DIR)

    # Done! Safe total duration
    logging.info(f"✅ Sync complete. Duration: {datetime.now() - start_time}")