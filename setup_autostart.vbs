' WallpaperChanger - Autostart Setup Script
' Configures WallpaperChanger to start automatically with Windows

Option Explicit

' Constants
Const HKEY_CURRENT_USER = &H80000001
Const REG_SZ = 1
Const APP_NAME = "WallpaperChanger"
Const REG_KEY_PATH = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

' Global objects
Dim objShell, objFSO, objRegistry, scriptDir, vbsPath, logPath

' Initialize
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objRegistry = GetObject("winmgmts:\\.\root\default:StdRegProv")

' Get paths
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
vbsPath = objFSO.BuildPath(scriptDir, "run_hidden_enhanced.vbs")
logPath = objFSO.BuildPath(scriptDir, "autostart_setup.log")

' Main execution
Call Main()

Sub Main()
    Call LogMessage("=== WallpaperChanger Autostart Setup ===")
    Call LogMessage("Script Directory: " & scriptDir)
    Call LogMessage("VBScript Path: " & vbsPath)
    
    ' Check if the enhanced VBScript exists
    If Not objFSO.FileExists(vbsPath) Then
        Call LogMessage("ERROR: run_hidden_enhanced.vbs not found")
        Call ShowError("run_hidden_enhanced.vbs not found!" & vbCrLf & _
                       "Please ensure this file exists in the WallpaperChanger directory.")
        WScript.Quit(1)
    End If
    
    ' Setup autostart using both methods for reliability
    Dim registrySuccess, startupSuccess
    
    registrySuccess = SetupRegistryAutostart()
    startupSuccess = SetupStartupFolder()
    
    If registrySuccess Or startupSuccess Then
        Call LogMessage("SUCCESS: Autostart configured successfully")
        Call ShowInfo("WallpaperChanger has been configured to start automatically with Windows." & vbCrLf & _
                     "You can disable this by running uninstall_autostart.vbs")
        WScript.Quit(0)
    Else
        Call LogMessage("ERROR: Failed to configure autostart")
        Call ShowError("Failed to configure autostart." & vbCrLf & _
                      "Please check the log file: " & logPath)
        WScript.Quit(1)
    End If
End Sub

Function SetupRegistryAutostart()
    On Error Resume Next
    Dim valueName, valueData
    
    valueName = APP_NAME
    valueData = "wscript.exe """ & vbsPath & """"
    
    Call LogMessage("Setting up registry autostart...")
    Call LogMessage("Registry Key: " & REG_KEY_PATH)
    Call LogMessage("Value Name: " & valueName)
    Call LogMessage("Value Data: " & valueData)
    
    ' Set the registry value
    objRegistry.SetStringValue HKEY_CURRENT_USER, REG_KEY_PATH, valueName, valueData
    
    If Err.Number = 0 Then
        Call LogMessage("SUCCESS: Registry autostart configured")
        SetupRegistryAutostart = True
    Else
        Call LogMessage("ERROR: Registry setup failed - " & Err.Description)
        SetupRegistryAutostart = False
    End If
    
    On Error GoTo 0
End Function

Function SetupStartupFolder()
    On Error Resume Next
    Dim startupPath, shortcutPath, objShortcut
    
    startupPath = objShell.SpecialFolders("Startup")
    shortcutPath = objFSO.BuildPath(startupPath, APP_NAME & ".lnk")
    
    Call LogMessage("Setting up Startup folder shortcut...")
    Call LogMessage("Startup Folder: " & startupPath)
    Call LogMessage("Shortcut Path: " & shortcutPath)
    
    ' Create shortcut
    Set objShortcut = objShell.CreateShortcut(shortcutPath)
    objShortcut.TargetPath = "wscript.exe"
    objShortcut.Arguments = """" & vbsPath & """"
    objShortcut.WorkingDirectory = scriptDir
    objShortcut.Description = "WallpaperChanger Background Service"
    objShortcut.WindowStyle = 7 ' Minimized
    objShortcut.Save()
    
    If Err.Number = 0 Then
        Call LogMessage("SUCCESS: Startup folder shortcut created")
        SetupStartupFolder = True
    Else
        Call LogMessage("ERROR: Startup folder setup failed - " & Err.Description)
        SetupStartupFolder = False
    End If
    
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
    MsgBox message, vbCritical, APP_NAME & " - Autostart Error"
End Sub

Sub ShowInfo(message)
    MsgBox message, vbInformation, APP_NAME & " - Autostart Setup"
End Sub

' Cleanup
Set objShell = Nothing
Set objFSO = Nothing
Set objRegistry = Nothing
