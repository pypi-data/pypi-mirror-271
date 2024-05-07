from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='heartbeat-library',
    version='0.0.1',
    license='MIT License',
    author='Pedro Ferreira Braz',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='pbraz.pedrof@gmail.com',
    keywords='heartbeat, heartbeat-library, heartbeat-api, heartbeat-wrapper, heartbeat-python, heartbeat-python-wrapper, heartbeat-python-api, heartbeat-python-wrapper-api, heartbeat-python-api-wrapper, multithreading, threading, requests, python-requests, python-threading, python-multithreading, python-heartbeat, python-heartbeat-api, python-heartbeat-wrapper, python-heartbeat-python, python-heartbeat-python-wrapper, python-heartbeat-python-api, python-heartbeat-python-wrapper-api, python-heartbeat-python-api-wrapper',
    description=u'Library for sending pulses to a process monitoring server',
    packages=['heartbeat-library'],
    install_requires=['requests', 'threading'],)



