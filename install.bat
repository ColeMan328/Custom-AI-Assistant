@echo off

:: Navigate to the directory of the script
cd %~dp0

:: Install dependencies
pip install -r requirements.txt

:: Create or update configuration files
:: Model configuration
echo Please enter the model to be used (e.g., gpt-4o, gpt-3.5-turbo, etc...):
set /p MODEL=

:: Create or update model configuration file
echo %MODEL% > model.txt

:: Temperature configuration
echo Please enter the temperature (e.g., 0.7 0.0 is least creative and 1.0 is more creative.):
set /p TEMPERATURE=

:: Create or update temperature configuration file
echo %TEMPERATURE% > temperature.txt

:: Role system content
echo Please enter the system role content:
echo (For example: You are a helpful assistant named Friday.This is where you customize AI personality)
set /p ROLE_SYSTEM_CONTENT=

:: Create or update role system content configuration file
echo %ROLE_SYSTEM_CONTENT% > role_system_content.txt

:: Path to the custom icon (make sure the icon exists at this path)
set ICON_PATH=%~dp0static\icon.ico

:: Retrieve the Desktop path using PowerShell
for /f "usebackq tokens=*" %%a in (`powershell -NoProfile -Command "[System.Environment]::GetFolderPath('Desktop')"`) do set DESKTOP_PATH=%%a

:: Create a PowerShell script to create a shortcut with a custom icon
echo $wsh = New-Object -ComObject WScript.Shell > create_shortcut.ps1
echo $shortcut = $wsh.CreateShortcut("%DESKTOP_PATH%\Custom AI.lnk") >> create_shortcut.ps1
echo $shortcut.TargetPath = "%~dp0run.bat" >> create_shortcut.ps1
echo $shortcut.WorkingDirectory = "%~dp0" >> create_shortcut.ps1
echo $shortcut.IconLocation = "%ICON_PATH%" >> create_shortcut.ps1
echo $shortcut.Save() >> create_shortcut.ps1

:: Run the PowerShell script
powershell -ExecutionPolicy Bypass -File create_shortcut.ps1

:: Clean up the PowerShell script
del create_shortcut.ps1

echo Installation complete. A shortcut to run.bat has been added to your Desktop with a custom icon.
pause