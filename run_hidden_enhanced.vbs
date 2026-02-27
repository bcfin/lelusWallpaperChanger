' WallpaperChanger - Enhanced Hidden Background Launcher
' Runs main.py in the background with error handling and logging

Option Explicit

' Configuration
Const LOG_FILE = "wallpaper_changer_launcher.log"
Const APP_NAME = "WallpaperChanger"

' Global objects
Dim objShell, objFSO, scriptDir, pythonPath, mainScriptPath, logPath

' Initialize
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get paths
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
pythonPath = "pythonw.exe"
mainScriptPath = objFSO.BuildPath(scriptDir, "main.py")
logPath = objFSO.BuildPath(scriptDir, LOG_FILE)

' Main execution
Call Main()

Sub Main()
    ' Log startup
    Call LogMessage("=== WallpaperChanger Launcher Started ===")
    Call LogMessage("Script Directory: " & scriptDir)
    Call LogMessage("Target Script: " & mainScriptPath)
    
    ' Check Python availability
    If Not CheckPythonAvailable() Then
        Call LogMessage("ERROR: Python not found in PATH")
        Call ShowError("Python is not installed or not in PATH" & vbCrLf & _
                       "Please run INSTALL.bat first or install Python from:" & vbCrLf & _
                       "https://www.python.org/downloads/")
        WScript.Quit(1)
    End If
    
    ' Check if main.py exists
    If Not objFSO.FileExists(mainScriptPath) Then
        Call LogMessage("ERROR: main.py not found at: " & mainScriptPath)
        Call ShowError("main.py not found in:" & vbCrLf & scriptDir)
        WScript.Quit(1)
    End If
    
    ' Check if requirements are installed
    If Not CheckRequirementsInstalled() Then
        Call LogMessage("WARNING: Some requirements may be missing")
    End If
    
    ' Run main.py hidden in background
    Call LogMessage("Starting WallpaperChanger in background...")
    
    On Error Resume Next
    objShell.Run """" & pythonPath & """ """ & mainScriptPath & """", 0, False
    
    If Err.Number <> 0 Then
        Call LogMessage("ERROR: Failed to start main.py - " & Err.Description)
        Call ShowError("Failed to start WallpaperChanger:" & vbCrLf & _
                       Err.Description & vbCrLf & vbCrLf & _
                       "Check the log file for details: " & logPath)
        WScript.Quit(1)
    End If
    
    On Error GoTo 0
    Call LogMessage("WallpaperChanger started successfully")
    Call LogMessage("=== Launcher Finished ===")
End Sub

Function CheckPythonAvailable()
    On Error Resume Next
    Dim result
    result = objShell.Run("pythonw.exe --version >nul 2>&1", 0, True)
    CheckPythonAvailable = (result = 0)
    On Error GoTo 0
End Function

Function CheckRequirementsInstalled()
    On Error Resume Next
    Dim result
    result = objShell.Run("pythonw.exe -c ""import PIL, requests, customtkinter"" >nul 2>&1", 0, True)
    CheckRequirementsInstalled = (result = 0)
    On Error GoTo 0
End Function

Sub LogMessage(message)
    On Error Resume Next
    Dim logFile, timestamp
    timestamp = Now()
    
    Set logFile = objFSO.OpenTextFile(logPath, 8, True) ' 8 = ForAppending
    logFile.WriteLine "[" & timestamp & "] " & message
    logFile.Close
    
    Set logFile = Nothing
    On Error GoTo 0
End Sub

Sub ShowError(message)
    MsgBox message, vbCritical, APP_NAME & " - Error"
End Sub

' Cleanup
Set objShell = Nothing
Set objFSO = Nothing
