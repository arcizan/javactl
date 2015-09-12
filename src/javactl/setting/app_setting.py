from __future__ import division, print_function, absolute_import, unicode_literals

import os
from javactl.util import CaseClass, normalize_path, omap, oget


class AppSetting(CaseClass):
    def __init__(self, name=None, home=None, jar=None, entry_point=None, command=None, pid_file=None):
        # constraints
        assert name is not None, 'app.name is required'
        assert home is not None, 'app.home is required'
        assert os.path.isabs(home), 'app.home must be an absolute path'
        assert (jar is None) != (command is None), 'Either app.jar or app.command but not both must be given'
        assert jar is not None or entry_point is None, 'app.entry_point must be used with app.jar'

        normalize = lambda p: normalize_path(p, home)

        CaseClass.__init__(
            self,
            ('name', name),
            ('home', home),
            ('jar', omap(normalize, jar)),
            ('entry_point', entry_point),
            ('command', omap(normalize, command)),
            ('pid_file', omap(normalize, pid_file))
        )

    def is_duplicate_allowed(self):
        return self.pid_file is not None

    def get_args(self, java_executable):
        if self.jar is not None:
            if self.entry_point is not None:
                return [java_executable, '-cp', self.jar, self.entry_point]
            else:
                return [java_executable, '-jar', self.jar]
        else:
            return [self.command]
