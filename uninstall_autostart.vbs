' WallpaperChanger - Autostart Uninstall Script
' Removes WallpaperChanger from Windows startup

Option Explicit

' Constants
Const HKEY_CURRENT_USER = &H80000001
Const APP_NAME = "WallpaperChanger"
Const REG_KEY_PATH = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

' Global objects
Dim objShell, objFSO, objRegistry, scriptDir, logPath

' Initialize
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objRegistry = GetObject("winmgmts:\\.\root\default:StdRegProv")

' Get paths
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
logPath = objFSO.BuildPath(scriptDir, "autostart_uninstall.log")

' Main execution
Call Main()

Sub Main()
    Call LogMessage("=== WallpaperChanger Autostart Uninstall ===")
    
    Dim registrySuccess, startupSuccess
    
    registrySuccess = RemoveRegistryAutostart()
    startupSuccess = RemoveStartupFolder()
    
    If registrySuccess Or startupSuccess Then
        Call LogMessage("SUCCESS: Autostart removed successfully")
        Call ShowInfo("WallpaperChanger has been removed from Windows startup.")
        WScript.Quit(0)
    Else
        Call LogMessage("INFO: No autostart entries found to remove")
        Call ShowInfo("WallpaperChanger was not configured for autostart.")
        WScript.Quit(0)
    End If
End Sub

Function RemoveRegistryAutostart()
    On Error Resume Next
    Dim valueName
    
    valueName = APP_NAME
    
    Call LogMessage("Removing registry autostart entry...")
    
    ' Check if the value exists first
    Dim values, valueTypes, valueNames
    objRegistry.EnumValues HKEY_CURRENT_USER, REG_KEY_PATH, valueNames, valueTypes
    
    If IsArray(valueNames) Then
        Dim i, found
        found = False
        For i = LBound(valueNames) To UBound(valueNames)
            If valueNames(i) = valueName Then
                found = True
                Exit For
            End If
        Next
        
        If found Then
            ' Delete the registry value
            objRegistry.DeleteValue HKEY_CURRENT_USER, REG_KEY_PATH, valueName
            
            If Err.Number = 0 Then
                Call LogMessage("SUCCESS: Registry autostart entry removed")
                RemoveRegistryAutostart = True
            Else
                Call LogMessage("ERROR: Failed to remove registry entry - " & Err.Description)
                RemoveRegistryAutostart = False
            End If
        Else
            Call LogMessage("INFO: No registry autostart entry found")
            RemoveRegistryAutostart = False
        End If
    Else
        Call LogMessage("INFO: No registry entries found")
        RemoveRegistryAutostart = False
    End If
    
    On Error GoTo 0
End Function

Function RemoveStartupFolder()
    On Error Resume Next
    Dim startupPath, shortcutPath
    
    startupPath = objShell.SpecialFolders("Startup")
    shortcutPath = objFSO.BuildPath(startupPath, APP_NAME & ".lnk")
    
    Call LogMessage("Removing Startup folder shortcut...")
    Call LogMessage("Shortcut Path: " & shortcutPath)
    
    If objFSO.FileExists(shortcutPath) Then
        objFSO.DeleteFile shortcutPath, True
        
        If Err.Number = 0 Then
            Call LogMessage("SUCCESS: Startup folder shortcut removed")
            RemoveStartupFolder = True
        Else
            Call LogMessage("ERROR: Failed to remove shortcut - " & Err.Description)
            RemoveStartupFolder = False
        End If
    Else
        Call LogMessage("INFO: No Startup folder shortcut found")
        RemoveStartupFolder = False
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

Sub ShowInfo(message)
    MsgBox message, vbInformation, APP_NAME & " - Autostart Removal"
End Sub

' Cleanup
Set objShell = Nothing
Set objFSO = Nothing
Set objRegistry = Nothing
