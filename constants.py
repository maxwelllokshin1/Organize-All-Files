import os
import shutil
from pathlib import Path

from_ = os.path.expanduser("~/Downloads")
to = os.path.expanduser("~/Downloads")

# start with this
start_library = {
    "Important" : {"maxwell", "lokshin", "resume", "cover", "letter"},
    "Python Projects": {".py"},
    "React Projects": {".tsx", ".js", ".css", ".html"},
    "C Projects": {".c", ".cs", ".cpp"},
    "Java Projects": {".java"},
}

# end with this
end_library = {
    "Code": {"Python Projects", "React Projects", "C Projects", "Java Projects"},
    "Documents": {".pdf", ".docx", "Important"},
    "Extras": set()
}

# check if the file has any attributes similar to the list originally created
def type_of_file(folder, source, file, library):

    path = Path(file).resolve()
    path_parts = {part.lower() for part in path.parts}
    print(path_parts)
    for category, attributes in library.items():
        print(f"{category}: {attributes}")# Check parts of file
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
    print(library)
    title_list = []
    # create the original folder directories
    for category in library.keys():
        title_list.append(os.path.join(source, category))
        try:
            os.makedirs(os.path.join(source, category), exist_ok=True)
            print(f"Folder {os.path.join(source, category)} made successfully")
        except OSError:
            print("ERROR")

    # look at each file
    for folder, sub_folder, files in os.walk(source):

        # normalize paths for reliable comparison
        normalized_folder = os.path.normpath(folder).lower()
        # skip folders that are subfolders of the initial category folders
        if not any(normalized_folder == os.path.normpath(title).lower() or
                   normalized_folder.startswith(os.path.normpath(title).lower() + os.sep)
                   for title in title_list):
            if files:
                for file in files:
                    fullpath = os.path.join(folder, file)

                    # find out if it's in any specific category
                    category, isFolder = type_of_file(folder, source, fullpath, library) # finds name of file

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
                    elif category:
                        # not folder
                        print(f"{fullpath} \t=> \t{os.path.join(source, category, file)}")
                        shutil.move(fullpath, os.path.join(source, category, file))
            elif not os.listdir(folder):
                # remove any empty folders
                os.rmdir(os.path.join(source, folder))

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
                path_to_path(category_path, source, sub_folders)
            if files:
                path_to_path(category_path, source, files)

    for folder, sub_folders, files in os.walk(source):
        if not os.listdir(folder):
            # remove any empty folders
            os.rmdir(os.path.join(folder))

def path_to_path(category_path, source, library):
    for file in library:
        original_path = os.path.join(category_path, file)
        final_path = os.path.join(source, file)
        print(f"Moved {original_path} => {final_path}")
        shutil.move(original_path, final_path)