__all__ = ["log_event"]

from . import threadedevents
from os import getenv


def log_event(
    reporting_component,
    reporting_instance,
    reporting_ns,
    event_message,
    event_reason="Unspecified",
    event_type="Normal",
    action="Unspecified",
    owner_name=None,
    owner_ns=None,
    owner_kind=None,
    event_lag=getenv("EVENT_LAG_SECONDS", "0"),
):
    """
    e.g. values
        reporting_component # "domsed",
        reporting_instance # getenv("POD_NAME")
        reporting_ns # Namespace of the reporting_instance
        event_message # "Some message truncated after 1024 chars"
        event_reason # "Started","Scheduled", "Pulled" etc.
        event_type # "Normal", "Urgent" etc.
        action # "Mutation", "Validation" etc.
        owner_name # e.g. the name of the Deployment or higher level object
                     that spawned this pod
        owner_ns # the corresponding namespace
                     (must match the reporting_ns above)
        owner_kind # Deployment etc.
        event_lag # Seconds to wait before creating event, default 0 
                     or the value of EVENT_LAG_SECONDS env variable
    """
    threadedevents.EventThread(
        reporting_component,
        reporting_instance,
        reporting_ns,
        event_message,
        event_reason,
        event_type,
        action,
        owner_name,
        owner_ns,
        owner_kind,
        event_lag,
    ).start()
