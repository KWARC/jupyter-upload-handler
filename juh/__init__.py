import os
import io
import requests
import urllib
import json

from tornado import web
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from notebook.notebookapp import NotebookApp
from urllib.parse import urlparse
from base64 import b64decode

base_path = os.path.dirname(__file__)
template_path = os.path.join(base_path, 'templates')
static_path = os.path.join(base_path, 'files', 'build')

ENDING = {
    "ipynb" : "notebooks"
}

class JupyterUploadHandler(IPythonHandler):
    @web.authenticated
    def get(self, *args, **kwwargs):
        # get the requested notebook
        prefix = os.getenv('UPLOAD_REDIRECT_PREFIX','')

        URL = self.get_query_argument('url')
        if URL.startswith('data'):
            base_filename = 'Untitled'
            header, encoded = URL.split(',', 1)
            _, extension = header.split('/', 1)
            extension = ".%s" % (extension[:-1])
            data = b64decode(encoded).decode('utf-8')
        
        else:
            data = requests.get(URL).text
            a = urlparse(URL)
            b = os.path.basename(a.path)
            base_filename, extension = os.path.splitext(b)

        # if the file alredy exists add some numbers
        fileNumber = 1
        filename = base_filename
        while os.path.isfile("%s%s" % (filename,extension)):
            filename = base_filename + "("+str(fileNumber)+")"
            fileNumber += 1

        # save the notebook
        with io.open("%s%s" % (filename,extension), 'w', encoding='utf-8') as f:
            f.write(data)

        # and open it in the browser
        try:
            url = ENDING[extension[1:]]
        except KeyError:
            url = "edit"
        self.redirect("%s/%s/%s%s" % (prefix, url, filename, extension))


def _jupyter_server_extension_paths():
    return [
        {'module': 'juh'}
    ]


def load_jupyter_server_extension(nb_server_app: NotebookApp):
    web_app = nb_server_app.web_app

    env = web_app.settings['jinja2_env']
    if hasattr(env.loader, 'loaders'):
        loaders = env.loader.loaders
    else:
        loaders = [env.loader]

    for loader in loaders:
        if hasattr(loader, 'searchpath'):
            loader.searchpath.append(template_path)
    web_app.settings['template_path'].append(template_path)

    web_app.settings['static_path'].append(static_path)

    base_url = web_app.settings.get('base_url', '/')
    handlers = [
        (url_path_join(base_url, '/upload'), JupyterUploadHandler,
         {})
    ]

    web_app.add_handlers('.*$', handlers)
