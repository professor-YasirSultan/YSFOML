# YSFOML (Yasir Sultan File Operations Markup Language)

**Streamlining File System Operations with AI-Driven Automation**

YSFOML (Yasir Sultan File Operations Markup Language) is a powerful and intuitive markup language designed to automate and simplify file system operations. It provides a structured, human-readable way to define a series of file-related tasks, bridging the gap between human intent and automated file management. [1]

## Why YSFOML?

YSFOML is meticulously crafted to empower programmers by facilitating seamless interaction with Artificial Intelligence for file system management. Its core design principle incorporates a robust "human-in-the-loop" security model, ensuring that AI models can leverage powerful automation capabilities without compromising data security or executing malicious behaviors. [1, 5]

## Key Features

*   **Structured Operations**: Define file system tasks using a clear, block-based syntax (`<YSFOML>...</YSFOML>`). [2.1]
*   **Comprehensive Action Set**: Perform a wide range of operations including creating, appending, deleting, renaming, moving files and folders, searching content, and reading file data. [3]
*   **Security Levels**: Operations are categorized by security levels (low, medium, high, extremelyHigh) to indicate potential impact and enforce permissions, requiring higher user confirmation for critical actions. [2.4]
*   **AI-First Design**: Specifically designed for AI models to understand, query, and propose modifications to file systems in a structured and auditable format. Actions like `treeFoldersJSON` and `treeFilesJSON` enable AI to gain project context. [5, 5.1, 5.2]
*   **Human-in-the-Loop Security**: AI-generated YSFOML instructions require manual review and execution by the user, providing a critical security layer against unsupervised AI access. [5]
*   **Backup Mechanisms**: Automatic backups are created for modifying operations (e.g., `create`, `append`, `replaceInFile`) to prevent accidental data loss. [9.2]

## Getting Started

To use YSFOML, you'll interact with the YSFOML Parser Application, a Python-based GUI tool (`YSFOML_GUI`). [7]

### Requirements

*   Python 3.x [7.1]
*   `tkinter` (usually included with Python) [7.1]
*   `requests` library (`pip install requests`) [7.1]
*   Optionally, `jsonpath-ng` for `action:json` with `jsonPath` (`pip install jsonpath-ng`). [7.1]

### Workflow

1.  **Prepare YSFOML**: Write or paste your YSFOML instructions into the "YSFOML Input" area of the GUI. [7.4]
2.  **Select Base Folder**: Choose the project directory where operations will take place. [7.4]
3.  **Select Security Level**: Set the appropriate security level; operations requiring a higher level than selected will be blocked. [7.4]
4.  **Process**: Click "Process YSFOML" to execute. [7.4]
5.  **Review Output**: Check "Processing Logs" and "Operation Results" for feedback. [7.4]

## Future Aspects

YSFOML is continuously evolving to offer even more powerful capabilities:

*   **Multi-Client Protocol (MCP) Integration**: Future integration of the MCP protocol within the YSFOML parser application will enable seamless review and approval of YSFOML code directly within a rich GUI environment, largely eliminating manual copy-pasting. [4]
*   **Variables & Conditional Logic**: Planned introduction of variables and conditional statements will allow for more dynamic and intelligent file operation sequences. [4]
*   **Secure Script Execution**: New actions like `executeScript` and `compileCode` will be introduced, classified under the `extremelyHigh` security level, mandating explicit human review and potentially incorporating sandboxing capabilities for maximum security. [4]

## Documentation

For a detailed specification of all YSFOML actions, core concepts, and advanced usage, please refer to our comprehensive documentation:

[YSFOML (Yasir Sultan File Operations Markup Language) Specification and Documentation, Version 1.0.6](https://professor-yasirsultan.github.io/YSFOML/)

## Explore YSFOML with AI

Interact with our dedicated YSFOML AI Bot, a programming language expert leveraging the power of YSFOML:

[Our YSFOML AI Bot at Poe](https://poe.com/YSFOML_expert)

## Connect with Professor Yasir Sultan

Stay updated with the latest developments and tutorials:

[Professor Yasir Sultan's YouTube Channel](https://www.youtube.com/@prof.yasir.sultan?sub_confirmation=1)

## Contributing & Support

YSFOML is currently under active development. We welcome feedback and contributions. Please note that YSFOML and its processor are provided "as is" and used at your own risk. [10, 13]
