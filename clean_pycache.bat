@echo off
echo Deleting all __pycache__ folders, excluding .git directories...

:: __pycache__ 디렉토리를 검색 및 삭제
for /d /r %%d in (__pycache__) do (
    :: .git 경로인지 확인하고 제외
    echo %%d | findstr /i "\\.git\\" >nul
    if errorlevel 1 (
        echo Deleting %%d
        rmdir /s /q "%%d"
    ) else (
        echo Skipping %%d as it is inside a .git directory
    )
)

echo Cleanup completed.
pause
