from distutils.core import setup
# import setuptools

packages = ['pbix_refresh']
setup(name='pbix_refresh',
      version='0.5.3',
      author='xigua, 刷新Power bi desktop, 已向下兼容旧版power bi ',
      packages=packages,
      package_dir={'requests': 'requests'}, )
