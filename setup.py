import setuptools

juh = 'juh'

setuptools.setup(name=juh,
                 version='1.0.0',
                 description='Jupyter Upload Handler',
                 long_description='',
                 author='Kai Amann',
                 author_email='kai.amann@fau.de',
                 url='https://github.com/KWARC/jupyter-upload-handler',
                 packages=[juh],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 package_data={juh: []},
                 classifiers=['Packages'])
