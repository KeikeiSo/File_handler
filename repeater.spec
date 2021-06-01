# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['repeater.py'],
             pathex=['C:\\Users\\calli\\OneDrive\\Documents\\GitHub\\File_handler'],
             binaries=[],
             datas=['./pdfhandler.py', './dochandler.py'],
             hiddenimports=['pyttsx3.drivers'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='repeater',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
