**Research and test what you've learnt on your cloud VM:**
1. **Why is managing file ownership important?**

   Managing file ownership helps control who can access and modify files and directories. It protects sensitive data and ensures users and services have the access they need.

   In my examples, the files and directories belong to the user `ubuntu` and the group `ubuntu`.
  <img width="820" height="282" alt="image" src="https://github.com/user-attachments/assets/b0fdcc18-f216-4fc8-a9a7-b0db39af7567" />


2. **What is the command to view file ownership?**

   I use `ls -l` to view a file’s ownership and permissions:

   ```bash
   ls -l cat.jpg
   ```

   Output:

   ```text
   -rw-rw-r-- 1 ubuntu ubuntu 71944 Oct 7 17:02 cat.jpg
   ```

   The first `ubuntu` is the owner, and the second `ubuntu` is the group.

   To view the directory itself, I use `ls -ld`:

   ```bash
   ls -ld albertis
   ```

   Output:

   ```text
   drwxrwxr-x 2 ubuntu ubuntu 4096 Oct 12 14:44 albertis
   ```

   When I ran `ls -l albertis`, it showed `total 0` because the directory was empty.

3. **What permissions are set when a user creates a file or directory? Who does file or directory belong to?**

   The permissions depend on the application’s requested permissions and the user’s **umask**. Files typically start with `666`, and directories with `777`, before the umask removes permissions.

   My examples show:

   | Item | Permissions | Owner | Group |
   |---|---|---|---|
   | `cat.jpg` | `664` — `rw-rw-r--` | `ubuntu` | `ubuntu` |
   | `albertis` | `775` — `rwxrwxr-x` | `ubuntu` | `ubuntu` |

   For `cat.jpg`, the owner and group can read and write. Others can only read.

   I created `albertis` with:

   ```bash
   mkdir albertis
   ```

   The owner and group can read, write, and traverse this directory. Others can read and traverse it.

   These permissions are consistent with a umask of `002`. I can check my current umask with:

   ```bash
   umask
   ```

   New files and directories normally belong to the user creating them and the creating process’s effective group. If the parent directory has the setgid bit, they inherit its group.

4. **Why does the owner, by default, not receive X permissions when they create a file?**

   Most files contain data rather than executable programs, so ordinary file creation does not request execute (`x`) permission. The umask can remove permissions but cannot add them.

   My `cat.jpg` file has `rw-rw-r--`, so nobody has execute permission. It only needs read permission to be viewed.

   Directories normally have `x` permission because it allows users to traverse them and access entries inside.

   To give myself execute permission as the owner of a script, I can use:

   ```bash
   chmod u+x install-nginx.sh
   ```

5. **What command is used to change the owner of a file or directory?**

   I use `chown` to change ownership. Changing the owner normally requires administrator privileges, so I use `sudo`.

   For example, if a user called `alice` exists:

   ```bash
   # Change the file owner
   sudo chown alice cat.jpg

   # Change the directory owner
   sudo chown alice albertis

   # Change both the owner and group
   sudo chown alice:ubuntu cat.jpg
   ```

   I can check the ownership afterwards with:

   ```bash
   ls -l cat.jpg
   ls -ld albertis
   ```


