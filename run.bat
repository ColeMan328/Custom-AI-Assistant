@echo off

:: Navigate to the directory of the script
cd %~dp0

:: Run the Flask application
start cmd /k "python app.py"

:: Wait for a couple of seconds to ensure the server starts
timeout 2

:: Open the default web browser to the local application URL
start "" "http://127.0.0.1:5000"
