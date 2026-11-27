# Sparta Tic-Tac-Toe Docker Exercise

This guide records the steps for packaging the Sparta Tic-Tac-Toe Node.js app in Docker, running it locally, and publishing the image to Docker Hub so other people can download and run it.

## What you need

- Docker Desktop installed and running.
- The supplied `nodejs20-sparta-tictactoe-v1.zip` file.
- A Docker Hub account. The repository must be public if anyone should be able to pull the image.

## 1. Prepare the project folder

In `E:\SPARTAGLOBAL`, create a project folder named `docker-run-sparta-app`. Extract the ZIP into that folder so its contents include:

```text
docker-run-sparta-app/
  app/
    index.js
    package.json
    package-lock.json
    ...the rest of the Sparta app...
```

Keep the Dockerfile next to the `app` folder. Open PowerShell in `E:\SPARTAGLOBAL\docker-run-sparta-app` before running the commands below.

## 2. Create the Dockerfile

The Dockerfile in this project uses Node.js 20, installs the locked production dependencies, copies the app, switches to the unprivileged `node` user, and starts `index.js` on port 3000:

```dockerfile
FROM node:20-alpine

ENV NODE_ENV=production
WORKDIR /app

COPY app/package.json app/package-lock.json ./
RUN npm ci --ignore-scripts

COPY app/ ./

USER node
EXPOSE 3000
CMD ["node", "index.js"]
```

`--ignore-scripts` skips the app's npm postinstall seed step, so the build does not need a MongoDB server. The app can start in its built-in fallback mode. MongoDB-backed state requires a separately running MongoDB service and a configured `MONGODB_URI`.

## 3. Build the image

From the project folder, build the image and give it a local name and version tag:

```powershell
docker build -t sparta-ttt:1.2.0 .
```

Confirm the image exists:

```powershell
docker image ls sparta-ttt
```

## 4. Run and check the app locally

Start a container and map port 3000 on your computer to port 3000 in the container:

```powershell
docker run -d --name sparta-ttt -p 3000:3000 sparta-ttt:1.2.0
```

Open <http://localhost:3000>. The app should load. Check the container status and logs with:

```powershell
docker ps
docker logs sparta-ttt
```

Stop the container when you are done:

```powershell
docker stop sparta-ttt
```

To start that same stopped container later, use `docker start sparta-ttt`.

### If Docker reports that the container name is already in use

A container named `sparta-ttt` already exists. Start the existing one with `docker start sparta-ttt`, or remove it and create a fresh one:

```powershell
docker rm -f sparta-ttt
docker run -d --name sparta-ttt -p 3000:3000 sparta-ttt:1.2.0
```

Removing a container deletes that container instance. It does not delete the image. If port 3000 is already being used by another container or application, stop that service or map a different host port, for example `-p 3001:3000`, and browse to <http://localhost:3001>.

## 5. Publish the image to Docker Hub

Create a Docker Hub repository named `tech610-tttapp` and set its visibility to **Public**. Replace `YOUR_DOCKERHUB_USERNAME` below with your Docker Hub username. For example, if your username is `albertina1310`, the image name starts with `albertina1310/`.

Sign in from PowerShell, tag the local image with the Docker Hub repository name, then push it:

```powershell
docker login
docker tag sparta-ttt:1.2.0 YOUR_DOCKERHUB_USERNAME/tech610-tttapp:1.2.0
docker push YOUR_DOCKERHUB_USERNAME/tech610-tttapp:1.2.0
```

Do not include angle brackets around the username. Docker Hub credentials are entered through `docker login`; do not put passwords or access tokens in the commands or documentation.

## 6. Instructions for anyone downloading the public image

On a computer with Docker installed, anyone can pull and run the published image. Replace the username with the actual Docker Hub account that owns the public repository:

```powershell
docker pull YOUR_DOCKERHUB_USERNAME/tech610-tttapp:1.2.0
docker run -d --name sparta-ttt -p 3000:3000 YOUR_DOCKERHUB_USERNAME/tech610-tttapp:1.2.0
```

They can then open <http://localhost:3000>. If they already have a container with the name `sparta-ttt`, they can choose another name (such as `sparta-ttt-public`) and another host port (such as `3001:3000`).



