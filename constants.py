import os
import shutil
from pathlib import Path

from_ = os.path.expanduser("~/Downloads")
to = os.path.expanduser("~/Desktop")

# start with this
start_library = {
    "Important" : {"maxwell", "lokshin", "resume", "cover", "letter"},
    "Design Documents" : {"design", "document"},
    "Python Projects": {".py"},
    "React Projects": {".tsx", ".js", ".css", ".html"},
    "C Projects": {".c", ".cs", ".cpp"},
    "Java Projects": {".java"},
}

# end with this
end_library = {
    "Code": {"Python Projects", "React Projects", "C Projects", "Java Projects"},
    "Documents": {".pdf", ".docx", "Important", "Design Documents"},
    "Images": {".png", ".jpg", ".jpeg", ".gif", ".tiff", ".webp"},
    "Applications": {".exe"},
    "Extras": set()
}

# check if the file has any attributes similar to the list originally created
def type_of_file(folder, source, file, library):

    path = Path(file).resolve()
    path_parts = {part.lower() for part in path.parts}
    print(path_parts)
    for category, attributes in library.items():

        for part in path_parts:
            if any(keyword.lower() in part for keyword in attributes):
                print(file)
                return category, folder.lower() != source.lower()

    file_extension = os.path.splitext(file)[1].lower()
    for category, attributes in library.items():                                                # Check extension of file
        if file_extension in attributes:
            return category, folder.lower() != source.lower()
    # Check if in folder
    return None, folder.lower() != source.lower()


def categorize(source, library):
    title_list = list(library.keys())

    # create the original folder directories
    for category in library.keys():
        try:
            os.makedirs(os.path.join(source, category), exist_ok=True)
            print(f"Folder {os.path.join(source, category)} made successfully")
        except OSError:
            print("ERROR")

    # look at each file
    for folder, sub_folder, files in os.walk(source):

        path = Path(folder).resolve()
        path_parts = {part.lower() for part in path.parts}
        if not any(keyword.lower() in path_parts for keyword in title_list):
            if files:
                for file in files:
                    fullpath = os.path.join(folder, file)

                    # find out if it's in any specific category
                    category, isFolder = type_of_file(folder, source, fullpath, library) # finds name of file
                    print(isFolder)
                    # is it a folder
                    if isFolder:
                        source_path = Path(source).resolve()
                        folder_path = Path(folder).resolve()
                        try:
                            # Get the relative path from 'Desktop'
                            relative_part = folder_path.relative_to(source_path)

                            # Handle edge case where folder == source_path
                            if str(relative_part) == ".":
                                result = ""
                            else:
                                result = str(relative_part)

                            if "Extras" in library.keys() and not category:
                                category = "Extras"
                            if category:
                                final_destination = os.path.join(folder, os.path.join(source, category, result))
                                print(f"Moved {folder} \t=> \t{final_destination}")
                                # Move the folder
                                shutil.move(folder, final_destination)

                        except ValueError:
                            print(f"{folder_path} is not inside {source_path}")
                        break
                    if "Extras" in library.keys() and not category:
                        category = "Extras"
                    if category:
                        print(source, category, file)
                        final_destination = os.path.join(source, category, file)
                        print(f"Moved {fullpath} \t=> \t{final_destination}")
                        # Move the folder
                        shutil.move(fullpath, final_destination)
            elif not os.listdir(folder):
                # remove any empty folders
                os.rmdir(os.path.join(source, folder))
            else:
                print(f"SKIPPING {folder}")

def transfer(source, output, library):
    for category in library.keys():
        print(os.path.join(output, category))
        source_path = os.path.join(source,category)
        final_destination = os.path.join(output, category)
        shutil.move(source_path, final_destination)
        print(f"Moved {os.path.join(source,category)} → {final_destination}")

def undo(source, library):
    for category in library.keys():
        category_path = os.path.join(source, category)
        # look at each file
        for folder, sub_folders, files in os.walk(category_path):
            print(folder)
            if sub_folders:
                print(sub_folders)
                path_to_path(category_path, source, sub_folders)
            if files:
                print(files)
                path_to_path(category_path, source, files)

    for folder, sub_folders, files in os.walk(source):
        if not os.listdir(folder):
            # remove any empty folders
            print("REMOVING: ", os.path.join(folder))
            os.rmdir(os.path.join(folder))

def path_to_path(category_path, source, folder):
    # if not os.listdir(folder):
    #     # remove any empty folders
    #     os.rmdir(os.path.join(folder))
    #     return
    for file in folder:
        original_path = os.path.join(category_path, file)
        final_path = os.path.join(source, file)
        print(f"Moved {original_path} => {final_path}")
        shutil.move(original_path, final_path)
