[CmdletBinding()]
param(
    [ValidateSet("Both", "CLI", "App")]
    [string]$HostTarget = "Both",
    [string]$ReleaseRoot = (Join-Path $HOME ".autodev\releases"),
    [switch]$RepairOwnedDirectCache
)

$ErrorActionPreference = "Stop"
$pathComparison = if ($IsWindows) { [StringComparison]::OrdinalIgnoreCase } else { [StringComparison]::Ordinal }
$source = Join-Path $PSScriptRoot "tkapin-autodev"
$version = (Get-Content -LiteralPath (Join-Path $source "plugin.json") -Raw | ConvertFrom-Json).version
if ($HostTarget -in @("Both", "CLI")) {
    Get-Command copilot -ErrorAction Stop | Out-Null
}
if ($HostTarget -in @("Both", "App")) {
    Get-Command agency -ErrorAction Stop | Out-Null
}

$files = @(Get-ChildItem -LiteralPath $source -File -Recurse -Force |
    Where-Object { $_.FullName -notmatch '[\\/]__pycache__[\\/]' -and $_.Extension -ne ".pyc" } |
    Sort-Object FullName)
if ($files.Count -eq 0) {
    throw "Plugin source is empty: $source"
}
$entries = @()
foreach ($file in $files) {
    if ($file.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw "Linked plugin files are not supported: $($file.FullName)"
    }
    $relative = [IO.Path]::GetRelativePath($source, $file.FullName)
    $entries += "$($relative.Replace('\', '/')) $((Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash)"
}
$hasher = [Security.Cryptography.SHA256]::Create()
try {
    $hash = [Convert]::ToHexString($hasher.ComputeHash([Text.Encoding]::UTF8.GetBytes(($entries -join "`n")))).ToLowerInvariant()
}
finally {
    $hasher.Dispose()
}
$target = Join-Path (Join-Path ([IO.Path]::GetFullPath($ReleaseRoot)) $hash) "tkapin-autodev"
foreach ($file in $files) {
    $relative = [IO.Path]::GetRelativePath($source, $file.FullName)
    $destination = Join-Path $target $relative
    if (Test-Path -LiteralPath $destination) {
        if ((Get-FileHash -LiteralPath $destination).Hash -ne (Get-FileHash -LiteralPath $file.FullName).Hash) {
            throw "Existing immutable release differs: $destination"
        }
    }
    else {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destination) | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $destination
    }
}

if ($HostTarget -in @("Both", "CLI")) {
    $registered = & copilot plugin list --json
    if ($LASTEXITCODE -ne 0) {
        throw "Cannot inspect existing Copilot plugin registrations"
    }
    $entry = @($registered | ConvertFrom-Json | Where-Object {
        $_.name -eq "tkapin-autodev" -and $_.enabled -and $_.version -eq $version
    })
    $copilotHome = if ($env:COPILOT_HOME) { $env:COPILOT_HOME } else { Join-Path $HOME ".copilot" }
    $copilotHome = [IO.Path]::GetFullPath($copilotHome)
    $cache = Join-Path $copilotHome "installed-plugins\_direct\tkapin-autodev"
    $identical = $entry.Count -eq 1 -and (Test-Path -LiteralPath $cache)
    if ($identical) {
        $cachedFiles = @(Get-ChildItem -LiteralPath $cache -File -Recurse -Force |
            Where-Object { $_.FullName -notmatch '[\\/]__pycache__[\\/]' -and $_.Extension -ne ".pyc" })
        $identical = $cachedFiles.Count -eq $files.Count
        foreach ($file in $files) {
            $cached = Join-Path $cache ([IO.Path]::GetRelativePath($source, $file.FullName))
            if (-not (Test-Path -LiteralPath $cached)) {
                $identical = $false
            }
            elseif ($file.Extension -eq ".py") {
                # Git checkout newline normalization does not change Python code.
                $utf8 = [Text.UTF8Encoding]::new($false, $true)
                $actual = $utf8.GetString([IO.File]::ReadAllBytes($cached)).Replace("`r`n", "`n")
                $expected = $utf8.GetString([IO.File]::ReadAllBytes($file.FullName)).Replace("`r`n", "`n")
                if ($actual -cne $expected) { $identical = $false }
            }
            elseif ((Get-FileHash -LiteralPath $cached).Hash -ne (Get-FileHash -LiteralPath $file.FullName).Hash) {
                $identical = $false
            }
        }
    }
    if ($identical) {
        Write-Host "Copilot CLI already has this enabled content (Python newlines normalized); no replacement needed."
    }
    else {
        if ($RepairOwnedDirectCache -and (Test-Path -LiteralPath $cache)) {
            $config = Get-Content -LiteralPath (Join-Path $copilotHome "config.json") -Raw | ConvertFrom-Json
            $owned = @($config.installedPlugins | Where-Object {
                $_.name -eq "tkapin-autodev" -and $_.marketplace -eq "" -and
                $_.source.source -eq "local" -and $_.cache_path -eq $cache
            })
            if ($owned.Count -ne 1) {
                throw "Cannot establish ownership of this direct cache; no files removed."
            }
            $oldSource = [IO.Path]::GetFullPath($owned[0].source.path)
            $ownedRoot = [IO.Path]::GetFullPath($ReleaseRoot).TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
            if (-not $oldSource.StartsWith($ownedRoot, $pathComparison) -or
                (Split-Path -Leaf $oldSource) -ne "tkapin-autodev") {
                throw "The registered source is not an owned immutable release; no files removed."
            }
            $oldFiles = @(Get-ChildItem -LiteralPath $oldSource -File -Recurse -Force |
                Where-Object Extension -ne ".pyc" | Sort-Object FullName)
            $cacheFiles = @(Get-ChildItem -LiteralPath $cache -File -Recurse -Force |
                Where-Object Extension -ne ".pyc")
            $linked = @((Get-Item -LiteralPath $cache), (Get-Item -LiteralPath $oldSource)) +
                @(Get-ChildItem -LiteralPath $cache -Recurse -Force) +
                @(Get-ChildItem -LiteralPath $oldSource -Recurse -Force)
            if ($oldFiles.Count -ne $cacheFiles.Count -or
                @($linked | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
                throw "Cache/source contains unexpected or linked content; no files removed."
            }
            foreach ($compiled in @(Get-ChildItem -LiteralPath $cache -File -Recurse -Force -Filter *.pyc)) {
                $bytecodeMatch = [regex]::Match($compiled.Name, '^(.+)\.cpython-[0-9]+(?:\.opt-[0-9]+)?\.pyc$')
                if ($compiled.Directory.Name -ne "__pycache__" -or
                    -not $bytecodeMatch.Success) {
                    throw "Unexpected bytecode file in cache; no files removed."
                }
                $origin = Join-Path $compiled.Directory.Parent.FullName "$($bytecodeMatch.Groups[1].Value).py"
                $relative = [IO.Path]::GetRelativePath($cache, $origin)
                if (-not (Test-Path -LiteralPath (Join-Path $oldSource $relative))) {
                    throw "Bytecode has no matching source in the owned release; no files removed."
                }
            }
            $oldEntries = @()
            foreach ($file in $oldFiles) {
                $relative = [IO.Path]::GetRelativePath($oldSource, $file.FullName)
                $cached = Join-Path $cache $relative
                $fileHash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
                if (-not (Test-Path -LiteralPath $cached) -or
                    (Get-FileHash -LiteralPath $cached -Algorithm SHA256).Hash -ne $fileHash) {
                    throw "Cached plugin has local changes; preserve and reconcile them before update."
                }
                $oldEntries += "$($relative.Replace('\', '/')) $fileHash"
            }
            $oldHasher = [Security.Cryptography.SHA256]::Create()
            try {
                $oldHash = [Convert]::ToHexString($oldHasher.ComputeHash(
                    [Text.Encoding]::UTF8.GetBytes(($oldEntries -join "`n")))).ToLowerInvariant()
            }
            finally {
                $oldHasher.Dispose()
            }
            if ((Split-Path -Leaf (Split-Path -Parent $oldSource)) -ne $oldHash) {
                throw "Registered source no longer matches its immutable fingerprint; no files removed."
            }
            Remove-Item -LiteralPath $cache -Recurse
            Write-Host "Removed only the verified owned static cache copy; release, project data, and configuration remain intact."
        }
        & copilot plugin install $target
        if ($LASTEXITCODE -ne 0) {
            throw "Copilot CLI plugin installation failed with exit code $LASTEXITCODE; existing sessions/configuration were not forcibly changed"
        }
    }
}
if ($HostTarget -in @("Both", "App")) {
    & agency plugin install "local:$target" --engine copilot
    if ($LASTEXITCODE -ne 0) {
        throw "App host plugin registration failed with exit code $LASTEXITCODE"
    }
    # This app build discovers personal skills but not plugin-bundled skills.
    $skillTarget = Join-Path $target "skills\autodev"
    $personal = Join-Path $HOME ".copilot\skills\autodev"
    if (Test-Path -LiteralPath $personal) {
        $existing = Get-Item -LiteralPath $personal -Force
        if ($existing.LinkType -notin @("Junction", "SymbolicLink")) {
            throw "Refusing to replace an existing personal skill directory: $personal"
        }
        $oldTarget = [IO.Path]::GetFullPath([string]$existing.Target)
        if ($oldTarget -ne $skillTarget) {
            $ownedRoot = [IO.Path]::GetFullPath($ReleaseRoot).TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
            $ownedSuffix = [IO.Path]::Combine("tkapin-autodev", "skills", "autodev")
            if (-not $oldTarget.StartsWith($ownedRoot, $pathComparison) -or
                -not $oldTarget.EndsWith($ownedSuffix, $pathComparison)) {
                throw "Refusing to repoint a personal skill not owned by this installer: $personal"
            }
            Remove-Item -LiteralPath $personal -Force
        }
    }
    if (-not (Test-Path -LiteralPath $personal)) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $personal) | Out-Null
        $linkType = if ($IsWindows) { "Junction" } else { "SymbolicLink" }
        New-Item -ItemType $linkType -Path $personal -Target $skillTarget | Out-Null
    }
}

[PSCustomObject]@{
    Plugin = "tkapin-autodev"
    Version = $version
    ContentHash = $hash
    InstalledSource = $target
    HostTarget = $HostTarget
    AppSkill = if ($HostTarget -in @("Both", "App")) { $personal } else { $null }
    Note = "Use a new host session to load the registered release. No existing session was restarted."
}
