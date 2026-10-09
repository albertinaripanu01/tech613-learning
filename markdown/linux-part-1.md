# Linux Part 1

## Introduction

Linux is an open-source operating system kernel. Distributions such as Ubuntu, Debian, and Fedora combine it with tools and applications. The terminal lets you run commands through a shell. Commands and file names are case-sensitive.

## Navigation

| Command | Purpose |
| --- | --- |
| `pwd` | Show the current directory |
| `ls` | List files and directories |
| `ls -la` | Show details and hidden files |
| `cd Documents` | Enter a directory |
| `cd ..` | Move to the parent directory |
| `cd ~` | Go to your home directory |

## The filesystem

- `/`: root directory.
- `/home`: user home directories on many systems.
- `/etc`: system configuration.
- `/var`: changing data, including logs.
- `/tmp`: temporary files.
- `~`: your home directory.

Quote names containing spaces: `cd "My Documents"`.

## Working with files

```bash
mkdir -p ~/linux-practice
cd ~/linux-practice
touch notes.txt
printf "Hello Linux\n" > notes.txt
cat notes.txt
cp notes.txt notes-backup.txt
mv notes-backup.txt backup.txt
```

`>` creates or overwrites a file; `>>` appends text.

## Getting help

Use `man ls` to read the manual or `ls --help` for command options. Press `q` to leave a manual page.

## Practice

1. Create a directory in your home folder.
2. Create a text file and write a sentence.
3. Copy the file and rename the copy.
4. List the files and display their contents.

Continue with [Linux Part 2](linux-part-2.md).
