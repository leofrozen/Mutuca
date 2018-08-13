# -*- mode: python -*-

block_cipher = None

added_files = [
         ( 'multimedia', 'multimedia' ),
         ( 'icon.png', '.' ),
         ( 'gameStages/maps', 'gameStages/maps' ),
         ( 'gameconfig/DATA.mut', 'gameconfig' ),
	 ( 'gameconfig/SAVE.mut', 'gameconfig' )
         ]

a = Analysis(['main.py'],
             pathex=['/home/frozen/pyinstaller/Mutuca/'],
             binaries=None,
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Mutuca_Portable',
          debug=False,
          strip=False,
          upx=True,
          console=False )
