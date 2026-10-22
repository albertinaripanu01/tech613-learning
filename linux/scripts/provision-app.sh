#!/usr/bin/env bash
set -euo pipefail

# Run as your normal Ubuntu user, without sudo.
# The script uses sudo only when installing system packages.
ZIP="$HOME/nodejs20-sparta-tictactoe-v1.zip"
DEPLOY_DIR="$HOME/tictactoe-deployment"
APP_NAME="tictactoe"

if [[ "$EUID" -eq 0 ]]; then
    echo "Please run: bash provision-app.sh (without sudo)"
    exit 1
fi

if [[ ! -f "$ZIP" ]]; then
    echo "ZIP file not found: $ZIP"
    exit 1
fi

echo "Installing required tools..."
sudo apt-get update
sudo apt-get install -y curl ca-certificates unzip util-linux

# Prevent two copies of this script running at the same time.
exec 9>"$HOME/.tictactoe-provision.lock"
flock -n 9 || {
    echo "Another deployment is already running."
    exit 1
}

# Install Node.js 22 if a suitable version is not installed.
if ! command -v node >/dev/null 2>&1 ||
   ! node -e 'process.exit(Number(process.versions.node.split(".")[0]) >= 22 ? 0 : 1)'
then
    SETUP_FILE="$(mktemp)"
    curl -fsSL https://deb.nodesource.com/setup_22.x \
        -o "$SETUP_FILE"
    sudo bash "$SETUP_FILE"
    rm -f "$SETUP_FILE"
    sudo apt-get install -y nodejs
fi

if ! command -v pm2 >/dev/null 2>&1; then
    echo "Installing PM2..."
    sudo npm install --global pm2
fi

echo "Extracting the app..."
mkdir -p "$DEPLOY_DIR"
unzip -oq "$ZIP" -d "$DEPLOY_DIR"

cd "$DEPLOY_DIR/app"

echo "Installing app dependencies..."
# Skip the app's install hook to avoid resetting scoreboard data.
npm ci --omit=dev --ignore-scripts

echo "Starting or restarting the app..."
export NODE_ENV=production
export PORT=3000

if pm2 describe "$APP_NAME" >/dev/null 2>&1; then
    pm2 restart "$APP_NAME" --update-env
else
    pm2 start index.js --name "$APP_NAME"
fi

echo "Configuring startup after reboot..."
sudo env PATH="$PATH" "$(command -v pm2)" startup systemd \
    -u "$(id -un)" --hp "$HOME"
pm2 save

echo "Checking the app..."
for attempt in {1..30}; do
    if curl -fsS http://127.0.0.1:3000/ >/dev/null; then
        echo "Deployment successful. App is running on port 3000."
        pm2 list
        exit 0
    fi
    sleep 2
done

echo "App did not respond. Check: pm2 logs tictactoe"
exit 1
