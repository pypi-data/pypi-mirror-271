from setuptools import setup, find_packages

setup(name='joaomarcosbraz',
    version='0.1.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author='João Marcos Braz',
    author_email='jbrazm.dev@gmail.com',
    description='Um simples pacote de Hello World',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)