@echo off
chcp 65001 >nul
title 도로 파일 랜덤 Y값 수정 프로그램
color 0A

:MENU
cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║              도로 파일 랜덤 Y값 수정 프로그램              ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 📁 작업 폴더: %~dp0
echo.
echo [1] 파일 수정 실행 (5cm이상 ~ 10cm 이하 과속방지턱 생성)
echo [2] 파일 수정 실행 (10cm이상 ~ 25cm 이하 과속방지턱 생성)
echo [3] 파일 수정 실행 (0cm 과속방지턱)
echo [4] 생성된 파일 확인
echo [5] 종료
echo.
set /p choice=선택하세요 (1-5): 

if "%choice%"=="1" goto RUN_SCRIPT_1
if "%choice%"=="2" goto RUN_SCRIPT_2
if "%choice%"=="3" goto RUN_SCRIPT_3
if "%choice%"=="4" goto CHECK_FILES
if "%choice%"=="5" goto EXIT
echo 잘못된 선택입니다. 다시 시도하세요.
timeout /t 2 >nul
goto MENU

:RUN_SCRIPT_1
cls
echo.
echo 🔄 파일 수정을 시작합니다... (5cm이상 ~ 10cm 이하 과속방지턱 생성)
echo.
python "%~dp0vroad_modifier.py" 1
goto END_SCRIPT

:RUN_SCRIPT_2
cls
echo.
echo 🔄 파일 수정을 시작합니다... (10cm이상 ~ 25cm 이하 과속방지턱 생성)
echo.
python "%~dp0vroad_modifier.py" 2
goto END_SCRIPT

:RUN_SCRIPT_3
cls
echo.
echo 🔄 파일 수정을 시작합니다... (0cm 과속방지턱)
echo.
python "%~dp0vroad_modifier.py" 3
goto END_SCRIPT

:END_SCRIPT
if %errorlevel% neq 0 (
    echo.
    echo ❌ 오류가 발생했습니다!
    echo - Python이 설치되어 있는지 확인해주세요
    echo - vroad_modifier.py 파일이 있는지 확인해주세요
    echo - 원본 파일 경로가 올바른지 확인해주세요
    echo.
) else (
    echo.
    echo ✅ 작업이 성공적으로 완료되었습니다!
    echo.
)

echo 아무 키나 눌러 메뉴로 돌아가세요...
pause >nul
goto MENU

:CHECK_FILES
cls
echo.
echo 📂 생성된 파일 목록:
echo.
dir "수정된_*.vroad" /b 2>nul
if %errorlevel% neq 0 (
    echo 아직 생성된 파일이 없습니다.
) else (
    echo.
    echo 위 파일들이 생성되었습니다.
)
echo.
echo 아무 키나 눌러 메뉴로 돌아가세요...
pause >nul
goto MENU

:EXIT
echo.
echo 👋 프로그램을 종료합니다.
timeout /t 1 >nul
exit