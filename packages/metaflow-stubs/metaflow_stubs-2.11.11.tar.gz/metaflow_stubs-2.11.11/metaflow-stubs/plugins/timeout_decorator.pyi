##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.11                                                            #
# Generated on 2024-05-02T22:04:13.833225                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators
    import metaflow.exception

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

UBF_CONTROL: str

class TimeoutException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class TimeoutDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    def __init__(self, *args, **kwargs):
        ...
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        ...
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    def task_post_step(self, step_name, flow, graph, retry_count, max_user_code_retries):
        ...
    ...

def get_run_time_limit_for_task(step_decos):
    ...

