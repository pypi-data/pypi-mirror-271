project('pyJHTDB C extensions', 'c')

py_mod = import('python')
py = py_mod.find_installation()
py_dep = py.dependency()
incdir = include_directories('pyJHTDB/lib/turblib')


py.extension_module(
  'libJHTDB',
  ['pyJHTDB/lib/C/local_tools.c', 'pyJHTDB/lib/turblib/turblib.c', 'pyJHTDB/lib/turblib/soapC.c', 'pyJHTDB/lib/turblib/soapClient.c', 'pyJHTDB/lib/turblib/stdsoap2.c'],
  dependencies: py_dep,
  install: true,
  install_dir: meson.source_root() / 'pendulum/lib/',
  include_directories: incdir
)