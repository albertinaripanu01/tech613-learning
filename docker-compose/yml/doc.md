# TTT Kubernetes deployments

The two folders contain separate versions of the deployment. Run the same two commands from the folder for the version you want:

```powershell
kubectl apply -f ttt-deploy].yml
kubectl apply -f ttt-service.yml
```

The first command applies the Deployment YAML; the second applies the Service YAML. The first filename above is copied exactly as typed. The file in the folders is named `ttt-deploy.yml` without `]`.

## 1. TTT app only

Folder: `yml\local-ttt-app-deploy`

### `ttt-deploy.yml`

```yaml
# YAML is case sensitive
# use spaces not a tab
apiVersion: apps/v1  # specify api to use for deployment
kind: Deployment
metadata:
  name: ttt-deployment  # name the deployment
  labels:
    app: ttt-app
spec:
  selector:
    matchLabels:
      app: ttt-app
  replicas: 3
  template:
    metadata:
      labels:
        app: ttt-app
    spec:
      containers:
        - name: ttt-app
          image: albertina1310/tech610-tttapp:1.2.0
          ports:
            - containerPort: 3000
```

`replicas: 3` creates three app pods. The same `app: ttt-app` label on the pods and selector lets the Service find them. The image is your Docker Hub image, and it listens on port 3000.

### `ttt-service.yml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ttt-service
  namespace: default
spec:
  ports:
    - nodePort: 30002
      port: 3000
      targetPort: 3000
  selector:
    app: ttt-app
  type: NodePort
```

`NodePort` exposes the app outside the cluster on 30002. Service port 3000 forwards to container port 3000; the selector routes traffic to the three TTT pods.

`Browser → NodePort 30002 → 3 TTT app pods`

## 2. TTT app with MongoDB

Folder: `yml\ttt-mongo`

Use the same two commands above from this folder. Here `ttt-deploy.yml` contains both Deployments, and `ttt-service.yml` contains both Services.

### `ttt-deploy.yml`

```yaml
# YAML is case sensitive
# use spaces not a tab
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ttt-deployment
  labels:
    app: ttt-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ttt-app
  template:
    metadata:
      labels:
        app: ttt-app
    spec:
      containers:
        - name: ttt-app
          image: albertina1310/tech610-tttapp:1.2.0
          ports:
            - containerPort: 3000
          env:
            - name: MONGODB_URI
              value: mongodb://ttt-mongo:27017/posts
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ttt-mongo
  labels:
    app: ttt-mongo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ttt-mongo
  template:
    metadata:
      labels:
        app: ttt-mongo
    spec:
      containers:
        - name: mongodb
          image: mongo:8.0
          ports:
            - containerPort: 27017
```

The app Deployment still runs three pods. `MONGODB_URI` is the environment variable this image reads to connect to MongoDB. `ttt-mongo` is the database Service's cluster DNS name. The second Deployment runs one MongoDB pod using `mongo:8.0` on port 27017.

### `ttt-service.yml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ttt-service
  namespace: default
spec:
  type: NodePort
  selector:
    app: ttt-app
  ports:
    - nodePort: 30003
      port: 3000
      targetPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: ttt-mongo
  namespace: default
spec:
  type: ClusterIP
  selector:
    app: ttt-mongo
  ports:
    - port: 27017
      targetPort: 27017
```

The app remains reachable through NodePort 30003. MongoDB uses an internal `ClusterIP` Service on port 27017, so the app can reach it by `ttt-mongo` inside the cluster.

`Browser → NodePort 30003 → 3 TTT app pods → ttt-mongo:27017 → 1 MongoDB pod`

