#!/bin/bash
cd "$(dirname "$0")" || exit 1
clear
echo "=================================================="
echo "  East of Tampa Sports - finish auto-push setup"
echo "=================================================="
echo
echo "Folder: $(pwd)"
echo
echo "No token needed. It is already in your Keychain."
echo

chmod +x tools/autopush.sh
mkdir -p "$HOME/Library/LaunchAgents"
launchctl unload "$HOME/Library/LaunchAgents/com.eastoftampa.autopush.plist" 2>/dev/null
cp tools/com.eastoftampa.autopush.plist "$HOME/Library/LaunchAgents/"
launchctl load "$HOME/Library/LaunchAgents/com.eastoftampa.autopush.plist" 2>/dev/null
sleep 2

echo "Testing a real push..."
echo "verified $(date '+%Y-%m-%d %H:%M')" > .setup-check
bash tools/autopush.sh
sleep 1

if git status -sb | head -1 | grep -q "ahead"; then
  echo
  echo "  Push did not go through. Log:"
  tail -3 .autopush.log 2>/dev/null
  echo
else
  echo
  echo "  Push works from the agent."
fi

if launchctl list | grep -q eastoftampa; then
  echo "  Agent is loaded and will check this folder every 15 minutes."
else
  echo "  Agent did not load. Tell Claude."
fi

echo
echo "  You can delete the old copy in Downloads whenever you like."
echo "=================================================="
echo
read -p "Press return to close."
