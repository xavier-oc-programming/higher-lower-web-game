import os
import sys
import subprocess
from pathlib import Path

from art import LOGO

BUILDS = {
    "1": Path(__file__).parent / "original" / "main.py",
    "2": Path(__file__).parent / "advanced" / "main.py",
}

while True:
    os.system("cls" if os.name == "nt" else "clear")
    print(LOGO)
    print("Select a build to run:\n")
    print("  [1] Original  — single-file Flask app (course version)")
    print("  [2] Advanced  — modular Flask app with session & templates")
    print("  [q] Quit\n")

    choice = input("Enter choice: ").strip().lower()

    if choice == "q":
        break
    elif choice in BUILDS:
        path = BUILDS[choice]
        subprocess.run([sys.executable, str(path)], cwd=str(path.parent))
    else:
        print("Invalid choice. Try again.")
        input("\nPress Enter to continue...")
