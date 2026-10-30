import os
import shutil
import logging
from pathlib import Path


# ==========================================
# 1. LOGGING CONFIGURATION
# ==========================================

logging.basicConfig(
    filename="organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================
# 2. FILE CATEGORIES
# ==========================================

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf"],
    "Spreadsheets": [".xlsx", ".xls", ".csv"],
    "Presentations": [".pptx", ".ppt"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Code": [".py", ".java", ".cpp", ".html", ".css", ".js"],
    "Data": [".json", ".xml", ".sql", ".db"],
    "Fonts": [".ttf", ".otf", ".woff"]
}


# ==========================================
# 3. GET FILE CATEGORY
# ==========================================

def get_category(file_extension):

    for category, extensions in CATEGORIES.items():

        if file_extension.lower() in extensions:
            return category

    return "Other"


# ==========================================
# 4. HANDLE DUPLICATE FILENAMES
# ==========================================

def get_unique_destination(destination):

    if not destination.exists():
        return destination

    folder = destination.parent
    filename = destination.name

    name, extension = os.path.splitext(filename)

    counter = 1

    while True:

        new_name = f"{name}_{counter}{extension}"

        new_destination = folder / new_name

        if not new_destination.exists():
            return new_destination

        counter += 1


# ==========================================
# 5. ORGANIZE FILES
# ==========================================

def organize_folder(folder_path, dry_run=False):

    moved_count = 0
    duplicate_count = 0
    error_count = 0
    planned_count = 0

    try:
        items = sorted(folder_path.iterdir())

    except OSError as error:
        print(f"Cannot read folder: {error}")
        logging.error(f"Cannot read folder: {error}")
        return None

    for item in items:

        # Skip folders and non-files
        if not item.is_file():
            continue

        # Avoid processing the log file
        if item.name == "organizer.log":
            continue

        try:
            # Get file extension
            extension = item.suffix.lower()

            # Find category
            category = get_category(extension)

            # Create destination folder path
            category_folder = folder_path / category

            # Create destination file path
            destination = category_folder / item.name

            # Check duplicate filename
            if destination.exists():

                duplicate_count += 1

                destination = get_unique_destination(destination)

                message = (
                    f"Duplicate renamed: {item.name} "
                    f"-> {destination.name}"
                )

                print(message)
                logging.warning(message)

            # Preview mode
            if dry_run:

                message = (
                    f"[PREVIEW] {item.name} "
                    f"-> {category}/{destination.name}"
                )

                print(message)
                logging.info(message)

                planned_count += 1

            # Actual file moving
            else:

                category_folder.mkdir(exist_ok=True)

                shutil.move(str(item), str(destination))

                message = (
                    f"Moved: {item.name} "
                    f"-> {category}/{destination.name}"
                )

                print(message)
                logging.info(message)

                moved_count += 1

        except OSError as error:

            message = f"Could not process {item.name}: {error}"

            print(message)
            logging.error(message)

            error_count += 1

    # Return results
    return {
        "moved": moved_count,
        "duplicates": duplicate_count,
        "errors": error_count,
        "planned": planned_count
    }


# ==========================================
# 6. DISPLAY SUMMARY
# ==========================================

def display_summary(results, dry_run):

    print("\n" + "=" * 40)
    print("          ORGANISATION SUMMARY")
    print("=" * 40)

    if dry_run:
        print(f"Files planned: {results['planned']}")
        print("Files actually moved: 0")

    else:
        print(f"Files moved: {results['moved']}")

    print(f"Duplicates renamed: {results['duplicates']}")
    print(f"Errors: {results['errors']}")

    print("=" * 40)


# ==========================================
# 7. MAIN PROGRAM
# ==========================================

def main():

    print("=" * 40)
    print("       SMART FILE ORGANISER PRO")
    print("=" * 40)

    # Get folder path
    folder_input = input(
        "\nEnter folder path: "
    ).strip().strip('"')

    folder_path = Path(folder_input)

    # Validate folder
    if not folder_path.exists() or not folder_path.is_dir():

        print("\nError: Folder does not exist!")

        logging.error(f"Invalid folder path: {folder_path}")

        return

    # Ask for preview mode
    choice = input(
        "\nPreview only? (yes/no): "
    ).strip().lower()

    if choice not in ("yes", "no"):

        print("Invalid choice. Enter yes or no.")
        return

    dry_run = choice == "yes"

    # Confirm actual file movement
    if not dry_run:

        confirmation = input(
            "\nThis will move files. Continue? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":

            print("Operation cancelled.")
            return

    print("\nStarting organisation...\n")

    # Organize folder
    results = organize_folder(folder_path, dry_run)

    if results is not None:

        display_summary(results, dry_run)

        print("\nOrganisation process completed!")

        logging.info("Organisation process completed.")


# ==========================================
# 8. PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()