@echo off
title Duplicate Data Finder - Desktop App
where pythonw >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    start "" pythonw duplicate_finder_gui.pyw
) else (
    start "" python duplicate_finder_gui.py
)
