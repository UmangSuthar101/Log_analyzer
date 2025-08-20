# log_analyzer/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Dict, Any, List

# package-relative imports (match your folder layout)
from parser import parse_log_line
from test_parser import analyze_logs  # move this to a real module later

app = FastAPI()
_last_summary: Dict[str, Any] = {}

@app.get("/healthz")
def health() -> Dict[str, str]:
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_log(file: UploadFile = File(...)) -> Dict[str, Any]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="file is required")

    content = await file.read()
    try:
        lines: List[str] = content.decode().splitlines()
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="file must be utf-8 text")

    parsed_logs = []
    skipped = 0
    for line in lines:
        log = parse_log_line(line)
        if log:
            parsed_logs.append(log)
        else:
            skipped += 1

    if not parsed_logs:
        raise HTTPException(status_code=422, detail="no valid logs found")

    result = analyze_logs(parsed_logs)
    result["skipped_lines"] = skipped

    global _last_summary
    _last_summary = result
    return result

@app.get("/summary")
def get_last_summary() -> Dict[str, Any]:
    return _last_summary or {"message": "no analysis performed yet"}

# for local docker run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("log_analyzer.main:app", host="0.0.0.0", port=8000)
