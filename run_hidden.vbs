' WallpaperChanger - Hidden Background Launcher
' Runs main.py in the background without visible command prompt

Option Explicit

' Get the directory where this script is located
Dim objShell, objFSO, scriptDir, pythonPath, mainScriptPath

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
pythonPath = "pythonw.exe"
mainScriptPath = objFSO.BuildPath(scriptDir, "main.py")

' Check if main.py exists
If Not objFSO.FileExists(mainScriptPath) Then
    MsgBox "Error: main.py not found in:" & vbCrLf & scriptDir, vbCritical, "WallpaperChanger"
    WScript.Quit(1)
End If

' Run main.py hidden in background
objShell.Run """" & pythonPath & """ """ & mainScriptPath & """", 0, False

' Cleanup
Set objShell = Nothing
Set objFSO = Nothing
