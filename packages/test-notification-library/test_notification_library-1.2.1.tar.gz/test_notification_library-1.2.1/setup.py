from setuptools import setup, find_packages

setup(
    name='test-notification-library',
    version='1.2.1',
    description='Library for sending notifications to different platforms during or after Robot Framework tests execution.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/barbosamp/robotframework-testnotification.git',
    author='Marcos Barbosa',
    author_email='mpbarbosa_@outlook.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    keywords='robotframework testing automation notification',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-telegram-bot',
    ],
    python_requires='>=3.6',
)

