# Simplest possible .spec file with only dynamic modules
import os
import glob

block_cipher = None

# Automatically discover all provider modules
provider_files = glob.glob('az/*_provider.py')
hidden_imports = [f'az.{os.path.basename(f)[:-3]}' for f in provider_files]

a = Analysis(
    ['az/az.py'],  # Entry point script
    pathex=[],  # Default path
    binaries=[],  # No extra binaries
    datas=[],  # No extra data files
    hiddenimports=hidden_imports,  # Dynamically include modules
    hookspath=[],  # No custom hooks
    excludes=[],  # No exclusions
    runtime_hooks=[],  # No runtime hooks
    noarchive=False,  # Default archive behavior
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='az',  # Output binary name
    debug=False,
    onefile=True,
    console=True,  # Keep the console for debugging
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,  # Default behavior
    upx=True,  # Compress using UPX (if available)
    name='az',  # Output directory name
)
