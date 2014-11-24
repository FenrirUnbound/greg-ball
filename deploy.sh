#!/bin/sh
sudo apt-get update -qq
sudo apt-get install unzip -y

cd $WERCKER_ROOT
echo 'Downloading AppEngine SDK...'

curl -o appengine.zip https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.15.zip; unzip -qx appengine.zip
export PATH="$PATH:$(pwd)/google_appengine"

echo "$APP_ENGINE_PASS" > "$WERCKER_STEP_TEMP/password"

cd $WERCKER_SOURCE_DIR

echo 'Starting deployment of directory'
appcfg.py update ./ --email="$APP_ENGINE_USER" --passin < "$WERCKER_STEP_TEMP/password"

echo 'Finished'