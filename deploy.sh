#!/bin/sh
sudo apt-get update -qq
sudo apt-get install unzip -y

cd $WERCKER_ROOT
echo 'Downloading AppEngine SDK...'

curl -s -o google_appengine.zip https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.15.zip
unzip -q google_appengine.zip -d /usr/local
export PATH="$PATH:/usr/local/google_appengine"

echo "$APP_ENGINE_PASS" > "$WERCKER_STEP_TEMP/password"

echo "cleaning up"
rm appengine.zip
find . -name "*.pyc" -exec rm -rf {} \;

echo 'Starting deployment of directory'
cd $WERCKER_SOURCE_DIR
appcfg.py update ./ --email="$APP_ENGINE_USER" --passin < "$WERCKER_STEP_TEMP/password"

echo 'Finished'