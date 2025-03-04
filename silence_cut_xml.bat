@echo off
chcp 65001

cd /d "%~dp0"
call venv\Scripts\activate
for %%f in (%*) do (
	python -m drnonsilentxml -i "%%~dpnxf" -if 60 -o "%~dp0%%~nf.xml" -of 59.94
)

pause