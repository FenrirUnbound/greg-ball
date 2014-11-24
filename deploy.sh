#!/bin/sh
sudo apt-get update
sudo apt-get install unzip

cd $WERCKER_ROOT
debug 'Downloading AppEngine SDK...'

curl -o appengine.zip https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.15.zip; unzip -x appengine.zip
export PATH="$PATH:$(pwd)/google_appengine"

echo "$APP_ENGINE_PASS" > "$WERCKER_STEP_TEMP/password"

cd $WERCKER_SOURCE_DIR

debug 'Starting deployment of directory'
appcfg.py update --email="$APP_ENGINE_USER" --passin < "$WERCKER_STEP_TEMP/password"

success 'Finished'