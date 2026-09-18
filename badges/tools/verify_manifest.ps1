param([string]$BadgeRoot = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'
$assetRoot = (Resolve-Path -LiteralPath $BadgeRoot).Path
$manifest = Get-Content -LiteralPath (Join-Path $assetRoot 'manifest.json') -Raw -Encoding utf8 | ConvertFrom-Json
$catalog = Get-Content -LiteralPath (Join-Path $assetRoot 'data/catalog.json') -Raw -Encoding utf8 | ConvertFrom-Json
$fixtures = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'import-fixtures.json') -Raw -Encoding utf8 | ConvertFrom-Json
$baseUrl = 'https://raw.githubusercontent.com/s09x/Nuvio-Assets/main/badges/'
$compiled = @{}
$groupIds = @($manifest.groups | ForEach-Object { $_.id })
if ($manifest.filters.Count -ne 1037 -or $manifest.groups.Count -ne 37) { throw 'Incomplete import catalog.' }
$expectedIds = @($catalog.items | ForEach-Object { $_.id } | Sort-Object)
$actualIds = @($manifest.filters | ForEach-Object { $_.id } | Sort-Object)
if (Compare-Object $expectedIds $actualIds) { throw 'Import IDs differ from the artwork catalog.' }
foreach ($filter in $manifest.filters) {
    if ($compiled.ContainsKey($filter.id)) { throw "Duplicate filter: $($filter.id)" }
    if ([string]::IsNullOrWhiteSpace($filter.name) -or [string]::IsNullOrWhiteSpace($filter.pattern)) { throw 'Unusable filter.' }
    if ($filter.groupId -notin $groupIds -or $filter.isEnabled -ne $true) { throw "Invalid filter settings: $($filter.id)" }
    if (-not $filter.imageURL.StartsWith($baseUrl, [System.StringComparison]::Ordinal)) { throw "Unexpected image host: $($filter.id)" }
    $imageRelative = $filter.imageURL.Substring($baseUrl.Length)
    $imagePath = [System.IO.Path]::GetFullPath((Join-Path $assetRoot $imageRelative))
    if (-not $imagePath.StartsWith($assetRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase) -or -not (Test-Path -LiteralPath $imagePath -PathType Leaf)) { throw "Missing image: $($filter.id)" }
    $compiled[$filter.id] = [System.Text.RegularExpressions.Regex]::new($filter.pattern, [System.Text.RegularExpressions.RegexOptions]::CultureInvariant, [TimeSpan]::FromMilliseconds(500))
}
$failures = [System.Collections.Generic.List[object]]::new()
$results = [System.Collections.Generic.List[object]]::new()
$started = [System.Diagnostics.Stopwatch]::StartNew()
foreach ($fixture in $fixtures) {
    $candidates = @($fixture.candidates | ForEach-Object { $_.Trim() } | Where-Object { $_ } | Select-Object -Unique)
    if ($candidates.Count -gt 1) { $candidates += ($candidates -join ' ') }
    $matched = [System.Collections.Generic.HashSet[string]]::new()
    foreach ($filter in $manifest.filters) {
        foreach ($candidate in $candidates) {
            if ($compiled[$filter.id].IsMatch($candidate)) { [void]$matched.Add($filter.id); break }
        }
    }
    $missing = @($fixture.required | Where-Object { -not $matched.Contains($_) })
    $unexpected = @($fixture.forbidden | Where-Object { $matched.Contains($_) })
    $case = [pscustomobject]@{ name=$fixture.name; missing=$missing; forbidden_matches=$unexpected; passed=($missing.Count -eq 0 -and $unexpected.Count -eq 0) }
    $results.Add($case)
    if (-not $case.passed) { $failures.Add($case) }
}
$started.Stop()
$report = [pscustomobject]@{
    status = $(if ($failures.Count) { 'failed' } else { 'passed' })
    schema = 'Nuvio/Fusion filters and groups, checked against the inspected Kotlin model'
    filter_count = $manifest.filters.Count
    group_count = $manifest.groups.Count
    all_regexes_compiled = $true
    all_image_paths_resolve_locally = $true
    regex_validation_engine = '.NET regular expressions with the shared Unicode property, lookaround and inline-case syntax'
    fixtures_are_synthetic = $true
    fixture_count = $fixtures.Count
    fixture_run_milliseconds = $started.ElapsedMilliseconds
    fixture_results = $results
    client_device_import_test = 'not performed'
}
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $assetRoot 'data/import-verification.json') -Encoding utf8NoBOM
[pscustomobject]@{ filters=$manifest.filters.Count; groups=$manifest.groups.Count; synthetic_cases=$fixtures.Count; elapsed_ms=$started.ElapsedMilliseconds; failures=$failures } | ConvertTo-Json -Depth 8
if ($failures.Count) { throw 'Import behavior checks failed.' }
