import enum


class TaskState(enum.Enum):
    PENDING = 'Pending'
    RUNNING = 'Running'
    STOPPING = 'Stopping'
    STOPPED = 'Stopped'
    COMPLETED = 'Completed'
    ERROR = 'Error'
