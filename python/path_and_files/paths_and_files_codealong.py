# pathlib works with paths, files, and folders.
# shutil provides operations such as copying folders and checking disk space.
# Both modules are built into Python; no installation is needed.
# Run from the repository root:
# python/path_and_files/paths_and_files_codealong.py

from pathlib import Path
import shutil
from tempfile import TemporaryDirectory


def main():
    # 1. Build a path. The / operator joins sections of a path.
    # This only constructs a path; it does not create anything on disk.
    releases = Path("releases")
    version = releases / "v2" / "app.py"
    print(version)  # Windows: releases\v2\app.py

    # 2. Find useful locations.
    print(Path.cwd())   # The working directory where Python is running.
    print(Path.home())  # Your user home folder, such as C:\Users\alber.
    print(Path("~/deploy-project").expanduser())  # Replace ~ with your home.

    # 3. Find the containing folder and build a path beside a file.
    script = Path("/tmp/example/deploy.py")
    print(script.parent)
    print(script.parent / "deploy.yaml")
    # These paths do not need to exist. Windows displays backslashes.

    # 4. Read individual parts of a path.
    p = Path("releases/v2/app.py")
    print(p.name)    # app.py: filename including extension.
    print(p.stem)    # app: filename without its final extension.
    print(p.suffix)  # .py: final extension.
    print(p.parent)  # releases/v2: containing folder.
    print(p.parts)   # ('releases', 'v2', 'app.py'): path sections.

    # 5. Check whether a path exists and what it points to.
    p = Path("definitely-not-here.txt")
    print(p.exists())   # False if nothing exists here.
    print(p.is_file())  # True only for an existing file.
    print(p.is_dir())   # True only for an existing directory.

    # 6. List immediate contents of the working directory.
    # "." means the current directory. sorted puts the paths in order.
    # iterdir does not look inside subfolders.
    for item in sorted(Path(".").iterdir()):
        kind = "dir " if item.is_dir() else "file"
        print(f"{kind} {item.name}")

    # 7. Find Python files, including inside subfolders.
    # "*.py" matches names ending in .py.
    # glob("*.py") searches this folder; rglob also searches subfolders.
    for py in sorted(Path(".").rglob("*.py")):
        print(py)

    # Use a temporary practice folder for examples that create or delete files.
    # It is automatically cleaned up when this with block finishes.
    with TemporaryDirectory(
        prefix="paths_codealong_", dir=Path(__file__).parent
    ) as temporary_folder:
        practice = Path(temporary_folder)

        # 8. Create a folder and any missing parent folders.
        backup = practice / "app" / "backup"
        # parents=True creates app too if it is missing.
        # exist_ok=True accepts a folder that already exists.
        backup.mkdir(parents=True, exist_ok=True)
        print(backup.exists())  # True

        # 9. Write and delete a file.
        f = practice / "temp.txt"
        # write_text creates a file or replaces its existing contents.
        # \n starts a new line; UTF-8 specifies the text encoding.
        f.write_text("scratch\n", encoding="utf-8")
        f.unlink()             # Delete the file.
        print(f.exists())      # False
        # unlink raises FileNotFoundError if the file is already missing.

        # 10. Delete an empty directory.
        d = practice / "empty-dir"
        d.mkdir(exist_ok=True)
        d.rmdir()              # Raises OSError if the directory is not empty.
        print(d.exists())      # False

        # 11. Copy a whole folder, then delete the copy and its contents.
        # Bash equivalent of copytree: cp -r
        copied_app = practice / "app-copy"
        shutil.copytree(practice / "app", copied_app)
        print(copied_app.exists())  # True

        # Bash equivalent of rmtree: rm -rf
        # Unlike rmdir, rmtree deletes non-empty folders too.
        shutil.rmtree(copied_app)
        print(copied_app.exists())  # False

    # 12. Check storage on the drive containing the working directory.
    # On Windows, "/" means the root of the current drive.
    # Use "E:/" instead to choose your E drive explicitly.
    usage = shutil.disk_usage("/")

    # total, used, and free are measured in bytes.
    # 1e9 means 1,000,000,000; dividing by it converts bytes to GB.
    # An f-string inserts calculations inside braces.
    # :.1f displays one decimal place.
    print(f"total {usage.total / 1e9:.1f} GB")
    print(f"used  {usage.used / 1e9:.1f} GB")
    print(f"free  {usage.free / 1e9:.1f} GB")

    # used / total gives a fraction: 250 / 500 = 0.5.
    # :.1% formats that fraction as a percentage: 50.0%.
    print(f"{usage.used / usage.total:.1%} full")

    # 13. Find a program in the directories listed in your system's PATH.
    # which returns the executable's location, or None if it cannot find it.
    print(shutil.which("git"))
    print(shutil.which("definitely-not-a-real-program"))


# Run examples only when executing this file directly, not when importing it.
if __name__ == "__main__":
    main()
