
This guide documents how to replace nginx's default page with my custom Christmas page, build a Docker image, publish it to Docker Hub, and run it locally or on another computer.

## Prerequisites

- Docker Desktop installed and running. The Docker CLI must be able to connect to the Docker engine.
- A Docker Hub account. This exercise uses `albertina1310`.
- PowerShell.

## 1. Open the project folder

```powershell
cd E:\SPARTAGLOBAL\tech613-mod-nginx-dockerfile
```

The folder contains:

- `index.html` — the custom page that nginx will serve.
- `Dockerfile` — instructions for building the image from nginx.

## 2. Customize the web page

Edit `index.html`. The current page displays “Happy Christmas!”. Save the file when finished.

## 3. Build the Docker image

Sign in to Docker Hub, then build and tag the image with your Docker Hub username and the repository name:

```powershell
docker login
docker build -t albertina1310/tech613-nginx-auto:1.0 .
```

The final `.` tells Docker to use the current folder as the build context. The Dockerfile starts from `nginx:alpine` and copies `index.html` to `/usr/share/nginx/html/index.html`, nginx's default web root page.

## 4. Run the image locally

```powershell
docker run --rm -d --name tech613-nginx -p 90:80 albertina1310/tech613-nginx-auto:1.0
```

This starts the container in the background. Port `90` on the computer is mapped to port `80` in the container. Visit [http://localhost:90](http://localhost:90) to see the page.

Stop the container with:

```powershell
docker stop tech613-nginx
```

Because the command includes `--rm`, Docker removes the container after it stops.

## 5. Publish the image on Docker Hub

Push the tagged image:

```powershell
docker push albertina1310/tech613-nginx-auto:1.0
```

For other people to run it without signing in, make the Docker Hub repository public. The image name includes the account name, repository name, and version tag.

## 6. Run the published image on another computer

Anyone with Docker installed can run:

```powershell
docker run --rm -d --name tech613-nginx -p 90:80 albertina1310/tech613-nginx-auto:1.0
```

Docker downloads the public image from Docker Hub automatically if it is not already available locally. Then open `http://localhost:90` on that computer.

## 7. Verify Docker Hub pull (optional)

On the publishing computer, stop the running container first, then remove the local image:

```powershell
docker stop tech613-nginx
docker image rm albertina1310/tech613-nginx-auto:1.0
```

Run the `docker run` command from step 6 again. Docker should pull the image from Docker Hub before starting it.

## Updating the page later

After changing `index.html`, rebuild the same tag, stop/remove the old container, and publish the updated image:

```powershell
docker build -t albertina1310/tech613-nginx-auto:1.0 .
docker rm -f tech613-nginx
docker push albertina1310/tech613-nginx-auto:1.0
docker run --rm -d --name tech613-nginx -p 90:80 albertina1310/tech613-nginx-auto:1.0
```

```powershell
ls 
uname -a
apt-get update -y
apt-get upgrade -y
sudo systemctl status nginx
apt-get install sudo
pwd
ls
cd /user
ls
cd share
ls
apt-get install nano 
nano index.html
exit
```