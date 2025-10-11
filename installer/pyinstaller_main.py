# https://pyinstaller.org/en/stable/usage.html#shortening-the-command

import PyInstaller.__main__
import os

if __name__ == "__main__":
    # Start main application
    script_dn = os.path.dirname(os.path.abspath(__file__))
    main_dn = script_dn[0:script_dn.rindex("\\")]
    main_fn = os.path.join(main_dn, "main.py")

    PyInstaller.__main__.run([
    main_fn,
    '--onefile',
    '--add-data=data.json;.',
    # '--windowed',
    '--icon=installer\\icon.ico',
    ])


