@echo off
echo [1/3] Running Python Script...
python update_json.py

echo [2/3] Adding changes to Git...
git add .

set /p msg="Enter Commit Message (e.g. Add 2026 series): "
git commit -m "%msg%"

echo [3/3] Pushing to GitHub...
git push

echo Update Complete!
pause