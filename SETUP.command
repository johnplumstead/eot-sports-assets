#!/bin/bash
cd "$(dirname "$0")" || exit 1
clear
echo "=================================================="
echo "  East of Tampa Sports - GitHub setup"
echo "=================================================="
echo
echo "Folder: $(pwd)"
echo

if [ ! -d .git ]; then
  echo "ERROR: this folder is not a git repo. Re-unzip and try again."
  echo; read -p "Press return to close."; exit 1
fi

git config --local credential.helper osxkeychain

echo "STEP 1 of 2 - Pushing to GitHub"
echo
echo "  You will be asked for ONE thing: a Password."
echo
echo "     Paste your TOKEN there.  (NOT your GitHub password)"
echo
echo "  Your username is already filled in, so there is only one prompt."
echo "  Nothing shows on screen while you paste. That is normal."
echo "  It gets saved to your Keychain, so this only happens once."
echo
echo "--------------------------------------------------"
git push -u origin main
PUSH=$?
echo "--------------------------------------------------"

if [ $PUSH -ne 0 ]; then
  echo
  echo "  Push failed. Nothing was installed, nothing is broken."
  echo
  echo "  Most likely cause: the token is missing permission."
  echo "  It needs  Repository permissions > Contents > Read and write"
  echo "  on the eot-sports-assets repo."
  echo
  echo "  Fix the token, then double-click this file again."
  echo; read -p "Press return to close."; exit 1
fi

echo
echo "  Push succeeded."
echo
echo "STEP 2 of 2 - Installing the auto-push agent"
chmod +x tools/autopush.sh
mkdir -p "$HOME/Library/LaunchAgents"
cp tools/com.eastoftampa.autopush.plist "$HOME/Library/LaunchAgents/"
launchctl unload "$HOME/Library/LaunchAgents/com.eastoftampa.autopush.plist" 2>/dev/null
launchctl load "$HOME/Library/LaunchAgents/com.eastoftampa.autopush.plist" 2>/dev/null
sleep 2

if launchctl list | grep -q eastoftampa; then
  echo "  Agent installed. It checks this folder every 15 minutes."
else
  echo "  Agent did not start. Not fatal - the push above worked."
  echo "  Tell Claude and it will sort this out."
fi

echo
echo "=================================================="
echo "  Done."
echo "  https://github.com/johnplumstead/eot-sports-assets"
echo "=================================================="
echo
read -p "Press return to close."
