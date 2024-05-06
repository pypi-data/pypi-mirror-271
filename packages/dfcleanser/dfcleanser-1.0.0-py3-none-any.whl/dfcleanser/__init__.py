name = "dfcleanser"

def _jupyter_server_extension_paths():
    return [{
        "module": "dfcleanser"
    }]

# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `my_fancy_module` directory
        src="static",
        # directory in the `nbextension/` namespace
        dest="dfcleanser",
        # _also_ in the `nbextension/` namespace
        require="dfcleanser/index")]

def load_jupyter_server_extension(nbapp):
    nbapp.log.info("dfcleanser enabled!")


# Logger config
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter('dfcleanser %(levelname)s — %(name)s — %(message)s'))
logger.addHandler(sh)    