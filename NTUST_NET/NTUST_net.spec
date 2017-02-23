# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\steve\\Desktop\\Program\\NTUST_NET\\NTUST_net.py'],
             pathex=['C:\\Users\\steve\\Desktop\\Program\\NTUST_NET'],
             binaries=[],
             datas=[],
             hiddenimports=['queue'],
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
          name='NTUST_net',
          debug=False,
          strip=False,
          upx=True,
          console=True )
