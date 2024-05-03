# -*- coding: utf-8 -*-

import os
import logging
from glob import glob
from importlib import import_module
from importlib.util import find_spec as importlib_find
from oncall_slackbot import settings

logger = logging.getLogger(__name__)


class PluginsManager:
    def __init__(self):
        pass

    commands = {"respond_to": {}, "listen_to": {}, "default_reply": {}}

    def init_plugins(self):
        if hasattr(settings, "PLUGINS"):
            plugins = settings.PLUGINS
        else:
            plugins = "slackbot.plugins"

        for plugin in plugins:
            self._load_plugins(plugin)

    @staticmethod
    def _load_plugins(plugin):
        logger.info('loading plugin "%s"', plugin)
        path_name = importlib_find(plugin)
        try:
            path_name = path_name.submodule_search_locations[0]
        except TypeError:
            path_name = path_name.origin

        module_list = [plugin]
        if not path_name.endswith(".py"):
            module_list = glob("{}/[!_]*.py".format(path_name))
            module_list = [
                ".".join((plugin, os.path.split(f)[-1][:-3])) for f in module_list
            ]
        for module in module_list:
            try:
                import_module(module)
            except Exception:  # pylint: disable=broad-except
                # TODO Better exception handling
                logger.exception("Failed to import %s", module)

    def get_plugins(self, category, text):
        has_matching_plugin = False
        if text is None:
            text = ""
        for matcher in self.commands[category]:
            match = matcher.search(text)
            if match:
                has_matching_plugin = True
                yield self.commands[category][matcher], match.groups()

        if not has_matching_plugin:
            yield None, None
