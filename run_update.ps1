$emailRegex = '(?s)<a href="mailto:[^"]+"[^>]*aria-label="Email"[^>]*>.*?</a>'
$linkedinRegex = '(?s)<a href="https://www\.linkedin\.com/[^"]+"[^>]*aria-label="LinkedIn"[^>]*>.*?</a>'
$githubRegex = '(?s)(<a href="https://github\.com/[^"]+"[^>]*aria-label="GitHub")([^>]*>)'

$newEmail = '<a href="mailto:luanlaguna7@gmail.com" aria-label="Email" class="tooltip-wrap" data-tooltip="Gmail">
              <svg viewBox="0 0 40 40" class="social-icon g-icon" style="border-radius: 8px;">
                <rect width="40" height="40" rx="8" fill="#ffffff" />
                <path d="M7 12 L20 22 L33 12 V28 H7 Z" fill="#f4f6f8"/> 
                <path d="M7 12 L20 22 L20 26 L7 16 Z" fill="#ea4335"/>
                <path d="M7 12 H11 V28 H7 Z" fill="#ea4335"/>
                <path d="M33 12 L20 22 L20 26 L33 16 Z" fill="#4285f4"/>
                <path d="M29 12 H33 V28 H29 Z" fill="#4285f4"/>
              </svg>
            </a>'

$newLinkedin = '<a href="https://www.linkedin.com/in/luan-laguna-390032174/" target="_blank" rel="noopener" aria-label="LinkedIn" class="tooltip-wrap" data-tooltip="LinkedIn">
              <svg viewBox="0 0 40 40" class="social-icon in-icon" style="border-radius: 8px;">
                <rect width="40" height="40" rx="8" fill="#0A66C2" />
                <path d="M12.5 14.5c1.8 0 2.9-1.2 2.9-2.7 0-1.5-1.1-2.7-2.8-2.7s-2.9 1.2-2.9 2.7c0 1.5 1.1 2.7 2.8 2.7zm-2.2 4.1h4.5v14.1h-4.5V18.6zm13.1-4.7c-2.4 0-3.5 1.3-4.1 2.3v-2h-4.5c.1 1.3 0 14.1 0 14.1h4.5v-7.9c0-4.2 2.2-5 3.5-5 1.4 0 2.6 1 2.6 4.3v8.6h4.5v-9c0-4.8-2.6-7.4-6.5-7.4z" fill="#FFF"/>
              </svg>
            </a>'

Get-ChildItem -Path . -Filter *.html -Recurse | ForEach-Object {
    $content = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
    
    $content = $content -replace $emailRegex, $newEmail
    $content = $content -replace $linkedinRegex, $newLinkedin
    
    if (-not ($content -match 'data-tooltip="GitHub"')) {
        $content = $content -replace $githubRegex, '$1 class="tooltip-wrap" data-tooltip="GitHub"$2'
    }
    
    if ($_.Name -eq "projects.html") {
        $content = $content.Replace('<div class="proj-img-placeholder">OpsQuery &mdash; screenshot coming soon</div>', '<img src="assets/projects/opsquery-hero.jpg.jpg" alt="OpsQuery project" />')
        
        $brmRegex = '(?s)<div class="archive-icon" aria-hidden="true">\s*<!-- Settings / operations icon -->\s*<svg viewBox="0 0 24 24">.*?</svg>\s*</div>'
        $brmRepl = '<div class="archive-icon proj-img-wrap" aria-hidden="true" style="padding: 0; background: none; border-radius: 8px; width: 100%; height: auto;"><img src="assets/projects/brmachine-dashboard.jpg" alt="BRMachine Dashboard" style="display:block;" /></div>'
        $content = $content -replace $brmRegex, $brmRepl
    }
    
    if ($_.Name -eq "opsquery.html") {
        $content = $content.Replace('<div class="detail-image-placeholder">OpsQuery &mdash; screenshot coming soon</div>', '<img src="../assets/projects/opsquery-hero.jpg.jpg" alt="OpsQuery project" />')
    }
    
    if ($_.Name -eq "restaurant-platform.html") {
        $content = $content.Replace('<img src="../assets/projects/ordering-platform.jpg"', '<img src="../assets/projects/restaurant-hero.jpg.jpg"')
    }

    [System.IO.File]::WriteAllText($_.FullName, $content, [System.Text.Encoding]::UTF8)
}
Write-Output "HTML files updated"
