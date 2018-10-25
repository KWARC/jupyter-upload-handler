import os
import io
import requests
import urllib

from tornado import web
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from notebook.notebookapp import NotebookApp
from urllib.parse import urlparse

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
        URL = self.get_query_argument("url")
        notebook = requests.get(URL).text
        a = urlparse(URL)
        base = os.path.basename(a.path)
        baseFilename, extension = os.path.splitext(base)

        # if the file alredy exists slap some numbers on the name
        fileNumber = 1
        filename = base
        while os.path.isfile(filename+extension): 
            filename = baseFilename + "("+str(fileNumber)+")"
            fileNumber = fileNumber + 1

        # save the notebook
        with io.open(filename+extension, 'w', encoding='utf-8') as f:
            f.write(notebook)

        # and open it in the browser
        try:
            url = ENDING[extension[1:]]
        except KeyError:
            url = "edit"
        self.redirect("/%s/%s%s" % (url, filename, extension))


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
