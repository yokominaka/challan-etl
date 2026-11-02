# run_project.ps1 - Automated Execution Script for E-Challan Pipeline

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  PUNJAB TRAFFIC E-CHALLAN ETL & EDA AUTOMATED RUNNER    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Start FastAPI Mock Server in the background
Write-Host "`n[1/4] Starting FastAPI Mock Server..." -ForegroundColor Green
$serverProcess = Start-Process python -ArgumentList "-m uvicorn api.main:app --host 127.0.0.1 --port 8000" -PassThru -WindowStyle Hidden

# Allow server time to initialize
Write-Host "Waiting 3 seconds for server startup..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

try {
    # 2. Run ETL Pipeline
    Write-Host "`n[2/4] Executing ETL Pipeline (Extract -> Transform -> Load)..." -ForegroundColor Green
    python main.py
    
    if ($LASTEXITCODE -ne 0) {
        throw "ETL Pipeline execution failed."
    }

    # 3. Execute EDA Analytics & Export Figures
    Write-Host "`n[3/4] Generating Visualizations and Exporting Figures..." -ForegroundColor Green
    python scripts/eda.py
    
    if ($LASTEXITCODE -ne 0) {
        throw "EDA Script execution failed."
    }

    Write-Host "`n[4/4] Pipeline Run Completed Successfully!" -ForegroundColor Green
    Write-Host "High-res plots exported to: reports/figures/" -ForegroundColor Cyan

} catch {
    Write-Host "`nError encountered during execution: $_" -ForegroundColor Red
} finally {
    # 4. Clean up background process
    Write-Host "`nTerminating background FastAPI server (PID: $($serverProcess.Id))..." -ForegroundColor Yellow
    Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
    Write-Host "Shutdown complete." -ForegroundColor Green
}