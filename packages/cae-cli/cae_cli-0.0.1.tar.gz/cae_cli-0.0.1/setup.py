from setuptools import setup


setup(name='cae-cli',
    version='0.0.1',
    license='Apache License',
    author='Carlos Vinicius Da Silva',
    long_description="teste da aplicação ainda",
    long_description_content_type="text/markdown",
    author_email='vini989073599@gmail.com',
    keywords='cae-cli',
    description=u'o cae tem como objetivo facilitar a utilização de projeto com arquitetura limpa',
    packages=['cae_cli', 'cae_cli.templates'],
    install_requires=[
        'arch-flow>=0.1.4',  # Dependência do cae-cli
        'colorama>=0.4.4'  # Dependência do arch-flow
      ],
)