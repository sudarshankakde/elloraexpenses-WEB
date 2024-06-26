
@echo off

REM Open terminal window for Django server
start cmd.exe /k "call conda activate freelance && python manage.py runserver"
