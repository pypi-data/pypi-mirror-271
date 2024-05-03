##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.11                                                            #
# Generated on 2024-05-02T22:04:13.836701                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import abc

class SecretsProvider(abc.ABC, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None) -> typing.Dict[str, str]:
        """
        Retrieve the secret from secrets backend, and return a dictionary of
        environment variables.
        """
        ...
    ...

