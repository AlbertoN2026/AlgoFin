[app]

# 1. Configurações Básicas
title = AlgoFin
package.name = algofinteste
package.domain = br.com.aldair
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.2

# 2. Requisitos: Limpos e Sem Travas de Versão do Python
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,urllib3,certifi,idna,charset-normalizer

# 3. Configurações do Android
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

# 4. A MÁQUINA DO TEMPO: O Segredo do Sucesso
# Esta linha trava o motor de compilação em Janeiro de 2024, muito antes do Python 3.14 existir!
p4a.branch = v2024.01.21

[buildozer]
# 5. Configurações de Log
log_level = 2
warn_on_root = 1