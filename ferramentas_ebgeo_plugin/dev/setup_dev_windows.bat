@echo off
setlocal

rem === Se não tem argumento, ainda não foi elevado — salva o perfil e relança ===
if "%~1"=="" (
    net session >nul 2>&1
    if %errorlevel% neq 0 (
        powershell -Command "Start-Process '%~f0' -ArgumentList '%USERPROFILE%' -Verb RunAs"
        exit /b
    )
)

rem === Define o perfil: usa argumento se foi passado, senão usa variável atual ===
if not "%~1"=="" (
    set "_userprofile=%~1"
) else (
    set "_userprofile=%USERPROFILE%"
)

rem === Caminhos ===
set "_updir=%~dp0"
for %%a in ("%_updir%\..") do set "_dir=%%~dpa"

set "link_path=%_userprofile%\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\ferramentas_ebgeo_plugin"
set "target_path=%_dir%ferramentas_ebgeo_plugin"

echo Criando link:
echo   De: "%target_path%"
echo   Para: "%link_path%"
echo.

if exist "%link_path%" (
    echo O link ou pasta já existe: "%link_path%"
    echo Remova-o manualmente se quiser recriar.
    pause
    exit /b
)

mklink /D "%link_path%" "%target_path%"
if errorlevel 1 (
    echo Erro ao criar o link.
) else (
    echo Link criado com sucesso!
)
pause