# *Repo Find Orphans*

This is a small tool that complements Google's `repo` project
repository management tool. The problem it tries to solve is that
developers occasionally add subprojects to the repository without
first registering them in the repo manifest. This is not a recommended
activity in the repo workflow, but it happens frequently in large
teams. These unregistered directories become orphans, which means
the repo tool ignores them during synchronization and updates. This
tool addresses this issue by identifying these orphan directories,
which developers can choose to include in the project manifest for
tracking in the future.


## Installation

There are two ways to install this tool:

1. **Using pip**:   this will install the tool into your active
virtual environment or to the the global python environment.  To
install with pip use the following command

```
   pip install repo-find-orphans
```


2. **Using pipx**: If you want to keep your Python global environment
clean or install Python CLI tools in isolated environments use the
pipx option.

  - First make sure pipx is installed

```
pip install pipx
```

   - Then install the tool

```
pipx install repo-find-orphans
```
This will create a dedicated virtual environment for the tool and add the executable script to your ~/.local/bin


## Usage

After installing *Repo Find Orphans*, use the provided command-line interface to search for orphan directories. Here's how you use the tool:

Open your terminal and enter the following command.

```
repository-find-orphans PATH_TO_MANIFEST PATH_TO_PROJECT_DIR
```

replace `PATH_TO_MANIFEST` with your manifest file's path, which
is usually `repo/default.xml`, and `PATH_TO_PROJECT_DIR` with the
path to your project directory.

For example:

```
repo-find-orphans ./repo/default.xml .
```

This will scan the project directory and will try to find all projects in the project manifest file.  Then it will print the list of projects that exists in the directory,  but not mentioned in the manifest.  You can review this output and add the missing projects to the manifest.


# Troubleshooting

If you installed your tool using pipx, but get the `command not
found` error when you are trying to run it check that `~/.local/bin`
is in your shell search path. If it is not, run `pipx ensurepath`
to fix this
