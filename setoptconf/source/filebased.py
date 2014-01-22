import os.path

from copy import deepcopy

from ..config import Configuration
from .base import Source


__all__ = (
    'FileBasedSource',
)


class FileBasedSource(Source):
    def __init__(self, files, base_path=None, combine=False):
        super(FileBasedSource, self).__init__()

        if isinstance(files, (list, tuple)):
            self.files = files
        elif isinstance(files, basestring):
            self.files = [files]
        else:
            raise TypeError('files must be a string or list of strings')

        self.base_path = base_path or os.getcwd()
        self.combine = combine

    def get_config(self, settings, manager=None, parent=None):
        parsed_settings = []

        for file_source in self.files:
            if os.path.isabs(file_source):
                file_path = file_source
            else:
                file_path = os.path.join(self.base_path, file_source)

            if os.path.exists(file_path):
                file_settings = self.get_settings_from_file(
                    file_path,
                    deepcopy(settings),
                    manager=manager,
                )

                if file_settings:
                    parsed_settings.append(file_settings)

                    if not self.combine:
                        # No need to gather any more, we only want one.
                        break

        if parsed_settings:
            config = parent
            for parsed_setting in reversed(parsed_settings):
                config = Configuration(
                    settings=parsed_setting,
                    parent=config,
                )

        else:
            config = Configuration(settings=settings, parent=parent)

        return config

    def get_settings_from_file(self, file_path, settings, manager=None):
        raise NotImplementedError()
