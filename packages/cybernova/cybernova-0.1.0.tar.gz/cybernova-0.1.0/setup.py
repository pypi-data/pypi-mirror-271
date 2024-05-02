from setuptools import setup, find_packages
from setuptools.command.install import install
import os
class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Assuming __main__.py is in the cybernova/ package directory
        os.chmod(os.path.join(self.install_lib, 'cybernova', '__main__.py'), 0o755)
setup(
    name='cybernova',
    version='0.1.0',  # Initial development version
    author='Aniket Bhardwaj',
    author_email='aniket.bhardwaj0803@gmail.com',
    description='A suite of cybersecurity tools for network analysis and vulnerability scanning.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Aniket-bhardwaj/CyberNova',  # Adjust the URL to your repository
    packages=find_packages(),
    install_requires=[
        
        'python-nmap>=0.7.1',
        'python-whois>=0.9.4',  
        'dnspython>=0.6.30',  
        

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cybernova=cybernova.main:main',  # Adjust if your main function is located elsewhere
        ],
    },
    include_package_data=True,
)
