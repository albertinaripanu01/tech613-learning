# Linux Part 2

Start with [Linux Part 1](linux-part-1.md) if you are new to the terminal.

## Permissions

Run `ls -l` to see file permissions. Permissions are grouped by owner, group, and others.

| Symbol | Meaning |
| --- | --- |
| `r` | Read |
| `w` | Write |
| `x` | Execute a file, or traverse a directory |

Use `chmod u+x hello.sh` to give the owner permission to execute a script. `whoami` shows your username; `id` shows your user and group information.

## Searching text and files

```bash
cd ~/linux-practice
grep -n "Linux" notes.txt
find . -type f -name "*.txt"
wc -l notes.txt
head -n 5 notes.txt
tail -n 5 notes.txt
```

`grep` searches file contents. `find` searches the directory tree. `wc -l` counts newline characters.

## Pipes and redirection

A pipe (`|`) passes one command's output to another command.

```bash
printf "pear\napple\npear\n" | sort | uniq
printf "Another line\n" >> notes.txt
```

`sort` sorts lines, and `uniq` removes adjacent duplicate lines. `>>` appends output; `>` overwrites the destination.

## Processes and disk space

| Command | Purpose |
| --- | --- |
| `ps -ef` | List processes |
| `top` | Watch processes interactively; press `q` to quit |
| `df -h` | Show filesystem space |
| `du -sh .` | Show the current directory's disk usage |

Press `Ctrl+C` to interrupt a command running in the terminal.

## Your first shell script

Save the following as `hello.sh` in your practice directory:

```bash
#!/bin/bash
name="Linux learner"
printf "Hello, %s!\n" "$name"
printf "Current directory: %s\n" "$PWD"
```

Run it using Bash:

```bash
bash hello.sh
```

If Bash is installed at `/bin/bash`, you can also run it directly:

```bash
chmod u+x hello.sh
./hello.sh
```

## Practice

1. Find all `.txt` files in your practice directory.
2. Search your notes for a word and display matching line numbers.
3. Append a new line and check the file with `cat`.
4. Create and run the script above.
5. Check available disk space with `df -h`.
