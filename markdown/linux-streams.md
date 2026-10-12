**What is a stream in Linux?**
You call something a stream when you mean the channel carrying data into or out of a program.
1. **What are the 3 data streams?**
   - **stdin (0):** input, usually from your keyboard.  
     For example, with `cat`:

     ```text
     Keyboard → stdin → cat → stdout → Terminal
     ```

   - **stdout (1):** normal output, usually displayed in the terminal.  
     For example, with `echo "Hello"`:

     ```text
     echo → stdout (1) → Terminal
            "Hello"
     ```

   - **stderr (2):** error messages, also usually displayed in the terminal.  
     For example, with `ls missing_directory`:

     ```text
     ls: cannot access 'missing_directory': No such file or directory

     ls → stderr (2) → Terminal
          error message
     ```
2. **Create a new file `new.txt` and run the command `ls missing_directory new.txt` - this should give output to two different streams.**
   <img width="587" height="66" alt="image" src="https://github.com/user-attachments/assets/df28ae2b-ff1f-4ef1-a4e6-a2cd59c66c70" />

3. **How can we direct each stream to a file (one at a time)?**
   - **stdout (1):** use `>` to save normal output to a file.

     ```bash
     ls missing_directory new.txt > output.txt
     ```

     Normal output goes to `output.txt`; errors remain in the terminal.

   - **stderr (2):** use `2>` to save errors to a file.

     ```bash
     ls missing_directory new.txt 2> errors.txt
     ```

     Errors go to `errors.txt`; normal output remains in the terminal.

   - **stdin (0):** use `<` to read input **from** a file.

     ```bash
     cat < new.txt
     ```

     Input comes from `new.txt`; normal output goes to the terminal.

   `>` and `2>` overwrite the destination file. Use `>>` and `2>>` to append instead.
4. **How can we direct both 2 output streams to a file?**
    Redirect stdout and stderr to separate files:

   ```bash
   ls missing_directory new.txt > output.txt 2> errors.txt
   ```
5. **Which stream is directed to a file by default?**
    Using `>` without a stream number redirects **stdout (1)**. stderr remains in the terminal.

   ```bash
   ls > output.txt
   ```
6. **How can we direct both output streams to a file in one command?**
   Send stdout and stderr to the same file:

   ```bash
   ls missing_directory new.txt > combined.txt 2>&1
   ```

   `2>&1` redirects stderr to the same destination as stdout. Put it after `> combined.txt`.
