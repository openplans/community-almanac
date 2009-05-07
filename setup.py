try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys
# We monkeypatch setuptools to perform script installs the way distutils does.
# Calling pkg_resources is too time intensive for a serious command line
# applications.
def install_script(self, dist, script_name, script_text, dev_path=None):
    self.write_script(script_name, script_text, 'b')

if sys.platform != 'win32' and 'setuptools' in sys.modules:
    # Someone used easy_install to run this.  I really want the correct
    # script installed.
    import setuptools.command.easy_install
    setuptools.command.easy_install.easy_install.install_script = install_script

setup(
    name='communityalmanac',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
        "Pylons>=0.9.7",
        "SQLAlchemy>=0.5",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'communityalmanac': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'communityalmanac': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=True,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = communityalmanac.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
