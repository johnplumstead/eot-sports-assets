#!/bin/bash
# Commits and pushes anything new in the repo. Run by launchd every 15 minutes.
# Credentials come from the macOS Keychain, so no token is stored in this file.
set -u
REPO="$HOME/Downloads/eot-sports"
GIT=/usr/bin/git
cd "$REPO" || exit 1
[ -z "$($GIT status --porcelain)" ] && exit 0
$GIT add -A
$GIT commit -qm "assets: $($GIT status --porcelain | wc -l | tr -d ' ') file(s) $(date '+%Y-%m-%d %H:%M')"
if $GIT push -q origin main 2>>"$REPO/.autopush.log"; then
  echo "$(date '+%Y-%m-%d %H:%M') pushed" >> "$REPO/.autopush.log"
else
  echo "$(date '+%Y-%m-%d %H:%M') PUSH FAILED" >> "$REPO/.autopush.log"
fi
