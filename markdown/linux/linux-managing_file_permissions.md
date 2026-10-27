**Research and test what you've learnt on your cloud VM:**
| Permissions | Numeric mode | Type | Owner | Group | Others |
| --- | --- | --- | --- | --- | --- |
| `-rwxr-xr--` | `754` | File | `rwx` | `r-x` | `r--` |
| `-rw-r--r--` | `644` | File | `rw-` | `r--` | `r--` |
| `-rw-------` | `600` | File | `rw-` | `---` | `---` |
| `-r--------` | `400` | File | `r--` | `---` | `---` |
| `-rwx------` | `700` | File | `rwx` | `---` | `---` |
| `-rwxr-xr-x` | `755` | File | `rwx` | `r-x` | `r-x` |
| `-rw-rw-r--` | `664` | File | `rw-` | `rw-` | `r--` |
| `-rwxrwxrwx` | `777` | File | `rwx` | `rwx` | `rwx` |
| `drwxr-xr-x` | `755` | Directory | `rwx` | `r-x` | `r-x` |
| `drwx------` | `700` | Directory | `rwx` | `---` | `---` |

- `-` at the start means a regular file; `d` means a directory.
- `r` = read, `w` = write, `x` = execute a file or enter/traverse a directory.
- `-` within a permission group means that permission is absent.
1. **Does being the owner of a file mean you have full permissions on that file? Explain.**

   No. The owner's access depends on the User permission bits: read (`r`), write (`w`), and execute (`x`). The owner can normally change these permissions with `chmod`, even if they currently have read-only access.

   ![File ownership and permissions example](https://github.com/user-attachments/assets/7748705e-add4-4494-8cbf-c496f9d62455)

   **Practice exercise**

   Run these commands as your normal user, without `sudo`.

   **Create a practice file:**

   ```text
   echo "Original text" > ownership-practice.txt
   ```

   **Check its owner and permissions:**

   ```text
   ls -l ownership-practice.txt
   whoami
   ```

   **Give the owner read-only permission:**

   ```text
   chmod 400 ownership-practice.txt
   ```

   **Reading works:**

   ```text
   cat ownership-practice.txt
   ```

   **Writing fails with “Permission denied”:**

   ```text
   echo "New text" >> ownership-practice.txt
   ```

   **As the owner, restore write permission:**

   ```text
   chmod u+w ownership-practice.txt
   ```

   **Writing now works:**

   ```text
   echo "New text" >> ownership-practice.txt
   cat ownership-practice.txt
   ```
2. **If you give permissions to the User entity, what does this mean?**

   These permissions apply to the file's owner.

3. **If you give permissions to the Group entity, what does this mean?**

   These permissions apply to users who belong to the file's group, except the owner, whose User permissions apply.

4. **If you give permissions to the Other entity, what does this mean?**

   These permissions apply to users who are neither the owner nor members of the file's group.

5. **User permissions are read-only, Group permissions are read and write, and Other permissions are read, write and execute. As the owner, what permissions will you have? Explain.**

   You have **read-only** access. Linux uses the matching User permissions for the owner; it does not combine them with Group or Other permissions.

6. **Explain this line from `ls -l`:**

   ```text
   -rwxr-xr-- 1 tcboony staff 123 Nov 25 18:36 keeprunning.sh
   ```

   | Part | Meaning |
   | --- | --- |
   | `-` | A regular file, not a directory |
   | `rwx` | The owner can read, write, and execute |
   | `r-x` | Group members can read and execute, but cannot write |
   | `r--` | Other users can only read |
   | `1` | Number of hard links |
   | `tcboony` | File owner |
   | `staff` | File group |
   | `123` | File size in bytes |
   | `Nov 25 18:36` | Last modification date and time |
   | `keeprunning.sh` | File name |

   The numeric permission mode is **754**.
