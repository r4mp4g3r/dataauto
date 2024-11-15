# Installation Guide

This guide will walk you through the steps to install and set up **DataAuto** on your machine.

## Prerequisites

Before installing DataAuto, ensure you have the following installed:

- **Python 3.6+**: DataAuto requires Python version 3.6 or higher.
- **pip**: Python's package installer should be available.

You can verify your Python and pip installations by running:

```bash
python --version
pip --version
```

If you don’t have Python installed, download it from the official website.

## Installation Methods

1. Installing via PyPI

DataAuto is available on PyPI, making installation straightforward.

```bash
pip install dataauto
```

Advantages:
 • Quick Setup: Install DataAuto with a single command.
 • Automatic Dependency Management: pip handles all required dependencies.

Steps:
 1. Open Your Terminal or Command Prompt.
 2. Run the Installation Command:

```bash
pip install dataauto
```

 3. Verify the Installation:

```bash
dataauto --version
```

Expected Output:
```bash
DataAuto version 0.1.0
```

2. Installing from Source

If you prefer to install DataAuto from the source code (useful for development or contribution), follow these steps.

a. Clone the Repository

```bash
git clone https://github.com/yourusername/dataauto.git
cd dataauto
```

 Note: Replace yourusername with your actual GitHub username.

b. Create a Virtual Environment (Optional but Recommended)

Creating a virtual environment helps manage dependencies and avoid conflicts with other Python projects.

```bash
python -m venv venv
```
 • Activate the Virtual Environment:
 • On macOS/Linux:
```bash
source venv/bin/activate
```

 • On Windows:
```bash
venv\Scripts\activate
```


c. Install Dependencies
```bash
pip install -r requirements.txt
```
 Note: If you encounter issues with pip not finding requirements.txt, ensure you’re in the root directory of the cloned repository.

d. Install the Package in Editable Mode

Installing in editable mode allows you to make changes to the source code and have them reflected without reinstalling the package.

```bash
pip install -e .
```
e. Verify the Installation
```bash
dataauto --version
```
Expected Output:
```bash
DataAuto version 0.1.0
```
3. Additional Installation Options (Optional)

a. Installing via GitHub Releases

If you prefer downloading pre-built packages from GitHub Releases:
 1. Navigate to the DataAuto Releases Page.
 2. Download the Latest Release (e.g., dataauto-0.1.0-py3-none-any.whl).
 3. Install the Wheel File:
```bash
pip install path/to/dataauto-0.1.0-py3-none-any.whl
```

4. Handling Installation Issues

If you encounter issues during installation, consider the following troubleshooting steps:

a. Upgrade pip

An outdated pip can cause installation problems.
```bash
pip install --upgrade pip
```
b. Check Python Version

Ensure you’re using Python 3.6 or higher.
```bash
python --version
```
c. Resolve Dependency Conflicts

If there are conflicts with existing packages, consider using a fresh virtual environment.
```bash
python -m venv new_env
source new_env/bin/activate  # On Windows: new_env\Scripts\activate
pip install -r requirements.txt
pip install -e .
```
d. Permission Issues

If you encounter permission errors, try installing with the --user flag or using sudo (on Unix-based systems).
 • Using --user:
```bash
pip install --user dataauto
```

 • Using sudo:
```bash
sudo pip install dataauto
```
 ⚠️ Warning: Using sudo can affect system-wide packages. It’s generally safer to use virtual environments.

e. Verify Environment Activation

Ensure your virtual environment is activated before installing or running DataAuto.

# On macOS/Linux
```bash
source venv/bin/activate
```
# On Windows
```bash
venv\Scripts\activate
```
## Troubleshooting Common Issues

1. command not found: dataauto

Cause: The installation might not have added the DataAuto executable to your PATH.

Solution:
 • Ensure that the Scripts (Windows) or bin (macOS/Linux) directory of your Python installation is in your system’s PATH.
 • If using a virtual environment, ensure it’s activated.

2. Missing Dependencies

Cause: Required packages might not be installed.

Solution:
 • Reinstall dependencies:
```bash
pip install -r requirements.txt
```
 • Ensure you’re installing in the correct environment (virtual environment vs. global).

3. Permission Denied Errors

Cause: Insufficient permissions to install packages.

Solution:
 • Use the --user flag:
```bash
pip install --user dataauto
```
 • Or activate a virtual environment.

4. Broken Installation

Cause: Installation was interrupted or corrupted.

Solution:
 • Uninstall and reinstall DataAuto:
```bash
pip uninstall dataauto
pip install dataauto
```

## Final Notes

After following the installation steps, you should have DataAuto set up and ready to use on your machine. If you continue to experience issues, consider reaching out through the GitHub Issues page for further assistance.

Feel free to explore the Usage Guide and Tutorials to start leveraging DataAuto for your data analysis tasks!