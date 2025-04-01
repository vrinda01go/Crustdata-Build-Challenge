@echo off
start chrome ^
 --remote-debugging-port=9222 ^
 --remote-allow-origins=* ^
 --user-data-dir="C:\Users\workstation\ai_browser\chrome_profile" ^
 --load-extension="C:\Users\workstation\Downloads\spotisush" ^
 --ignore-certificate-errors ^
 --no-first-run ^
 --no-default-browser-check ^
 --disable-web-security ^
 --disable-site-isolation-trials ^
 "https://open.spotify.com"
