Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$Form = New-Object System.Windows.Forms.Form
$Form.Text = "HUNGER Billing Installer"
$Form.Size = New-Object System.Drawing.Size(420,260)
$Form.StartPosition = "CenterScreen"

$Label = New-Object System.Windows.Forms.Label
$Label.Text = "Install dependencies and run the app"
$Label.AutoSize = $true
$Label.Location = New-Object System.Drawing.Point(20,20)
$Form.Controls.Add($Label)

$Output = New-Object System.Windows.Forms.TextBox
$Output.Multiline = $true
$Output.ScrollBars = "Vertical"
$Output.Size = New-Object System.Drawing.Size(360,120)
$Output.Location = New-Object System.Drawing.Point(20,50)
$Form.Controls.Add($Output)

$InstallBtn = New-Object System.Windows.Forms.Button
$InstallBtn.Text = "Install"
$InstallBtn.Location = New-Object System.Drawing.Point(20,180)
$Form.Controls.Add($InstallBtn)

$RunBtn = New-Object System.Windows.Forms.Button
$RunBtn.Text = "Run App"
$RunBtn.Location = New-Object System.Drawing.Point(120,180)
$Form.Controls.Add($RunBtn)

$CloseBtn = New-Object System.Windows.Forms.Button
$CloseBtn.Text = "Close"
$CloseBtn.Location = New-Object System.Drawing.Point(300,180)
$Form.Controls.Add($CloseBtn)

function Append-Log($text) {
  $Output.AppendText($text + [Environment]::NewLine)
}

$InstallBtn.Add_Click({
  Append-Log "Upgrading pip..."
  python -m pip install --upgrade pip 2>&1 | ForEach-Object { Append-Log $_ }
  Append-Log "Installing requirements..."
  python -m pip install -r requirements.txt 2>&1 | ForEach-Object { Append-Log $_ }
  Append-Log "Done."
})

$RunBtn.Add_Click({
  Append-Log "Launching application..."
  Start-Process -FilePath python -ArgumentList "main.py"
})

$CloseBtn.Add_Click({ $Form.Close() })

[void]$Form.ShowDialog()
