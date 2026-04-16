# SmartScreen Directory Organization Script
$rootDir = Get-Location

# Move Documentation Files to docs/
$docFiles = @(
    "README.md", "README_NEW.md", "QUICK_START.md", "QUICK_REFERENCE.md",
    "ADMIN_PANEL_GUIDE.md", "ADMIN_SETUP_QUICK_START.md",
    "API_DOCUMENTATION.md", "API_ENDPOINTS_VERIFICATION.md", "API_MATCHING_COMPLETE.md",
    "API_SYNC_COMPLETION_REPORT.md", "BACKEND_FRONTEND_MATCHING_REPORT.md", "BACKEND_SETUP.md",
    "COMPLETION_CHECKLIST.md", "DEPLOYMENT_GUIDE.md",
    "FRONTEND_API_FIXES_DETAILED.md", "FRONTEND_COMPLETE.md", "FRONTEND_CRITICAL_FIXES.md",
    "IMPLEMENTATION_SUMMARY.md", "PRODUCTION_BACKEND_IMPROVEMENTS.md", "PRODUCTION_STATUS.md",
    "SRS.md", "ATS_Project_Guide.md", "TnP.MD", "plan.md", "synthetic.md", "details.md"
)

Write-Host "Moving documentation files..." -ForegroundColor Cyan
foreach ($file in $docFiles) {
    $source = Join-Path $rootDir $file
    if (Test-Path $source) {
        Move-Item -Path $source -Destination "docs/" -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Moved $file"
    }
}

# Move Script Files to scripts/
$scriptFiles = @(
    "1.py", "check_admin.py", "check_db_urls.py", "create_admin_seed.py",
    "diagnose_backend.py", "diagnostics.py", "fix_startup.py", "test_admin_endpoints.py",
    "test_login.py", "setup.bat", "setup.sh"
)

Write-Host "Moving script files..." -ForegroundColor Cyan
foreach ($file in $scriptFiles) {
    $source = Join-Path $rootDir $file
    if (Test-Path $source) {
        Move-Item -Path $source -Destination "scripts/" -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Moved $file"
    }
}

# Move Test Output Files to tests/
$testFiles = @(
    "test_output.txt", "test_results.txt"
)

Write-Host "Moving test files..." -ForegroundColor Cyan
foreach ($file in $testFiles) {
    $source = Join-Path $rootDir $file
    if (Test-Path $source) {
        Move-Item -Path $source -Destination "tests/" -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Moved $file"
    }
}

# Move Config Files to config/
$configFiles = @(
    ".env.example", "Procfile", "skills.json"
)

Write-Host "Moving config files..." -ForegroundColor Cyan
foreach ($file in $configFiles) {
    $source = Join-Path $rootDir $file
    if (Test-Path $source) {
        Move-Item -Path $source -Destination "config/" -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Moved $file"
    }
}

# Clean up root __pycache__
if (Test-Path "__pycache__") {
    Remove-Item -Recurse -Force "__pycache__" -ErrorAction SilentlyContinue
    Write-Host "✓ Removed __pycache__" -ForegroundColor Green
}

# Clean up smartscreen.db from root (testing only)
if (Test-Path "smartscreen.db") {
    Remove-Item -Force "smartscreen.db" -ErrorAction SilentlyContinue
    Write-Host "✓ Removed smartscreen.db (test database)" -ForegroundColor Green
}

Write-Host "`n✅ Directory organization complete!" -ForegroundColor Green
Write-Host "`nNew Structure:" -ForegroundColor Yellow
Write-Host "  SmartScreen/" -ForegroundColor White
Write-Host "    ├── backend/          (FastAPI application)" -ForegroundColor Gray
Write-Host "    ├── frontend/         (React application)" -ForegroundColor Gray
Write-Host "    ├── docs/             (All documentation)" -ForegroundColor Gray
Write-Host "    ├── scripts/          (Utility and setup scripts)" -ForegroundColor Gray
Write-Host "    ├── tests/            (Test files and results)" -ForegroundColor Gray
Write-Host "    ├── config/           (Configuration files)" -ForegroundColor Gray
Write-Host "    ├── .env              (Environment variables)" -ForegroundColor Gray
Write-Host "    └── requirements.txt" -ForegroundColor Gray
