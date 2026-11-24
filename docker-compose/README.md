# Sparta Tic-Tac-Toe Docker Compose

These deployments run the published Node app image with MongoDB as a separate service. They use the existing Docker Hub image `albertina1310/tech610-tttapp:1.2.0` and pin MongoDB to `7.0.22`, matching the MongoDB version already documented in this learning repository. The database volume keeps data when containers are recreated.

## Choose a deployment

| Folder | Behavior |
| --- | --- |
| [no-seed](no-seed/docker-compose.yml) | Starts the app and an empty database. |
| [manual-seed](manual-seed/docker-compose.yml) | Starts the same unseeded services; run the seed command yourself. |
| [auto-seed](auto-seed/docker-compose.yml) | Seeds from the app startup command, then starts the app (as in the class example). This reseeds on each app container start and replaces scoreboard entries. |
| [auto-seed-one-shot](auto-seed-one-shot/docker-compose.yml) | Starts a dedicated one-shot seed service after MongoDB is healthy and app starts. Use this to keep seeding separate from normal app restarts. |

Each folder is a standalone Compose project. Run commands from the folder you chose.

## Start without seeding

```powershell
docker compose up -d
docker compose ps
docker compose logs -f app
```

Open <http://localhost:3000>. The app waits for MongoDB's health check. The Compose network lets the app resolve the database by service name `db`, so its connection string is `mongodb://db:27017/tictactoe`. The Mongo image listens on the container network interfaces by default; no `bindIp` change is needed for service-to-service traffic. Port `27017:27017` also exposes MongoDB on the host for local tools.

## Seed manually

From `manual-seed` after `docker compose up -d`:

```powershell
docker compose exec app sh
```

At the container prompt, run:

```sh
node seeds/seed.js
exit
```

Or run it without opening an interactive shell:

```powershell
docker compose exec app node seeds/seed.js
```

The seed script clears and inserts the default scoreboard records. Run it only when you intend to replace the current scoreboard.

## Seed automatically: app startup

From `auto-seed`:

```powershell
docker compose up -d
docker compose logs app
```

The app container runs `node seeds/seed.js` before `node index.js`. Its `depends_on` health condition waits until MongoDB answers a ping. As the seed script replaces scoreboard entries, restarting this app container reseeds the database.

## Seed automatically: one-shot service

From `auto-seed-one-shot`:

```powershell
docker compose up -d
docker compose logs seed
```

The `seed` service runs once and exits. To run it again later:

```powershell
docker compose run --rm seed
```

## Container shell and cleanup

```powershell
docker compose exec app sh
docker compose exec db mongosh tictactoe
docker compose down
```

`docker compose down` keeps the named database volume. To permanently delete the stored Mongo data as well, use `docker compose down -v`.

MongoDB has no authentication configured in this learning deployment. Keep port 27017 limited to a trusted local network; do not expose it publicly on an EC2 security group.


