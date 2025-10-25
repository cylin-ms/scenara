# CYL's Calendar Analysis - PowerShell Graph Module
# This uses Microsoft's official PowerShell module which has better security compliance

param(
    [string]$Date = "2025-10-22"
)

Write-Host "🚀 CYL's Microsoft Calendar Analysis - PowerShell Graph Module" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Check if Microsoft.Graph module is installed
$GraphModule = Get-Module -ListAvailable -Name Microsoft.Graph.Calendar
if (-not $GraphModule) {
    Write-Host "❌ Microsoft.Graph.Calendar module not found" -ForegroundColor Red
    Write-Host "💡 To install, run as Administrator:" -ForegroundColor Yellow
    Write-Host "   Install-Module Microsoft.Graph -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

try {
    # Connect to Microsoft Graph
    Write-Host "🔐 Connecting to Microsoft Graph..." -ForegroundColor Yellow
    Connect-MgGraph -Scopes "Calendars.Read", "User.Read" -NoWelcome
    
    # Get current user info
    $User = Get-MgUser -UserId "me" -Property DisplayName, UserPrincipalName
    Write-Host "👤 Authenticated as: $($User.DisplayName) ($($User.UserPrincipalName))" -ForegroundColor Green
    
    # Parse date
    $TargetDate = [DateTime]::Parse($Date)
    $StartTime = $TargetDate.Date.ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    $EndTime = $TargetDate.Date.AddDays(1).AddMilliseconds(-1).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    
    Write-Host "📅 Fetching calendar events for $($TargetDate.ToString('yyyy-MM-dd'))..." -ForegroundColor Yellow
    
    # Get calendar events
    $Events = Get-MgUserCalendarView -UserId "me" -StartDateTime $StartTime -EndDateTime $EndTime -All
    
    if ($Events.Count -eq 0) {
        Write-Host "📭 No meetings found for $($TargetDate.ToString('yyyy-MM-dd'))" -ForegroundColor Yellow
        exit 0
    }
    
    Write-Host "✅ Found $($Events.Count) calendar events" -ForegroundColor Green
    
    # Analyze meetings
    $AcceptedCount = 0
    $TentativeCount = 0
    $DeclinedCount = 0
    $NoResponseCount = 0
    $Collaborators = @()
    
    Write-Host "`n📊 MEETING ANALYSIS:" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    
    foreach ($Event in $Events) {
        $Response = $Event.ResponseStatus.Response
        switch ($Response) {
            "accepted" { $AcceptedCount++ }
            "tentativelyAccepted" { $TentativeCount++ }
            "declined" { $DeclinedCount++ }
            default { $NoResponseCount++ }
        }
        
        # Collect collaborators
        if ($Event.Organizer.EmailAddress.Address) {
            $Collaborators += $Event.Organizer.EmailAddress.Address
        }
        foreach ($Attendee in $Event.Attendees) {
            if ($Attendee.EmailAddress.Address) {
                $Collaborators += $Attendee.EmailAddress.Address
            }
        }
    }
    
    # Display statistics
    Write-Host "   • Total meetings: $($Events.Count)" -ForegroundColor White
    Write-Host "   • ✅ Accepted: $AcceptedCount" -ForegroundColor Green
    Write-Host "   • ❓ Tentative: $TentativeCount" -ForegroundColor Yellow
    Write-Host "   • ❌ Declined: $DeclinedCount" -ForegroundColor Red
    Write-Host "   • ⚪ No response: $NoResponseCount" -ForegroundColor Gray
    Write-Host "   • 👥 Unique collaborators: $(($Collaborators | Sort-Object -Unique).Count)" -ForegroundColor Cyan
    
    # Display today's meetings
    Write-Host "`n📋 TODAY'S MEETINGS:" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    
    $Counter = 1
    foreach ($Event in $Events | Sort-Object { $_.Start.DateTime }) {
        $StartTime = [DateTime]::Parse($Event.Start.DateTime)
        $EndTime = [DateTime]::Parse($Event.End.DateTime)
        $Response = $Event.ResponseStatus.Response
        
        $StatusEmoji = switch ($Response) {
            "accepted" { "✅" }
            "tentativelyAccepted" { "❓" }
            "declined" { "❌" }
            default { "⚪" }
        }
        
        Write-Host "   $Counter. $StatusEmoji $($Event.Subject)" -ForegroundColor White
        Write-Host "      Time: $($StartTime.ToString('HH:mm')) - $($EndTime.ToString('HH:mm')) PDT" -ForegroundColor Gray
        Write-Host "      Response: $Response" -ForegroundColor Gray
        Write-Host ""
        $Counter++
    }
    
    # Flight CI005 conflict analysis
    Write-Host "✈️  FLIGHT CI005 ANALYSIS:" -ForegroundColor Cyan
    Write-Host "=========================" -ForegroundColor Cyan
    Write-Host "   Flight CI005 departs at 4:25 PM PDT today" -ForegroundColor White
    Write-Host "   Checking for meeting conflicts..." -ForegroundColor Yellow
    
    $FlightTime = $TargetDate.Date.AddHours(16).AddMinutes(25)  # 4:25 PM
    $TravelTime = $FlightTime.AddHours(-2)  # Need to leave by 2:25 PM
    
    $Conflicts = @()
    foreach ($Event in $Events) {
        $EndTime = [DateTime]::Parse($Event.End.DateTime)
        if ($EndTime -gt $TravelTime) {
            $Conflicts += @{
                Subject = $Event.Subject
                EndTime = $EndTime.ToString("HH:mm")
                Response = $Event.ResponseStatus.Response
            }
        }
    }
    
    if ($Conflicts.Count -gt 0) {
        Write-Host "   ⚠️  $($Conflicts.Count) potential conflicts found:" -ForegroundColor Red
        foreach ($Conflict in $Conflicts) {
            Write-Host "      • $($Conflict.Subject) (ends $($Conflict.EndTime)) - $($Conflict.Response)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ✅ No meeting conflicts with flight departure" -ForegroundColor Green
    }
    
    # Verification against expected pattern
    Write-Host "`n🔍 VERIFICATION:" -ForegroundColor Cyan
    Write-Host "===============" -ForegroundColor Cyan
    Write-Host "   Expected: 1 accepted + 7 tentative meetings" -ForegroundColor White
    Write-Host "   Found: $AcceptedCount accepted + $TentativeCount tentative meetings" -ForegroundColor White
    
    if ($AcceptedCount -eq 1 -and $TentativeCount -eq 7) {
        Write-Host "   ✅ Perfect match with your calendar check!" -ForegroundColor Green
    } else {
        Write-Host "   ❓ Different from expected - let's verify the data" -ForegroundColor Yellow
    }
    
    # Save data to JSON
    $OutputData = @{
        generated_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        user = "$($User.DisplayName) ($($User.UserPrincipalName))"
        date = $Date
        analysis = @{
            total_meetings = $Events.Count
            accepted_meetings = $AcceptedCount
            tentative_meetings = $TentativeCount
            declined_meetings = $DeclinedCount
            no_response_meetings = $NoResponseCount
            unique_collaborators = ($Collaborators | Sort-Object -Unique).Count
        }
        events = $Events
    }
    
    $OutputFile = "cyl_calendar_powershell_$(Get-Date -Format 'yyyyMMdd').json"
    $OutputData | ConvertTo-Json -Depth 10 | Out-File $OutputFile -Encoding UTF8
    Write-Host "`n💾 Raw data saved to: $OutputFile" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Message -like "*permission*" -or $_.Exception.Message -like "*consent*") {
        Write-Host "💡 Tip: You may need admin consent for the Microsoft Graph PowerShell app" -ForegroundColor Yellow
        Write-Host "   Contact your IT admin or try the Graph Explorer web interface" -ForegroundColor Yellow
    }
} finally {
    # Disconnect
    try {
        Disconnect-MgGraph -ErrorAction SilentlyContinue
    } catch {
        # Ignore disconnect errors
    }
}

Write-Host "`n✅ Calendar analysis completed!" -ForegroundColor Green