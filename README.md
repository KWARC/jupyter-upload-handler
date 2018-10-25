# jupyter-upload-handler

This repository contains an extension for uploading files to a Jupyter server.

### Installing & Enabling the Server extension

```
    python setup.py install
    
    jupyter serverextension enable --py juh --sys-prefix
```

## Usage

To run a notebook with the extension run:

```
    jupyter notebook
```

To upload a file to your Jupyter server navigate to http://localhost:8080/upload?url=fileURL where `fileURL` is the URL where the file you want to upload is stored. 
If you are running via JupyterHub you can instead go to http://localhost:8080/user-redirect/upload?url=fileURL. The extension will automatically redirect you to the uploaded file.