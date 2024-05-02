import abc
from jtd_codebuild.component import Component


class Preset(Component, metaclass=abc.ABCMeta):
    def generate(self, cwd: str, **options):
        raise NotImplementedError
