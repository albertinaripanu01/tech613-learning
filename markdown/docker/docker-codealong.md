# Docker Commands and Nginx Exercise

## List containers

Show running containers:

```bash
docker ps
```

Show all containers, including stopped containers:

```bash
docker ps -a
```

## Run nginx on port 80

Start nginx in the background and map port 80 on your computer to port 80 in the container:

```bash
docker run -d -p 80:80 nginx
```

Check the container name Docker assigned:

```bash
docker ps
```

Open `http://localhost` to view the nginx default page. If port 80 is already in use, use another host port, such as `-p 90:80`.

## Stop, start, and remove a container

Replace `<container-name>` with the name shown by `docker ps` or `docker ps -a`.

Stop a running container:

```bash
docker stop <container-name>
```

Start a stopped container:

```bash
docker start <container-name>
```

Force-remove a container, including a running one:

```bash
docker rm -f <container-name>
```

## Enter a running container and edit the page

Open a shell inside the container:

```bash
docker exec -it <container-name> sh
```

Run these commands inside the container shell:

```sh
ls
uname -a
apt-get update -y
apt-get upgrade -y
apt-get install -y sudo
pwd
ls
cd /usr
ls
cd share
ls
cd nginx
cd html
ls
apt-get install -y nano
nano index.html
```

Edit the page in nano. Save with **Ctrl+O**, press **Enter**, then exit nano with **Ctrl+X**. Leave the container shell:

```sh
exit
```

## Run the Dream Team nginx image on port 90

```bash
docker run -d -p 90:80 daraymonsta/nginx-257:dreamteam
```

Open `http://localhost:90` to view the page. Use `docker ps` to find the container’s assigned name or ID.