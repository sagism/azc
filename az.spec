# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['az/az.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['az.anthropic_provider', 'az.gemini_provider', 'az.grok_provider', 'az.llm_provider', 'az.ollama_provider', 'az.openai_provider'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='az',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='az',
)
