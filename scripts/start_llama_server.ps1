$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ModelPath = Join-Path $ProjectRoot "models\Qwen3-8B-Q5_K_M.gguf"



# Change this to the directory containing llama-server.exe.
$LlamaCppDirectory = "D:\Programming\Projects\MultiAgent Financial Analyst\llama_cpp"

$ServerExecutable = Join-Path $LlamaCppDirectory "llama-server.exe"

if (-not (Test-Path $ServerExecutable)) {
    throw "llama-server.exe was not found at: $ServerExecutable"
}

if (-not (Test-Path $ModelPath)) {
    throw "The Qwen model was not found at: $ModelPath"
}

Write-Host "Starting local Qwen3-8B server..."
Write-Host "Model: $ModelPath"
Write-Host "Endpoint: http://127.0.0.1:8080"


$ChatTemplateArgs = '{\"enable_thinking\":false}'


& $ServerExecutable `
    --model $ModelPath `
    --alias "qwen3-8b" `
    --host "127.0.0.1" `
    --port 8080 `
    --ctx-size 8192 `
    --n-gpu-layers 99 `
    --batch-size 512 `
    --ubatch-size 256 `
    --jinja `
    --flash-attn on `
    --threads 6 `
    --parallel 1 `
    --chat-template-kwargs $ChatTemplateArgs