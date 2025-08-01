# Open three work websites in separate Edge windows (forced new windows)
Start-Process msedge -ArgumentList "--new-window", "https://viewer.autodesk.com/designviews"
Start-Sleep -Seconds 2
Start-Process msedge -ArgumentList "--new-window", "https://mtm115.sharepoint.com/sites/Quality/Lists/ARDescription/AllItems.aspx"
Start-Sleep -Seconds 2
Start-Process msedge -ArgumentList "--new-window", "https://chatgpt.com/g/g-p-67a0fc3e1c5c8191abd8f5feee50e23a-mywork-mtm/project"
