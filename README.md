Smart File Organiser Pro

A Python-based file management tool that automatically organises files into category-based folders using their file extensions.

Features

- Automatically sorts files into categories.
- Supports Images, Documents, Spreadsheets, Presentations, Audio, Videos, Archives, Code, Data and Fonts.
- Detects duplicate filenames and generates unique filenames.
- Dry-run mode to preview changes before moving files.
- Logging system to record activities.
- Error handling for file operations.
- Displays an organisation summary.

Technologies Used

- Python
- pathlib
- os
- shutil
- logging

How to Run

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Run:

python main.py

5. Enter the folder path you want to organise.
6. Choose preview mode ("yes") or actual organisation ("no").
7. Confirm before moving files.

Project Structure

SmartFileOrganiser/
├── main.py
├── README.md
└── .gitignore

Safety

Use preview mode before organising important folders. Always keep a backup of important files.

Author

Ganesh Singh