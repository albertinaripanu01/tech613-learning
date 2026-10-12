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
3. **How can we direct each stream to a file (one at a time)?**
4. **How can we direct both 2 output streams to a file?**
5. **Which stream is directed to a file by default?**
6 **How can we direct both output streams to a file in one command?**

