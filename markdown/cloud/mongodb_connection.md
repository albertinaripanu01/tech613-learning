1. Keep the MongoDB process from `mongodb.md` running.

2. Open a terminal on the separate instance where you have the Tic Tac Toe app, and navigate to the app directory.

   ![Tic Tac Toe app instance](https://github.com/user-attachments/assets/86c25152-86f8-4de1-83d5-28b6149aa9a8)

3. Set the MongoDB connection URI. Replace `63.35.224.252` with the public IP address of the instance running MongoDB.

   ```bash
   export MONGODB_URI=mongodb://63.35.224.252:27017/tictactoe
   ```

4. Check the environment variable:

   ```bash
   printenv MONGODB_URI
   ```

5. Stop PM2 and install the dependencies:

   ```bash
   pm2 kill
   npm install
   ```

   Look for `SEEDED mongodb` in the output.

   ![MongoDB seeding output](https://github.com/user-attachments/assets/bf2d02bd-2faa-4e23-8643-24a361604c2e)

6. Start the app:

   ```bash
   pm2 start index.js --name tic
   ```

7. Reload the page in your browser. The following should appear:

   ![Expected Tic Tac Toe page](https://github.com/user-attachments/assets/066fc97d-1d84-4a33-b2a3-fcc019a35819)

  
9:20
