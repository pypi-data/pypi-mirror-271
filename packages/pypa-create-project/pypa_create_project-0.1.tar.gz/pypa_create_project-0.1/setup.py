from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
        name='pypa-create-project',
        version='0.1',
        license='MIT',
        description=readme(),
        author='Kevin Alexander Krefting',
        author_email='linuxdevalex@outlook.de',
        url='https://github.com/androlinuxs/pypa-create-project',
        scripts=['pypa-create-project', 'pypa'],
        classifiers=[
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'Programming Language :: Python :: 3'
        ]
)
