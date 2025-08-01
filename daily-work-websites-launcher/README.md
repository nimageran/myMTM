# Daily Work Websites Launcher

A simple PowerShell script to automatically open multiple work websites in separate browser windows with one click.

## What it does
- Opens three specific websites in separate Microsoft Edge windows
- Adds a 1-second delay between each launch to prevent resource conflicts
- Perfect for multi-monitor setups where you want one website per monitor

## How to use

1. **Save the script** as `OpenWorkSites.ps1`
2. **Create a desktop shortcut:**
   - Right-click desktop → New → Shortcut
   - Browse to your `.ps1` file
   - Name it something like "Daily Work Sites"
3. **Configure the shortcut:**
   - Right-click shortcut → Properties
   - In Target field, change to: `powershell.exe -ExecutionPolicy Bypass -File "C:\Users\ngeran\Desktop\OpenWorkSites R0.ps1"`'
   - Note: If you update to later versions, like R1, R2, etc, accordingly change that revision number in the above target path.
   - Click OK

## Customization

To modify for your own websites:
1. Replace the URLs in the script with your desired websites
2. Add more `Start-Process` lines if you need more sites
3. Adjust the `Start-Sleep -Seconds` value to change delay timing
4. Change `msedge` to `chrome` or `firefox` for different browsers

## Use cases
- Daily work routine automation
- Multi-monitor setups
- Frequently accessed website groups
- Development environment setup

## Requirements
- Windows 10/11
- PowerShell (built into Windows)
- Microsoft Edge (or modify script for other browsers)

## Why PowerShell over batch files?
- Better Windows security integration (less SmartScreen warnings)
- More reliable process handling
- Easier to read and modify
