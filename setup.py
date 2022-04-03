from cx_Freeze import setup, Executable

base = None
executables = [Executable('systeme-suisse.py', base=base)]
packages=['cx_Freeze', 'os', 'sys', 'random', 'time', 'itertools', 'faker']

options = {
    'build.exe':{
        'packages':packages,
    },
}

setup(
    name = "Systeme-Suisse",
    options = options,
    version = "0.1",
    description = "Système suisse de tournoi",
    executables = executables
)