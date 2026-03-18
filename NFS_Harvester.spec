# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['harvester.py'],
    pathex=[],
    binaries=[(r".\Pipeline\#ADMIN\DB\MAF 32 Piece Lookup Table.db", r'Pipeline\#ADMIN\DB')],
    datas=[
        (r".\src\_config\logging.yaml", r'src\_config'), 
        (r".\Pipeline\#ADMIN\LOGS\harvester_pipeline.log", r'Pipeline\#ADMIN\DB\LOGS'), 
        (r".\Pipeline\#ADMIN\LOGS\harvester_pipeline_error.log", r'Pipeline\#ADMIN\DB\LOGS'),
    ],
    hiddenimports=[
        "src._tools",
        "src._config",
        "dbm.sqlite3",
        "openpyxl",
        "openpyxl.utils.exceptions",
    ],
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
    a.binaries,
    a.datas,
    [],
    name='NFS_Harvester',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
