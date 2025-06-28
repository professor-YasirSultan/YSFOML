import os
import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import tkinter.font as tkFont
import shutil
import requests
import json # Import the json library

dummy_content = """
<YSFOML>
action:create;
filename:file1.txt
</YSFOML>
hey,
this is the first file1
by Yasir Sultan

<YSFOML>
action:append;
filename:file2.txt
</YSFOML>


hey,
this is the second file
developed by Yasir Sultan
-- Appended content --

<YSFOML>
action:create;
filename:daily_report.txt;
</YSFOML>
Daily sales report for 2025-06-27.
Total sales: $1500.00
New customers: 12

<YSFOML>
action:append;
filename:daily_report.txt;
</YSFOML>
Additional entry for 2025-06-28:
Total sales: $1800.00
New customers: 15

<YSFOML>
action:createFolder;
foldername:my_new_folder
</YSFOML>

<YSFOML>
action:create;
filename:my_new_folder/nested_file.txt
</YSFOML>
This file is inside my_new_folder.

<YSFOML>
action:rename;
filename:file1.txt;
filename2:renamed_file1.txt
</YSFOML>

<YSFOML>
action:move;
filepath1:file2.txt;
filepath2:my_new_folder/moved_file2.txt
</YSFOML>

<YSFOML>
action:treeFolders;
foldername:my_new_folder
</YSFOML>

<YSFOML>
action:treeFiles;
foldername:
</YSFOML>

<YSFOML>
action:findFile;
filename:renamed_file1.txt;
foldername:
</YSFOML>

<YSFOML>
action:findInFile;
filename:daily_report.txt;
searchString:sales
</YSFOML>

<YSFOML>
action:replaceInFile;
filename:daily_report.txt;
searchString:$;
newString:USD
</YSFOML>

<YSFOML>
action:readFileAll;
filename:daily_report.txt
</YSFOML>

<YSFOML>
action:readFileLines;
filename:daily_report.txt;
startLine:2;
endLine:3
</YSFOML>

<YSFOML>
action:insertAt;
filename:daily_report.txt;
lineNum:1;
colNum:1
</YSFOML>
--- START OF REPORT ---\n

<YSFOML>
action:downloadFile;
url:https://raw.githubusercontent.com/openai/openai-python/main/README.md;
localLocation:downloaded_readme.md
</YSFOML>

<YSFOML>
action:treeFoldersJSON;
foldername:my_new_folder
</YSFOML>

<YSFOML>
action:treeFilesJSON;
foldername:
</YSFOML>

<YSFOML>
action:delete;
filename:renamed_file1.txt
</YSFOML>

<YSFOML>
action:deleteFolder;
foldername:my_new_folder
</YSFOML>

<YSFOML>
action:unsupportedCustomAction;
actionSource:userAdded;
param1:test;
</YSFOML>
This is content for an unsupported custom action.
"""


class YSFOML_class:
    # Define security levels and their hierarchy
    SECURITY_LEVELS = {
        'treeFolders': 'low',
        'treeFiles': 'low',
        'treeFoldersJSON': 'low',  # Added new action
        'treeFilesJSON': 'low',    # Added new action
        'findFile': 'low',
        'findInFile': 'low',
        'readFileAll': 'low',
        'readFileLines': 'low',
        'create': 'medium',
        'append': 'medium',
        'createFolder': 'medium',
        'rename': 'medium',
        'move': 'medium',
        'replaceInFile': 'medium',
        'insertAt': 'medium',
        'downloadFile': 'medium',
        'delete': 'high',
        'deleteFolder': 'high',
        # 'runScript': 'extremelyHigh' # Placeholder for future extremelyHigh actions
    }

    LEVEL_ORDER = {'low': 0, 'medium': 1, 'high': 2, 'extremelyHigh': 3}

    def __init__(self, instructions_str: str, content: str):
        self.instructions_str = instructions_str
        self.content = content
        self.instructions_dic = self._parse_instructions_to_dict()

    def _parse_instructions_to_dict(self) -> dict[str, str]:
        result_dict = {}
        lines = self.instructions_str.splitlines()

        for line in lines:
            stripped_line = line.strip()

            if stripped_line.endswith(';'):
                stripped_line = stripped_line[:-1]

            if stripped_line:
                parts = stripped_line.split(':', 1)
                key = parts[0].strip()

                if len(parts) > 1:
                    value = parts[1].strip()
                else:
                    value = ""

                result_dict[key] = value
        return result_dict

    def display_instructions_as_table(self) -> str:
        output_lines = []
        left_marg = "      "
        output_lines.append("Instructions:")
        output_lines.append(f"{left_marg}{'Key':<20} | Value")
        output_lines.append(left_marg + "-" * 50)

        for key, value in self.instructions_dic.items():
            formatted_key = f"{key:<20}"
            output_lines.append(f"{left_marg}{formatted_key} | {value}")
        return "\n".join(output_lines)

    def display_info(self) -> str:
        output_lines = []
        output_lines.append(self.display_instructions_as_table())
        output_lines.append(f"Content: \n{self.content}")
        return "\n".join(output_lines)

    def _backup_existing_file(self, file_path: str, log_widget: scrolledtext.ScrolledText, copy_mode: bool = False) -> bool:
        """
        Backs up an existing file.
        If copy_mode is True, it copies the file.
        If copy_mode is False, it renames (moves) the file.
        Returns True on success, False on failure.
        """
        if os.path.exists(file_path):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            name_part, ext_part = os.path.splitext(os.path.basename(file_path))
            backup_filename = f"{name_part}_backup_{timestamp}{ext_part}"
            backup_file_path = os.path.join(os.path.dirname(file_path), backup_filename)

            try:
                if copy_mode:
                    shutil.copy2(file_path, backup_file_path)
                    msg = f"Existing file '{os.path.basename(file_path)}' copied to '{backup_filename}' as backup."
                else:
                    os.rename(file_path, backup_file_path)
                    msg = f"Existing file '{os.path.basename(file_path)}' backed up (renamed) to '{backup_filename}'."
                log_widget.insert(tk.END, msg + "\n")
                return True
            except OSError as e:
                msg = f"Error backing up file '{file_path}' to '{backup_file_path}': {e}"
                log_widget.insert(tk.END, msg + "\n")
                return False
        return True # No file to backup, so it's a success

    def _move_to_trash(self, item_path: str, is_folder: bool, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        """
        Renames and moves a file or folder to a designated trash folder.
        Returns True on success, False on failure.
        """
        if not os.path.exists(item_path):
            log_widget.insert(tk.END, f"Item not found: '{item_path}'. Cannot move to trash.\n")
            return False

        trash_folder = os.path.join(base_folder, "YSFOML_Trash")
        try:
            os.makedirs(trash_folder, exist_ok=True)
        except OSError as e:
            log_widget.insert(tk.END, f"Error creating trash directory '{trash_folder}': {e}\n")
            return False

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        name_part = os.path.basename(item_path)
        new_name = f"{name_part}_removed_{timestamp}"
        target_path_in_trash = os.path.join(trash_folder, new_name)

        try:
            shutil.move(item_path, target_path_in_trash)
            item_type = "folder" if is_folder else "file"
            log_widget.insert(tk.END, f"Successfully moved {item_type} '{item_path}' to trash as '{target_path_in_trash}'\n")
            return True
        except shutil.Error as e:
            log_widget.insert(tk.END, f"Error moving '{item_path}' to trash: {e}\n")
            return False
        except OSError as e:
            log_widget.insert(tk.END, f"OS Error moving '{item_path}' to trash: {e}\n")
            return False

    def create_file_backup(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        filename = self.instructions_dic.get('filename')
        if not filename:
            msg = f"Warning: No 'filename' key found in instructions for this object. Cannot create file."
            log_widget.insert(tk.END, msg + "\n")
            return False

        file_path = os.path.join(base_folder, filename)

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        except OSError as e:
            msg = f"Error creating directory for file '{file_path}': {e}"
            log_widget.insert(tk.END, msg + "\n")
            return False

        if not self._backup_existing_file(file_path, log_widget, copy_mode=False):
            return False

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.content)
            msg = f"Successfully created file: {file_path}"
            log_widget.insert(tk.END, msg + "\n")
            return True
        except IOError as e:
            msg = f"Error creating file '{file_path}': {e}"
            log_widget.insert(tk.END, msg + "\n")
            return False

    def append_file_backup(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        filename = self.instructions_dic.get('filename')
        if not filename:
            msg = f"Warning: No 'filename' key found in instructions for this object. Cannot append to file."
            log_widget.insert(tk.END, msg + "\n")
            return False

        file_path = os.path.join(base_folder, filename)

        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        except OSError as e:
            msg = f"Error creating directory for file '{file_path}': {e}"
            log_widget.insert(tk.END, msg + "\n")
            return False

        if not self._backup_existing_file(file_path, log_widget, copy_mode=True):
            return False

        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(self.content)
            msg = f"Successfully appended content to file: {file_path}"
            log_widget.insert(tk.END, msg + "\n")
            return True
        except IOError as e:
            msg = f"Error appending to file '{file_path}': {e}"
            log_widget.insert(tk.END, msg + "\n")
            return False

    def delete_file(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        filename = self.instructions_dic.get('filename')
        if not filename:
            log_widget.insert(tk.END, "Warning: No 'filename' key found for delete operation.\n")
            return False

        file_path = os.path.join(base_folder, filename)
        return self._move_to_trash(file_path, is_folder=False, base_folder=base_folder, log_widget=log_widget)

    def create_folder(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        foldername = self.instructions_dic.get('foldername')
        if not foldername:
            log_widget.insert(tk.END, "Warning: No 'foldername' key found for createFolder operation.\n")
            return False

        folder_path = os.path.join(base_folder, foldername)
        try:
            os.makedirs(folder_path, exist_ok=True)
            log_widget.insert(tk.END, f"Successfully created folder: '{folder_path}' (or it already existed).\n")
            return True
        except OSError as e:
            log_widget.insert(tk.END, f"Error creating folder '{folder_path}': {e}\n")
            return False

    def delete_folder(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        foldername = self.instructions_dic.get('foldername')
        if not foldername:
            log_widget.insert(tk.END, "Warning: No 'foldername' key found for deleteFolder operation.\n")
            return False

        folder_path = os.path.join(base_folder, foldername)
        return self._move_to_trash(folder_path, is_folder=True, base_folder=base_folder, log_widget=log_widget)

    def rename_file(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        old_filename = self.instructions_dic.get('filename')
        new_filename = self.instructions_dic.get('filename2')
        if not old_filename or not new_filename:
            log_widget.insert(tk.END, "Warning: Both 'filename' (old) and 'filename2' (new) keys are required for rename operation.\n")
            return False

        old_path = os.path.join(base_folder, old_filename)
        new_path = os.path.join(base_folder, new_filename)

        if not os.path.exists(old_path):
            log_widget.insert(tk.END, f"Old file not found: '{old_path}'. Cannot rename.\n")
            return False

        if os.path.exists(new_path):
            log_widget.insert(tk.END, f"New file name already exists: '{new_path}'. Cannot rename.\n")
            return False

        try:
            os.rename(old_path, new_path)
            log_widget.insert(tk.END, f"Successfully renamed '{old_path}' to '{new_path}'\n")
            return True
        except OSError as e:
            log_widget.insert(tk.END, f"Error renaming file from '{old_path}' to '{new_path}': {e}\n")
            return False

    def move_file(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        source_path_str = self.instructions_dic.get('filepath1')
        destination_path_str = self.instructions_dic.get('filepath2')
        if not source_path_str or not destination_path_str:
            log_widget.insert(tk.END, "Warning: Both 'filepath1' (source) and 'filepath2' (destination) keys are required for move operation.\n")
            return False

        source_path = os.path.join(base_folder, source_path_str)
        destination_path = os.path.join(base_folder, destination_path_str)

        if not os.path.exists(source_path):
            log_widget.insert(tk.END, f"Source path not found: '{source_path}'. Cannot move.\n")
            return False

        if os.path.exists(destination_path):
            log_widget.insert(tk.END, f"Error: Destination path already exists '{destination_path}'. Move aborted.\n")
            return False

        dest_dir = os.path.dirname(destination_path)
        if dest_dir and not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir, exist_ok=True)
                log_widget.insert(tk.END, f"Created destination directory: '{dest_dir}'\n")
            except OSError as e:
                log_widget.insert(tk.END, f"Error creating destination directory '{dest_dir}': {e}\n")
                return False

        try:
            shutil.move(source_path, destination_path)
            log_widget.insert(tk.END, f"Successfully moved '{source_path}' to '{destination_path}'\n")
            return True
        except shutil.Error as e:
            log_widget.insert(tk.END, f"Error moving '{source_path}' to '{destination_path}': {e}\n")
            return False
        except OSError as e:
            log_widget.insert(tk.END, f"OS Error moving '{source_path}' to '{destination_path}': {e}\n")
            return False

    def _get_tree_output(self, base_folder: str, include_files: bool, log_widget: scrolledtext.ScrolledText) -> str | None:
        foldername = self.instructions_dic.get('foldername')
        start_path = os.path.join(base_folder, foldername) if foldername else base_folder

        if not os.path.exists(start_path):
            log_widget.insert(tk.END, f"Path not found: '{start_path}'. Cannot display tree.\n")
            return None
        if not os.path.isdir(start_path):
            log_widget.insert(tk.END, f"Path is not a directory: '{start_path}'. Cannot display tree.\n")
            return None

        output_lines = []
        for root, dirs, files in os.walk(start_path):
            # Calculate relative path from start_path to current root
            relative_path = os.path.relpath(root, start_path)
            if relative_path == ".": # If it's the start_path itself
                level = 0
            else:
                level = relative_path.count(os.sep) + 1 # +1 because os.sep count is 0 for direct children

            indent = ' ' * 4 * (level)
            output_lines.append(f"{indent}{os.path.basename(root)}/")
            if include_files:
                subindent = ' ' * 4 * (level + 1)
                for f in files:
                    output_lines.append(f"{subindent}{f}")
        return "\n".join(output_lines) + "\n"

    def _get_tree_output_json(self, base_folder: str, include_files: bool, log_widget: scrolledtext.ScrolledText) -> str | None:
        """
        Generates a JSON string representing the folder/file tree.
        """
        foldername = self.instructions_dic.get('foldername')
        start_path = os.path.join(base_folder, foldername) if foldername else base_folder

        if not os.path.exists(start_path):
            log_widget.insert(tk.END, f"Path not found: '{start_path}'. Cannot display tree in JSON.\n")
            return None
        if not os.path.isdir(start_path):
            log_widget.insert(tk.END, f"Path is not a directory: '{start_path}'. Cannot display tree in JSON.\n")
            return None

        tree_dict = {
            "name": os.path.basename(start_path),
            "type": "directory",
            "path": os.path.relpath(start_path, base_folder),
            "contents": []
        }

        # Use a stack for iterative traversal to build the nested dictionary
        # Stack stores (current_path, current_dict_contents_list)
        stack = [(start_path, tree_dict["contents"])]

        while stack:
            current_path, current_contents_list = stack.pop(0) # Use pop(0) for BFS-like order

            try:
                for item in os.listdir(current_path):
                    item_path = os.path.join(current_path, item)
                    relative_item_path = os.path.relpath(item_path, base_folder)

                    if os.path.isdir(item_path):
                        folder_entry = {
                            "name": item,
                            "type": "directory",
                            "path": relative_item_path,
                            "contents": []
                        }
                        current_contents_list.append(folder_entry)
                        stack.append((item_path, folder_entry["contents"]))
                    elif include_files and os.path.isfile(item_path):
                        file_entry = {
                            "name": item,
                            "type": "file",
                            "path": relative_item_path
                        }
                        current_contents_list.append(file_entry)
            except OSError as e:
                log_widget.insert(tk.END, f"Error listing directory '{current_path}': {e}\n")
                # Continue processing other parts of the tree if possible

        try:
            return json.dumps(tree_dict, indent=2)
        except Exception as e:
            log_widget.insert(tk.END, f"Error converting tree to JSON: {e}\n")
            return None


    def _get_found_files_output(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> str | None:
        filename_to_find = self.instructions_dic.get('filename')
        search_folder_name = self.instructions_dic.get('foldername')

        if not filename_to_find:
            log_widget.insert(tk.END, "Warning: 'filename' key is required for findFile operation.\n")
            return None

        search_path = os.path.join(base_folder, search_folder_name) if search_folder_name else base_folder

        log_widget.insert(tk.END, f"Searching for '{filename_to_find}' in '{search_path}'...\n")
        found_paths = []
        if not os.path.exists(search_path) or not os.path.isdir(search_path):
            log_widget.insert(tk.END, f"Search path does not exist or is not a directory: '{search_path}'.\n")
            return None

        for root, _, files in os.walk(search_path):
            if filename_to_find in files:
                found_paths.append(os.path.join(root, filename_to_find))

        output_lines = []
        if found_paths:
            output_lines.append(f"Found '{filename_to_find}' at:")
            for p in found_paths:
                output_lines.append(f"  - {p}")
        else:
            output_lines.append(f"'{filename_to_find}' not found in '{search_path}'.")
        return "\n".join(output_lines) + "\n"

    def _get_find_in_file_output(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> str | None:
        filename = self.instructions_dic.get('filename')
        search_string = self.instructions_dic.get('searchString')

        if not filename or not search_string:
            log_widget.insert(tk.END, "Warning: Both 'filename' and 'searchString' keys are required for findInFile operation.\n")
            return None

        file_path = os.path.join(base_folder, filename)
        if not os.path.exists(file_path):
            log_widget.insert(tk.END, f"File not found: '{file_path}'. Cannot search.\n")
            return None

        log_widget.insert(tk.END, f"Searching for '{search_string}' in '{file_path}'...\n")
        found_locations = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    line_num = i + 1
                    col_num = 0
                    while True:
                        idx = line.find(search_string, col_num)
                        if idx == -1:
                            break
                        found_locations.append((line_num, idx + 1))
                        col_num = idx + len(search_string)
            output_lines = []
            if found_locations:
                output_lines.append("Found occurrences:")
                for loc in found_locations:
                    output_lines.append(f"  - Line: {loc[0]}, Column: {loc[1]}")
            else:
                output_lines.append(f"'{search_string}' not found in '{file_path}'.")
            return "\n".join(output_lines) + "\n"
        except IOError as e:
            log_widget.insert(tk.END, f"Error reading file '{file_path}': {e}\n")
            return None

    def replace_in_file(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        filename = self.instructions_dic.get('filename')
        search_string = self.instructions_dic.get('searchString')
        new_string = self.instructions_dic.get('newString')

        if not filename or not search_string or new_string is None:
            log_widget.insert(tk.END, "Warning: 'filename', 'searchString', and 'newString' keys are required for replaceInFile operation.\n")
            return False

        file_path = os.path.join(base_folder, filename)
        if not os.path.exists(file_path):
            log_widget.insert(tk.END, f"File not found: '{file_path}'. Cannot replace content.\n")
            return False

        if not self._backup_existing_file(file_path, log_widget, copy_mode=True):
            log_widget.insert(tk.END, "Replacement aborted due to backup failure.\n")
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            new_content = original_content.replace(search_string, new_string)

            if original_content == new_content:
                log_widget.insert(tk.END, f"'{search_string}' not found in '{file_path}'. No replacements made.\n")
                return True # Not an error, just no changes
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            log_widget.insert(tk.END, f"Successfully replaced '{search_string}' with '{new_string}' in '{file_path}'.\n")
            return True
        except IOError as e:
            log_widget.insert(tk.END, f"Error replacing content in file '{file_path}': {e}\n")
            return False

    def _get_file_content_all(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> str | None:
        filename = self.instructions_dic.get('filename')
        if not filename:
            log_widget.insert(tk.END, "Warning: 'filename' key is required for readFileAll operation.\n")
            return None

        file_path = os.path.join(base_folder, filename)
        if not os.path.exists(file_path):
            log_widget.insert(tk.END, f"File not found: '{file_path}'. Cannot read.\n")
            return None
        if os.path.isdir(file_path):
            log_widget.insert(tk.END, f"Path is a directory: '{file_path}'. Cannot read as file.\n")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except IOError as e:
            log_widget.insert(tk.END, f"Error reading file '{file_path}': {e}\n")
            return None

    def _get_file_content_lines(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> str | None:
        filename = self.instructions_dic.get('filename')
        try:
            start_line = int(self.instructions_dic.get('startLine', 1))
            end_line = int(self.instructions_dic.get('endLine', -1))
        except ValueError:
            log_widget.insert(tk.END, "Warning: 'startLine' and 'endLine' must be integers for readFileLines operation.\n")
            return None

        if not filename:
            log_widget.insert(tk.END, "Warning: 'filename' key is required for readFileLines operation.\n")
            return None

        file_path = os.path.join(base_folder, filename)
        if not os.path.exists(file_path):
            log_widget.insert(tk.END, f"File not found: '{file_path}'. Cannot read lines.\n")
            return None
        if os.path.isdir(file_path):
            log_widget.insert(tk.END, f"Path is a directory: '{file_path}'. Cannot read as file.\n")
            return None

        output_lines = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                total_lines = len(lines)

                if end_line == -1 or end_line > total_lines:
                    end_line_actual = total_lines
                else:
                    end_line_actual = end_line

                if start_line > total_lines:
                    log_widget.insert(tk.END, f"Start line ({start_line}) is beyond total lines ({total_lines}). No content to display.\n")
                    return None
                if start_line <= 0:
                    start_line = 1

                for i in range(start_line - 1, end_line_actual):
                    if 0 <= i < total_lines:
                        stripped_line_content = lines[i].rstrip('\n')
                        output_lines.append(f"[{i+1}]: {stripped_line_content}")
            return "\n".join(output_lines) + "\n"
        except IOError as e:
            log_widget.insert(tk.END, f"Error reading file '{file_path}': {e}\n")
            return None

    def insert_at(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        filename = self.instructions_dic.get('filename')
        text_to_insert = self.content
        try:
            line_num = int(self.instructions_dic.get('lineNum'))
            col_num = int(self.instructions_dic.get('colNum'))
        except (ValueError, TypeError):
            log_widget.insert(tk.END, "Warning: 'lineNum' and 'colNum' must be integers for insertAt operation.\n")
            return False

        if not filename or not text_to_insert:
            log_widget.insert(tk.END, "Warning: 'filename', 'lineNum', 'colNum', and content (text to insert) are required for insertAt operation.\n")
            return False

        file_path = os.path.join(base_folder, filename)
        if not os.path.exists(file_path):
            log_widget.insert(tk.END, f"File not found: '{file_path}'. Cannot insert text.\n")
            return False

        if not self._backup_existing_file(file_path, log_widget, copy_mode=True):
            log_widget.insert(tk.END, "Insert operation aborted due to backup failure.\n")
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            target_line_idx = line_num - 1

            if not (0 <= target_line_idx < len(lines)):
                log_widget.insert(tk.END, f"Error: Line number {line_num} is out of bounds for file '{file_path}' (total lines: {len(lines)}).\n")
                return False

            original_line = lines[target_line_idx]
            actual_col_num = min(col_num - 1, len(original_line.rstrip('\n')))

            modified_line = original_line[:actual_col_num] + text_to_insert + original_line[actual_col_num:]
            lines[target_line_idx] = modified_line

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            log_widget.insert(tk.END, f"Successfully inserted text at Line {line_num}, Column {col_num} in '{file_path}'.\n")
            return True
        except IOError as e:
            log_widget.insert(tk.END, f"Error inserting text into file '{file_path}': {e}\n")
            return False
        except Exception as e:
            log_widget.insert(tk.END, f"An unexpected error occurred during insertAt operation: {e}\n")
            return False

    def download_file(self, base_folder: str, log_widget: scrolledtext.ScrolledText) -> bool:
        url = self.instructions_dic.get('url')
        local_location = self.instructions_dic.get('localLocation')

        if not url or not local_location:
            log_widget.insert(tk.END, "Warning: Both 'url' and 'localLocation' keys are required for downloadFile operation.\n")
            return False

        local_file_path = os.path.join(base_folder, local_location)
        local_dir = os.path.dirname(local_file_path)

        try:
            os.makedirs(local_dir, exist_ok=True)
        except OSError as e:
            log_widget.insert(tk.END, f"Error creating local directory '{local_dir}': {e}\n")
            return False

        # Backup existing file if it exists before downloading (which overwrites)
        if os.path.exists(local_file_path):
            if not self._backup_existing_file(local_file_path, log_widget, copy_mode=False): # Rename existing
                log_widget.insert(tk.END, "Download aborted due to backup failure.\n")
                return False

        log_widget.insert(tk.END, f"Attempting to download from '{url}' to '{local_file_path}'...\n")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(local_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            log_widget.insert(tk.END, f"Successfully downloaded '{url}' to '{local_file_path}'\n")
            return True
        except requests.exceptions.RequestException as e:
            log_widget.insert(tk.END, f"Error downloading file from '{url}': {e}\n")
            return False
        except IOError as e:
            log_widget.insert(tk.END, f"Error writing downloaded file to '{local_file_path}': {e}\n")
            return False


    def process_instructions(self, base_folder: str, log_widget: scrolledtext.ScrolledText, results_widget: scrolledtext.ScrolledText, current_security_level: str) -> bool:
        """
        Processes a single YSFOML instruction object.
        Returns True if the operation was successful or a read-only operation, False if an error occurred
        during a modifying operation or if permission is denied.
        """
        op = self.instructions_dic.get('action')
        action_source = self.instructions_dic.get('actionSource')

        log_widget.insert(tk.END, f"Processing action: '{op}'\n")

        success = True # Assume success for read-only operations or until an error occurs for modifying ones

        # Check for unknown or user-added actions first
        if op not in self.SECURITY_LEVELS:
            if action_source == 'userAdded':
                log_widget.insert(tk.END, f"Action '{op}' is a user-added action and is not supported for execution yet.\n")
                return False # Treat as failure for now
            else:
                log_widget.insert(tk.END, f"Warning: Unknown or missing 'action' instruction '{op}'. Skipping file operation for this object.\n")
                return False # Treat as failure for unknown actions

        # Check security level
        required_level = self.SECURITY_LEVELS.get(op)
        if self.LEVEL_ORDER.get(current_security_level, -1) < self.LEVEL_ORDER.get(required_level, -1):
            log_widget.insert(tk.END, f"Permission Denied: Action '{op}' requires '{required_level}' security level, but current level is '{current_security_level}'.\n")
            return False

        # Warn if userAdded is specified for a built-in action
        if action_source == 'userAdded' and op in self.SECURITY_LEVELS:
            log_widget.insert(tk.END, f"Warning: 'actionSource: userAdded' specified for built-in action '{op}'. This parameter is intended for custom actions.\n")

        # Execute the action based on 'op'
        if op == 'create':
            success = self.create_file_backup(base_folder, log_widget)
        elif op == 'append':
            success = self.append_file_backup(base_folder, log_widget)
        elif op == 'delete':
            success = self.delete_file(base_folder, log_widget)
        elif op == 'createFolder':
            success = self.create_folder(base_folder, log_widget)
        elif op == 'deleteFolder':
            success = self.delete_folder(base_folder, log_widget)
        elif op == 'rename':
            success = self.rename_file(base_folder, log_widget)
        elif op == 'move':
            success = self.move_file(base_folder, log_widget)
        elif op == 'treeFolders':
            tree_output = self._get_tree_output(base_folder, include_files=False, log_widget=log_widget)
            if tree_output is not None:
                results_widget.insert(tk.END, f"--- Folder Tree for '{self.instructions_dic.get('foldername', base_folder)}' ---\n")
                results_widget.insert(tk.END, tree_output)
                results_widget.insert(tk.END, f"--- End Folder Tree ---\n")
            # Read-only operation, doesn't affect overall success for stopping
        elif op == 'treeFiles':
            tree_output = self._get_tree_output(base_folder, include_files=True, log_widget=log_widget)
            if tree_output is not None:
                results_widget.insert(tk.END, f"--- File Tree for '{self.instructions_dic.get('foldername', base_folder)}' ---\n")
                results_widget.insert(tk.END, tree_output)
                results_widget.insert(tk.END, f"--- End File Tree ---\n")
            # Read-only operation
        elif op == 'treeFoldersJSON': # New action
            json_output = self._get_tree_output_json(base_folder, include_files=False, log_widget=log_widget)
            if json_output is not None:
                results_widget.insert(tk.END, f"--- Folder Tree JSON for '{self.instructions_dic.get('foldername', base_folder)}' ---\n")
                results_widget.insert(tk.END, json_output)
                results_widget.insert(tk.END, f"\n--- End Folder Tree JSON ---\n")
        elif op == 'treeFilesJSON': # New action
            json_output = self._get_tree_output_json(base_folder, include_files=True, log_widget=log_widget)
            if json_output is not None:
                results_widget.insert(tk.END, f"--- File Tree JSON for '{self.instructions_dic.get('foldername', base_folder)}' ---\n")
                results_widget.insert(tk.END, json_output)
                results_widget.insert(tk.END, f"\n--- End File Tree JSON ---\n")
        elif op == 'findFile':
            found_paths_str = self._get_found_files_output(base_folder, log_widget)
            if found_paths_str is not None:
                results_widget.insert(tk.END, f"--- Find File Results for '{self.instructions_dic.get('filename')}' ---\n")
                results_widget.insert(tk.END, found_paths_str)
                results_widget.insert(tk.END, f"--- End Find File Results ---\n")
            # Read-only operation
        elif op == 'findInFile':
            found_locations_str = self._get_find_in_file_output(base_folder, log_widget)
            if found_locations_str is not None:
                results_widget.insert(tk.END, f"--- Find In File Results for '{self.instructions_dic.get('searchString')}' in '{self.instructions_dic.get('filename')}' ---\n")
                results_widget.insert(tk.END, found_locations_str)
                results_widget.insert(tk.END, f"--- End Find In File Results ---\n")
            # Read-only operation
        elif op == 'replaceInFile':
            success = self.replace_in_file(base_folder, log_widget)
        elif op == 'readFileAll':
            file_content = self._get_file_content_all(base_folder, log_widget)
            if file_content is not None:
                results_widget.insert(tk.END, f"--- Content of '{self.instructions_dic.get('filename')}' ---\n")
                results_widget.insert(tk.END, file_content)
                results_widget.insert(tk.END, f"--- End of '{self.instructions_dic.get('filename')}' ---\n")
            # Read-only operation
        elif op == 'readFileLines':
            file_content_lines = self._get_file_content_lines(base_folder, log_widget)
            if file_content_lines is not None:
                results_widget.insert(tk.END, f"--- Content of '{self.instructions_dic.get('filename')}' (Lines {self.instructions_dic.get('startLine', '1')}-{self.instructions_dic.get('endLine', 'End')}) ---\n")
                results_widget.insert(tk.END, file_content_lines)
                results_widget.insert(tk.END, f"--- End of '{self.instructions_dic.get('filename')}' ---\n")
            # Read-only operation
        elif op == 'insertAt':
            success = self.insert_at(base_folder, log_widget)
        elif op == 'downloadFile':
            success = self.download_file(base_folder, log_widget)
        else:
            # This block should ideally not be reached if SECURITY_LEVELS is comprehensive
            log_widget.insert(tk.END, f"Error: Action '{op}' was not handled. This indicates an internal logic error.\n")
            success = False

        return success


def parse_YSFOML_string(full_text: str) -> tuple[list[YSFOML_class], list[str]]:
    start_tag = "<YSFOML>"
    end_tag = "</YSFOML>"

    YSFOML_objects = []
    warnings = []

    current_pos = 0
    while True:
        start_tag_index = full_text.find(start_tag, current_pos)

        if start_tag_index == -1:
            break

        end_tag_index = full_text.find(end_tag, start_tag_index)

        if end_tag_index == -1:
            warnings.append(f"Warning: Found '{start_tag}' at position {start_tag_index} but no matching '{end_tag}'. Skipping remaining content.")
            break

        raw_instructions = full_text[start_tag_index + len(start_tag) : end_tag_index]
        instructions = raw_instructions[1:] if raw_instructions.startswith('\n') else raw_instructions

        content_start_index = end_tag_index + len(end_tag)

        next_start_tag_index = full_text.find(start_tag, content_start_index)

        if next_start_tag_index != -1:
            raw_content = full_text[content_start_index : next_start_tag_index]
            content = raw_content[1:] if raw_content.startswith('\n') else raw_content
            current_pos = next_start_tag_index
        else:
            raw_content = full_text[content_start_index:]
            content = raw_content[1:] if raw_content.startswith('\n') else raw_content
            current_pos = len(full_text)

        obj = YSFOML_class(instructions, content)
        YSFOML_objects.append(obj)

        if current_pos >= len(full_text):
            break

    return YSFOML_objects, warnings

class YSFOML_GUI:
    def __init__(self, master):
        self.master = master
        master.title("YSFOML (Yasir Sultan File Operations Markup Language) Processor")

        self.default_font = tkFont.Font(family="Helvetica", size=14)
        self.text_font = tkFont.Font(family="Consolas", size=11)

        master.option_add("*Font", self.default_font)

        self.input_text_width = 80
        self.input_text_height = 10
        self.log_text_width = 80
        self.log_text_height = 8
        self.results_text_width = 80
        self.results_text_height = 8

        self.project_folder_name = os.path.join(os.getcwd(), "YSFOML_output")
        os.makedirs(self.project_folder_name, exist_ok=True)

        self.log_folder_name = os.path.join(self.project_folder_name, "logs")
        os.makedirs(self.log_folder_name, exist_ok=True)

        # Input Frame
        self.input_frame = tk.LabelFrame(master, text="YSFOML Input", padx=10, pady=10, font=self.default_font)
        self.input_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.input_text = scrolledtext.ScrolledText(self.input_frame, wrap=tk.WORD, width=self.input_text_width, height=self.input_text_height, font=self.text_font)
        self.input_text.pack(fill="both", expand=True)
        self.input_text.insert(tk.END, dummy_content.strip())

        # Folder and Control Frame
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(pady=5, padx=10, fill="x")

        self.folder_label = tk.Label(self.control_frame, text="Project Folder:")
        self.folder_label.pack(side=tk.LEFT, padx=(0, 5))
        self.folder_entry = tk.Entry(self.control_frame, width=40, font=self.default_font)
        self.folder_entry.insert(0, self.project_folder_name)
        self.folder_entry.pack(side=tk.LEFT, padx=5, expand=True, fill="x")
        self.browse_button = tk.Button(self.control_frame, text="Browse Folder", command=self.browse_folder, font=self.default_font)
        self.browse_button.pack(side=tk.LEFT)

        self.load_file_button = tk.Button(self.control_frame, text="Load YSFOML File", command=self.load_ysfoml_file, font=self.default_font)
        self.load_file_button.pack(side=tk.LEFT, padx=(5,0))

        self.process_button = tk.Button(self.control_frame, text="Process YSFOML", command=self.process_content, font=self.default_font)
        self.process_button.pack(side=tk.LEFT, padx=(5,0))

        # Security Level Dropdown
        self.security_level_var = tk.StringVar(master)
        self.security_level_var.set("low") # default value
        security_options = ["low", "medium", "high", "extremelyHigh"]
        self.security_menu_label = tk.Label(self.control_frame, text="Security:")
        self.security_menu_label.pack(side=tk.LEFT, padx=(10, 5))
        self.security_menu = tk.OptionMenu(self.control_frame, self.security_level_var, *security_options)
        self.security_menu.config(font=self.default_font)
        self.security_menu.pack(side=tk.LEFT, padx=(0, 5))


        # Processing Logs Frame
        self.processing_log_frame = tk.LabelFrame(master, text="Processing Logs", padx=10, pady=10, font=self.default_font)
        self.processing_log_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.processing_log_text = scrolledtext.ScrolledText(self.processing_log_frame, wrap=tk.WORD, width=self.log_text_width, height=self.log_text_height, state=tk.DISABLED, font=self.text_font)
        self.processing_log_text.pack(fill="both", expand=True)

        # Operation Results Frame
        self.results_frame = tk.LabelFrame(master, text="Operation Results", padx=10, pady=10, font=self.default_font)
        self.results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.results_text = scrolledtext.ScrolledText(self.results_frame, wrap=tk.WORD, width=self.results_text_width, height=self.results_text_height, state=tk.DISABLED, font=self.text_font)
        self.results_text.pack(fill="both", expand=True)

    def load_ysfoml_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("YSFOML Files", "*.ysfoml"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.config(state=tk.NORMAL)
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, content)
                self.input_text.config(state=tk.NORMAL) # Keep it normal for editing
                self.processing_log_text.config(state=tk.NORMAL)
                self.processing_log_text.delete("1.0", tk.END)
                self.processing_log_text.insert(tk.END, f"Loaded content from: {file_path}\n")
                self.processing_log_text.config(state=tk.DISABLED)
                self.results_text.config(state=tk.NORMAL)
                self.results_text.delete("1.0", tk.END)
                self.results_text.config(state=tk.DISABLED)
            except IOError as e:
                messagebox.showerror("Error", f"Could not read file: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            # Backup the newly selected folder
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_folder_name = f"{os.path.basename(folder_selected)}_backup_{timestamp}"
            parent_dir = os.path.dirname(folder_selected)
            backup_path = os.path.join(parent_dir, backup_folder_name)

            self.processing_log_text.config(state=tk.NORMAL)
            self.processing_log_text.insert(tk.END, f"Attempting to backup selected folder '{folder_selected}'...\n")

            if os.path.exists(folder_selected) and os.path.isdir(folder_selected):
                try:
                    shutil.copytree(folder_selected, backup_path)
                    self.processing_log_text.insert(tk.END, f"Successfully backed up '{folder_selected}' to '{backup_path}'\n")
                except FileExistsError:
                    self.processing_log_text.insert(tk.END, f"Backup folder '{backup_path}' already exists. Skipping backup.\n")
                except shutil.Error as e:
                    self.processing_log_text.insert(tk.END, f"Error backing up folder '{folder_selected}': {e}\n")
                except Exception as e:
                    self.processing_log_text.insert(tk.END, f"An unexpected error occurred during folder backup: {e}\n")
            else:
                self.processing_log_text.insert(tk.END, f"Selected path '{folder_selected}' does not exist or is not a directory. No backup performed.\n")

            self.processing_log_text.config(state=tk.DISABLED)

            self.project_folder_name = folder_selected
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_selected)
            self.log_folder_name = os.path.join(self.project_folder_name, "logs")
            os.makedirs(self.log_folder_name, exist_ok=True)


    def process_content(self):
        full_text_content = self.input_text.get("1.0", tk.END).strip()
        current_security_level = self.security_level_var.get()

        self.processing_log_text.config(state=tk.NORMAL)
        self.processing_log_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)

        self.processing_log_text.insert(tk.END, f"Starting YSFOML processing with security level: '{current_security_level}'\n")

        if not full_text_content:
            self.processing_log_text.insert(tk.END, "Please enter YSFOML content in the input box.\n")
            self.processing_log_text.config(state=tk.DISABLED)
            self.results_text.config(state=tk.DISABLED)
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        input_log_filename = f"input_{timestamp}.txt"
        processing_log_filename = f"processing_log_{timestamp}.txt"
        results_log_filename = f"results_log_{timestamp}.txt"
        input_log_filepath = os.path.join(self.log_folder_name, input_log_filename)
        processing_log_filepath = os.path.join(self.log_folder_name, processing_log_filename)
        results_log_filepath = os.path.join(self.log_folder_name, results_log_filename)

        try:
            with open(input_log_filepath, 'w', encoding='utf-8') as f:
                f.write(full_text_content)
            self.processing_log_text.insert(tk.END, f"Input content saved to: {input_log_filepath}\n\n")
        except IOError as e:
            self.processing_log_text.insert(tk.END, f"Error saving input log file '{input_log_filepath}': {e}\n\n")


        try:
            YSFOML_objects, parse_warnings = parse_YSFOML_string(full_text_content)

            for warning in parse_warnings:
                self.processing_log_text.insert(tk.END, f"PARSE WARNING: {warning}\n")

            if not YSFOML_objects:
                self.processing_log_text.insert(tk.END, "No YSFOML blocks found in the provided content.\n")
            else:
                self.processing_log_text.insert(tk.END, "---------------------- Processing YSFOML Objects --- \n")
                for i, obj in enumerate(YSFOML_objects):
                    self.processing_log_text.insert(tk.END, f"\n--- Object {i+1} ---\n")
                    self.processing_log_text.insert(tk.END, obj.display_info() + "\n")
                    self.processing_log_text.insert(tk.END, "\n")
                    
                    # Process instructions for the current object and check if it was successful
                    if not obj.process_instructions(self.project_folder_name, self.processing_log_text, self.results_text, current_security_level):
                        self.processing_log_text.insert(tk.END, f"\n--- Stopping processing due to error or permission denial in Object {i+1} ---\n")
                        messagebox.showerror("Processing Error", f"An error occurred or permission was denied during processing of Object {i+1}. Processing stopped.")
                        break # Stop the loop if an error occurred or permission was denied
                    
                    self.processing_log_text.insert(tk.END, "\n-----------------------------------\n\n")

        except Exception as e:
            error_message = f"An unexpected error occurred during processing: {e}\n"
            self.processing_log_text.insert(tk.END, error_message)
            messagebox.showerror("Error", error_message)

        finally:
            current_processing_log_content = self.processing_log_text.get("1.0", tk.END).strip()
            try:
                with open(processing_log_filepath, 'w', encoding='utf-8') as f:
                    f.write(current_processing_log_content)
                self.processing_log_text.insert(tk.END, f"\nFull processing log saved to: {processing_log_filepath}\n")
            except IOError as e:
                self.processing_log_text.insert(tk.END, f"\nError saving processing log file '{processing_log_filepath}': {e}\n")

            current_results_content = self.results_text.get("1.0", tk.END).strip()
            try:
                with open(results_log_filepath, 'w', encoding='utf-8') as f:
                    f.write(current_results_content)
                self.processing_log_text.insert(tk.END, f"\nFull results log saved to: {results_log_filepath}\n")
            except IOError as e:
                self.processing_log_text.insert(tk.END, f"\nError saving results log file '{results_log_filepath}': {e}\n")


            self.processing_log_text.config(state=tk.DISABLED)
            self.results_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Missing Dependency",
                             "The 'requests' library is not installed.\n"
                             "Please install it using 'pip install requests' to use all features.")
        root.destroy()
        exit()

    root = tk.Tk()
    app = YSFOML_GUI(root)
    root.mainloop()