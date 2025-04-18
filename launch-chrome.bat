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

@REM @echo off
@REM start chrome ^
@REM  --remote-debugging-port=9222 ^
@REM  --remote-allow-origins=* ^
@REM  --user-data-dir="C:\Users\workstation\ai_browser\chrome_profile" ^
@REM  --load-extension="C:\Users\workstation\Downloads\spotisush" ^
@REM  --proxy-server="http://127.0.0.1:8089" ^
@REM  --ignore-certificate-errors ^
@REM  --no-first-run ^
@REM  --no-default-browser-check ^
@REM  --disable-web-security ^
@REM  --disable-site-isolation-trials ^
@REM  "https://open.spotify.com"

@REM @echo off
@REM start chrome ^
@REM  --proxy-server=http://127.0.0.1:8089 ^
@REM  --user-data-dir="C:\Users\workstation\ai_browser\chrome_proxy" ^
@REM  --no-first-run ^
@REM  --no-default-browser-check ^
@REM  --disable-default-apps ^
@REM  https://httpbin.org/ip




