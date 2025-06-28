# YSFOML (Yasir Sultan File Operations Markup Language) Specification and Documentation, Version 1.0.0

## Table of Contents
1.  [Introduction](#1-introduction)
2.  [Core Concepts](#2-core-concepts)
    *   [2.1 YSFOML Block Structure](#21-ysfoml-block-structure)
    *   [2.2 Parameters](#22-parameters)
    *   [2.3 Base Folder](#23-base-folder)
    *   [2.4 Security Levels](#24-security-levels)
    *   [2.5 User-Defined Actions (`actionSource: userAdded`)](#25-user-defined-actions-actionsource-useradded)
3.  [Language Specification (Detailed Action Reference)](#3-language-specification-detailed-action-reference)
    *   [3.1 `action:create`](#31-actioncreate)
    *   [3.2 `action:append`](#32-actionappend)
    *   [3.3 `action:delete`](#33-actiondelete)
    *   [3.4 `action:createFolder`](#34-actioncreatefolder)
    *   [3.5 `action:deleteFolder`](#35-actiondeletefolder)
    *   [3.6 `action:rename`](#36-actionrename)
    *   [3.7 `action:move`](#37-actionmove)
    *   [3.8 `action:treeFolders`](#38-actiontreefolders)
    *   [3.9 `action:treeFiles`](#39-actiontreefiles)
    *   [3.10 `action:findFile`](#310-actionfindfile)
    *   [3.11 `action:findInFile`](#311-actionfindinfile)
    *   [3.12 `action:replaceInFile`](#312-actionreplaceinfile)
    *   [3.13 `action:readFileAll`](#313-actionreadfileall)
    *   [3.14 `action:readFileLines`](#314-actionreadfilelines)
    *   [3.15 `action:insertAt`](#315-actioninsertat)
    *   [3.16 `action:treeFoldersJSON`](#316-actiontreefoldersjson)
    *   [3.17 `action:treeFilesJSON`](#317-actiontreefilesjson)
4.  [Using the YSFOML Parser Application](#4-using-the-ysfoml-parser-application)
    *   [4.1 Requirements](#41-requirements)
    *   [4.2 Running the Application](#42-running-the-application)
    *   [4.3 Application Interface](#43-application-interface)
    *   [4.4 Workflow](#44-workflow)
    *   [4.5 Logging](#45-logging)
5.  [Error Handling and Best Practices](#5-error-handling-and-best-practices)
    *   [5.1 Error Handling](#51-error-handling)
    *   [5.2 Backup Mechanism](#52-backup-mechanism)
    *   [5.3 Best Practices](#53-best-practices)
6.  [Limitations](#6-limitations)
7.  [Disclaimer](#7-disclaimer)
8.  [YSFOML and Artificial Intelligence](#8-ysfoml-and-artificial-intelligence)
    *   [8.1 AI Workflow for Project Understanding and Modification](#81-ai-workflow-for-project-understanding-and-modification)

---

## 1. Introduction
YSFOML (Yasir Sultan File Operations Markup Language) is a simple, human-readable markup language designed for defining and executing a series of file system operations. It allows users to specify actions such as creating, appending, deleting, renaming, moving files and folders, as well as performing content-based operations like searching, replacing, and reading file contents. YSFOML is processed by a dedicated parser application that interprets the defined actions and executes them on the local file system.

YSFOML is free to use, and you are encouraged to create applications that utilize it. When doing so, please ensure that "YSFOML (Yasir Sultan File Operations Markup Language)" is mentioned without alteration.

## 2. Core Concepts

### 2.1 YSFOML Block Structure
YSFOML operations are defined within `<YSFOML>` and `</YSFOML>` tags. Each block represents a single file system operation.

**Syntax:**
```
<YSFOML>
action: [action_name];
[parameter1]:[value1];
[parameter2]:[value2]
...
</YSFOML>
[Optional Content associated with the action]
```
*   **`<YSFOML>` and `</YSFOML>`:** These tags delimit an YSFOML instruction block.
*   **Instructions:** Inside the tags, instructions are provided as `key:value;` pairs, with each instruction typically ending with a semicolon. The `action` key is mandatory and specifies the operation to be performed.
*   **Content:** The text immediately following the `</YSFOML>` closing tag (until the next `<YSFOML>` tag or end of document) is considered the "content" associated with that specific YSFOML block. This content is used by certain actions (e.g., `create`, `append`, `insertAt`).

### 2.2 Parameters
Parameters are key-value pairs within the YSFOML block that provide specific details for the action.

**General Syntax:** `parameter_name:parameter_value;`
*   **`parameter_name`**: The name of the parameter (e.g., `filename`, `foldername`, `searchString`).
*   **`parameter_value`**: The value for the parameter. This can be a file path, folder name, string, URL, line number, column number, etc.
*   **Semicolon (`;`)**: Each parameter definition should end with a semicolon.

### 2.3 Base Folder
All file system operations performed by the YSFOML parser are relative to a designated "base folder" (referred to as `project_folder_name` in the provided Python parser). If a file or folder path is specified without a leading slash (e.g., `file1.txt`, `my_new_folder/nested_file.txt`), it is assumed to be relative to this base folder.

### 2.4 Security Levels
YSFOML operations are categorized by security levels to indicate the potential impact on the file system. The YSFOML parser application may use these levels to enforce permissions or require higher user confirmation for more impactful operations.
*   `low`: Read-only operations that inspect the file system without making changes (e.g., listing files, searching content).
*   `medium`: Operations that create, modify, or move files/folders without permanent deletion (e.g., creating files, appending content, renaming). These operations often include backup mechanisms.
*   `high`: Operations that permanently delete files or folders. These are considered highly destructive and irreversible.
*   `extremelyHigh`: (Future/Reserved) Operations that could involve arbitrary code execution or significant system-wide changes. Currently, no YSFOML actions support this level, and external scripting is explicitly not supported.

### 2.5 User-Defined Actions (`actionSource: userAdded`)
While YSFOML provides a comprehensive set of built-in actions, future versions may allow for the definition of new, custom actions. If you are defining a new action that is not part of the standard YSFOML specification, you *must* include the `actionSource: userAdded;` parameter within the YSFOML block. This parameter signals to the parser that the action is a custom, user-defined one. Current YSFOML processors may log these actions as unsupported, but this mechanism is in place for future extensibility.

**Example for a hypothetical user-added action:**
```
<YSFOML>
action:myCustomAction;
actionSource:userAdded;
param1:value1;
param2:value2
</YSFOML>
This is content for my custom action.
```

## 3. Language Specification (Detailed Action Reference)
This section details each supported YSFOML action, its purpose, parameters, content usage, and behavior.

### 3.1 `action:create`
*   **Purpose:** Creates a new file or overwrites an existing one with the provided content.
*   **Parameters:**
    *   `filename`: (Required, String) The path and name of the file to create, relative to the base folder.
*   **Security Level:** `medium`
*   **Content:** The text content to write into the file.
*   **Behavior:**
    *   If the file already exists, it will be backed up (renamed with a timestamp) before being overwritten.
    *   Automatically creates parent directories if they do not exist.
*   **Example:**
    ```
    <YSFOML>
    action:create;
    filename:file1.txt
    </YSFOML>
    hey,
    this is the first file1
    by Yasir Sultan
    ```

### 3.2 `action:append`
*   **Purpose:** Appends content to an existing file. If the file does not exist, it will be created.
*   **Parameters:**
    *   `filename`: (Required, String) The path and name of the file to append to, relative to the base folder.
*   **Security Level:** `medium`
*   **Content:** The text content to append to the file.
*   **Behavior:**
    *   If the file already exists, a copy of the original file (with a timestamp) is created as a backup before appending.
    *   Automatically creates parent directories if they do not exist.
*   **Example:**
    ```
    <YSFOML>
    action:append;
    filename:file2.txt
    </YSFOML>


    hey,
    this is the second file
    developed by Yasir Sultan
    -- Appended content --
    ```

### 3.3 `action:delete`
*   **Purpose:** Deletes a specified file.
*   **Parameters:**
    *   `filename`: (Required, String) The path and name of the file to delete, relative to the base folder.
*   **Security Level:** `high`
*   **Content:** Not used.
*   **Behavior:**
    *   Logs an error if the file does not exist or if it's a directory.
*   **Example:**
    ```
    <YSFOML>
    action:delete;
    filename:renamed_file1.txt
    </YSFOML>
    ```

### 3.4 `action:createFolder`
*   **Purpose:** Creates a new directory (folder).
*   **Parameters:**
    *   `foldername`: (Required, String) The path and name of the folder to create, relative to the base folder.
*   **Security Level:** `medium`
*   **Content:** Not used.
*   **Behavior:**
    *   Creates all necessary parent directories.
    *   If the folder already exists, no action is taken, and it's noted as already existing.
*   **Example:**
    ```
    <YSFOML>
    action:createFolder;
    foldername:my_new_folder
    </YSFOML>
    ```

### 3.5 `action:deleteFolder`
*   **Purpose:** Deletes a specified directory and all its contents (files and subfolders).
*   **Parameters:**
    *   `foldername`: (Required, String) The path and name of the folder to delete, relative to the base folder.
*   **Security Level:** `high`
*   **Content:** Not used.
*   **Behavior:**
    *   Logs an error if the folder does not exist or if it's a file.
    *   This operation is recursive and irreversible.
*   **Example:**
    ```
    <YSFOML>
    action:deleteFolder;
    foldername:my_new_folder
    </YSFOML>
    ```

### 3.6 `action:rename`
*   **Purpose:** Renames a file.
*   **Parameters:**
    *   `filename`: (Required, String) The current path and name of the file to rename, relative to the base folder.
    *   `filename2`: (Required, String) The new path and name for the file, relative to the base folder.
*   **Security Level:** `medium`
*   **Content:** Not used.
*   **Behavior:**
    *   Logs an error if the original file does not exist.
    *   Logs an error if the new filename already exists.
    *   This action only renames within the same directory; for moving to a different directory, use `action:move`.
*   **Example:**
    ```
    <YSFOML>
    action:rename;
    filename:file1.txt;
    filename2:renamed_file1.txt
    </YSFOML>
    ```

### 3.7 `action:move`
*   **Purpose:** Moves a file from one location to another.
*   **Parameters:**
    *   `filepath1`: (Required, String) The current path and name of the file to move, relative to the base folder.
    *   `filepath2`: (Required, String) The destination path and new name for the file, relative to the base folder.
*   **Security Level:** `medium`
*   **Content:** Not used.
*   **Behavior:**
    *   Logs an error if the source file does not exist.
    *   Automatically creates the destination directory if it does not exist.
    *   If the destination file already exists, it will be overwritten.
*   **Example:**
    ```
    <YSFOML>
    action:move;
    filepath1:file2.txt;
    filepath2:my_new_folder/moved_file2.txt
    </YSFOML>
    ```

### 3.8 `action:treeFolders`
*   **Purpose:** Displays the directory structure (folders only) starting from a specified folder.
*   **Parameters:**
    *   `foldername`: (Optional, String) The folder from which to start the tree display, relative to the base folder. If omitted, the base folder itself is used.
*   **Security Level:** `low`
*   **Content:** Not used.
*   **Behavior:**
    *   Outputs the folder tree to the "Operation Results" panel.
    *   Does not list individual files.
*   **Example:**
    ```
    <YSFOML>
    action:treeFolders;
    foldername:my_new_folder
    </YSFOML>
    ```

### 3.9 `action:treeFiles`
*   **Purpose:** Displays the full directory and file structure starting from a specified folder.
*   **Parameters:**
    *   `foldername`: (Optional, String) The folder from which to start the tree display, relative to the base folder. If omitted, the base folder itself is used.
*   **Security Level:** `low`
*   **Content:** Not used.
*   **Behavior:**
    *   Outputs the full file and folder tree to the "Operation Results" panel.
*   **Example:**
    ```
    <YSFOML>
    action:treeFiles;
    foldername:
    </YSFOML>
    ```

### 3.10 `action:findFile`
*   **Purpose:** Searches for a specific file by name within a given folder and its subfolders.
*   **Parameters:**
    *   `filename`: (Required, String) The name of the file to search for.
    *   `foldername`: (Optional, String) The folder to start the search from, relative to the base folder. If omitted, the base folder itself is used.
*   **Security Level:** `low`
*   **Content:** Not used.
*   **Behavior:**
    *   Outputs the full paths of all found instances of the file to the "Operation Results" panel.
*   **Example:**
    ```
    <YSFOML>
    action:findFile;
    filename:renamed_file1.txt;
    foldername:
    </YSFOML>
    ```

### 3.11 `action:findInFile`
*   **Purpose:** Searches for occurrences of a specific string within a file.
*   **Parameters:**
    *   `filename`: (Required, String) The path and name of the file to search within, relative to the base folder.
    *   `searchString`: (Required, String) The string to search for.
*   **Security Level:** `low`
*   **Content:** Not used.
*   **Behavior:**
    *   Outputs the line number and column number for each occurrence of the `searchString` to the "Operation Results" panel.
*   **Example:**
    ```
    <YSFOML>
    action:findInFile;
    filename:daily_report.txt;
    searchString:sales
    </YSFOML>
    ```

### 3.12 `action:replaceInFile`
*   **Purpose:** Replaces all occurrences of a `searchString` with a `newString` within a specified file.
*   **Parameters:**
    *   `filename`: (Required, String) The path and name of the file to modify, relative to the base folder.
    *   `searchString`: (Required, String) The string to find and replace.
    *   `newString`: (Required, String) The string to replace `searchString` with. Can be an empty string to delete occurrences.
*   **Security Level:** `medium`
*   **Content:** Not used.
*   **Behavior:**
    *   A copy of the original file (with a timestamp) is created as a backup before modification.
    *   If `searchString` is not found, no changes are made to the file, and a message is logged.
*   **Example:**
    ```
    <YSFOML>
    action:replaceInFile;
    filename:daily_report.txt;
    searchString:$;
    newString:USD
    </YSFOML>
    ```

### 3.13 `action:readFileAll`
*   **Purpose:** Reads and displays the entire content of a specified file.
*   **Parameters:**
    *   `filename`: (Required, String) The path and name of the file to read, relative to the base folder.
*   **Security Level:** `low`
*   **Content:** Not used.
*   **Behavior:**
    *   Outputs the full content of the file to the "Operation Results" panel.
*   **Example:**
    ```
    <YSFOML>
    action:readFileAll;
    filename:daily_report.txt
    </YSFOML>
    ```

### 3.14 `action:readFileLines`
*   **Purpose:** Reads and displays specific lines from a file.
*   **Parameters:**
    *   `filename`: (Required, String) The path and name of the file to read, relative to the base folder.
    *   `startLine`: (Optional, Integer) The starting line number (1-indexed). Defaults to 1.
    *   `endLine`: (Optional, Integer) The ending line number (1-indexed). Defaults to the last line of the file if omitted or set to -1.
*   **Security Level:** `low`
*   **Content:** Not used.
*   **Behavior:**
    *   Outputs the specified range of lines to the "Operation Results" panel, prefixed with their line numbers.
    *   If `startLine` is out of bounds, an error is logged.
*   **Example:**
    ```
    <YSFOML>
    action:readFileLines;
    filename:daily_report.txt;
    startLine:2;
    endLine:3
    </YSFOML>
    ```

### 3.15 `action:insertAt`
*   **Purpose:** Inserts text content at a specific line and column within a file.
*   **Parameters:**
    *   `filename`: (Required, String) The path and name of the file to modify, relative to the base folder.
    *   `lineNum`: (Required, Integer) The 1-indexed line number where the text should be inserted.
    *   `colNum`: (Required, Integer) The 1-indexed column number within the specified line where the text should be inserted.
*   **Security Level:** `medium`
*   **Content:** The text content to insert into the file.
*   **Behavior:**
    *   A copy of the original file (with a timestamp) is created as a backup before modification.
    *   If `lineNum` is out of bounds, an error is logged.
    *   If `colNum` is greater than the length of the line, the text is appended to the end of that line.
*   **Example:**
    ```    <YSFOML>
    action:insertAt;
    filename:daily_report.txt;
    lineNum:1;
    colNum:1
    </YSFOML>
    --- START OF REPORT ---
    ```

### 3.16 `action:treeFoldersJSON`
*   **Purpose:** Generates a machine-readable JSON representation of the directory structure (folders only) starting from a specified folder. This action is primarily intended for AI models to programmatically understand the project's folder layout.
*   **Parameters:**
    *   `foldername`: (Optional, String) The folder from which to start the tree generation, relative to the base folder. If omitted, the base folder itself is used.
*   **Security Level:** `low`
*   **Content:** Not used.
*   **Behavior:**
    *   Outputs a JSON object representing the folder tree to the "Operation Results" panel.
    *   Each folder is represented with its name, type ("directory"), relative path, and a list of its contents (sub-folders).
    *   Does not list individual files.
*   **Example:**
    ```
    <YSFOML>
    action:treeFoldersJSON;
    foldername:my_new_folder
    </YSFOML>
    ```

### 3.17 `action:treeFilesJSON`
*   **Purpose:** Generates a machine-readable JSON representation of the full directory and file structure starting from a specified folder. This action is primarily intended for AI models to programmatically understand the complete project structure, including files.
*   **Parameters:**
    *   `foldername`: (Optional, String) The folder from which to start the tree generation, relative to the base folder. If omitted, the base folder itself is used.
*   **Security Level:** `low`
*   **Content:** Not used.
*   **Behavior:**
    *   Outputs a JSON object representing the full file and folder tree to the "Operation Results" panel.
    *   Each item (folder or file) is represented with its name, type ("directory" or "file"), and relative path. Folders also include a list of their contents.
*   **Example:**
    ```
    <YSFOML>
    action:treeFilesJSON;
    foldername:
    </YSFOML>
    ```

## 4. Using the YSFOML Parser Application
The provided Python script `YSFOML_GUI` acts as a parser and executor for YSFOML documents.

### 4.1 Requirements
*   Python 3.x
*   `tkinter` (usually included with Python)
*   `requests` library (`pip install requests`)
*   For `action:json` with `jsonPath`, a JSONPath library might be required (e.g., `pip install jsonpath-ng`).

### 4.2 Running the Application
1.  Save the provided Python code as a `.py` file (e.g., `ysfoml_parser.py`).
2.  Run it from your terminal: `python ysfoml_parser.py`

### 4.3 Application Interface
The GUI provides the following main components:
*   **YSFOML Input:** A text area where you paste or type your YSFOML document.
*   **Project Folder:** An entry field and a "Browse" button to select the base directory where all file operations will be performed. By default, it creates an `YSFOML_output` folder in the current working directory.
*   **Process YSFOML Button:** Initiates the parsing and execution of the YSFOML content.
*   **Processing Logs:** Displays detailed logs of each step, including warnings, errors, and success messages for file operations.
*   **Operation Results:** Displays the output of query-based operations like `treeFolders`, `findFile`, `readFileAll`, etc.
*   **Security Level Dropdown:** Allows the user to select a security level (low, medium, high, extremelyHigh) that will restrict which YSFOML actions can be executed.

### 4.4 Workflow
1.  **Prepare YSFOML:** Write or paste your YSFOML instructions into the "YSFOML Input" text area.
2.  **Select Base Folder:** Choose or confirm the "Project Folder" where the operations will take place.
3.  **Select Security Level:** Choose the appropriate security level from the dropdown. Operations requiring a higher security level than selected will be blocked.
4.  **Process:** Click "Process YSFOML".
5.  **Review Output:** Check the "Processing Logs" for the status of each operation and the "Operation Results" for the output of query actions.
6.  **Check File System:** Verify the changes in your chosen "Project Folder".

### 4.5 Logging
The parser automatically saves three log files for each processing run within a `logs` subfolder inside your chosen project folder:
*   `input_[timestamp].txt`: A copy of the YSFOML content that was processed.
*   `processing_log_[timestamp].txt`: The full content of the "Processing Logs" panel.
*   `results_log_[timestamp].txt`: The full content of the "Operation Results" panel.

## 5. Error Handling and Best Practices

### 5.1 Error Handling
*   The parser attempts to log descriptive error messages to the "Processing Logs" panel for failed operations (e.g., file not found, permission errors, invalid parameters).
*   Syntax errors within the `key:value;` pairs might lead to parameters not being correctly parsed, resulting in "Warning: No 'key' found" messages.
*   Missing closing `</YSFOML>` tags will result in warnings and incomplete parsing.
*   For critical errors (e.g., missing Python libraries), a `tkinter.messagebox` will appear.
*   Operations that fail due to insufficient security levels will be logged and prevented from executing.

### 5.2 Backup Mechanism
*   For `create`, `append`, `replaceInFile`, and `action:json` (write mode) operations, the parser creates a timestamped backup of the original file before modification. This is a crucial safety feature to prevent accidental data loss. Backups are stored in the same directory as the original file.

### 5.3 Best Practices
*   **Test on Dummy Data:** Always test your YSFOML scripts on a non-critical "Project Folder" or with dummy files first, especially for destructive operations like `delete` or `deleteFolder`.
*   **Clear Paths:** Use clear and consistent relative paths for filenames and foldernames.
*   **Review Logs:** Always review the "Processing Logs" after execution to ensure all operations completed as expected and to identify any warnings or errors.
*   **One Action Per Block:** Adhere to the "one action per YSFOML block" principle for clarity and proper parsing.
*   **Semicolons:** Remember to end each parameter definition with a semicolon.
*   **Content Placement:** Ensure the content associated with an action immediately follows its `</YSFOML>` tag.

## 6. Limitations
*   **No Conditional Logic:** YSFOML currently does not support conditional statements (if/else) or loops. Operations are executed sequentially as they appear in the document.
*   **No Variables:** There is no support for defining and using variables within YSFOML.
*   **No External Scripting:** YSFOML cannot directly execute external scripts or commands.
*   **Single File Processing:** The parser processes the entire input as a single YSFOML document.
*   **Platform Dependent Paths:** While `os.path.join` is used for path construction, complex path manipulations or platform-specific characters might behave unexpectedly.
*   **No Undo Feature:** Operations are permanent on the file system (except for the automatic backups for certain actions). There is no built-in "undo" functionality for the sequence of operations.

## 7. Disclaimer
YSFOML (Yasir Sultan File Operations Markup Language) and the YSFOML Processor application are currently under development. They are provided "as is" without warranty of any kind, either express or implied. Use at your own risk. The developer is not responsible for any data loss or other damages incurred from the use of this software.

## 8. YSFOML and Artificial Intelligence
YSFOML is designed with Artificial Intelligence (AI) interaction in mind, serving as a structured and human-readable language for AI models to specify file system operations. This allows AI to communicate desired file manipulations in a clear, auditable format.

A core principle of YSFOML's design, especially when used with AI, is the "human-in-the-loop" security model. AI models can generate YSFOML instructions based on user requests (e.g., "Please create a Python script and save it as 'hello.py'"). However, the execution of these instructions is intentionally manual: the AI provides the YSFOML text, and the user must then copy and paste this text into the YSFOML Parser application. This manual step acts as a critical security layer, preventing direct, unsupervised AI access to your local file system.

By generating YSFOML instructions, AI can help users understand, create, and edit code, manage project files, or perform other file-related tasks. This approach empowers users with AI assistance while maintaining ultimate control and oversight over their file system.

It is crucial to understand that the execution of any YSFOML instructions, whether generated by an AI or written manually, is entirely at the user's own risk. Users are strongly advised to always review the generated YSFOML content carefully before processing it with the YSFOML Parser, especially for actions with `medium` or `high` security levels that can modify or delete files.

### 8.1 AI Workflow for Project Understanding and Modification
For an AI to effectively assist with file system operations, especially in complex projects, it's essential for the AI to first gain an understanding of the project's structure and existing content. The `action:treeFoldersJSON` and `action:treeFilesJSON` actions are specifically designed for this purpose.
*   **Initial Project Overview:** An AI should begin by requesting a JSON representation of the project's folder or file tree using `action:treeFoldersJSON` (for a high-level folder structure) or `action:treeFilesJSON` (for a detailed view including all files). This provides the AI with a structured, machine-readable map of the project.
*   **Content Analysis:** Once the AI has the project structure, it can then identify relevant files (e.g., source code, configuration files, data files). For specific files, the AI can then use `action:readFileAll` or `action:readFileLines` to read their content and understand their purpose or identify areas for modification.
*   **Generating Modification Instructions:** With a clear understanding of the project structure and file contents, the AI can then generate precise YSFOML instructions for operations like `action:create`, `action:append`, `action:replaceInFile`, or `action:insertAt` to make the desired changes. This iterative process of "read-then-write" ensures that AI-generated modifications are contextually aware and accurate.

This structured approach allows the AI to provide more intelligent and targeted assistance, while the human-in-the-loop model ensures safety and oversight.
