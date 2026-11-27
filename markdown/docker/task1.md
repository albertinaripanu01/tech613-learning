# Create, Edit, Push, and Run an Nginx Image

These steps create an nginx container, edit its default page, save the changed container as a Docker image, push the image to Docker Hub, and run that image.

## 1. Create an nginx container

## 2. Enter the container and edit `index.html`

## 3. Sign in to Docker Hub

```powershell
docker login
```

This signs the Docker CLI in to Docker Hub. It does not reveal your username; `albertina1310` is the username used in the image name below.

## 4. Commit the changed container as an image

```powershell
docker commit my-nginx albertina1310/my-nginx:1.0
```

This creates an image named `albertina1310/my-nginx` with the tag `1.0`, including the page changes made in the container.

## 5. Push the image to Docker Hub

```powershell
docker push albertina1310/my-nginx:1.0
```

This uploads the image to the Docker Hub account. Make the repository public in Docker Hub if other people need to pull it without signing in.

## 6. Run the pushed image

The original container already uses the name `my-nginx`, so remove that container after committing the image:

```powershell
docker rm -f my-nginx
```

Now run the image from Docker Hub:

```powershell
docker run -d -p 90:80 --name my-nginx albertina1310/my-nginx:1.0
```

Docker pulls the image if it is not already on the computer. Open `http://localhost:90` to view the edited page.



