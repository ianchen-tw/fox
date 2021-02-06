from typing import Any, Iterable, Optional, Sequence, Union

from rich.console import Console as Console
from rich.progress import GetTimeCallable as GetTimeCallable
from rich.progress import Progress
from rich.progress import ProgressColumn as ProgressColumn
from rich.progress import ProgressType as ProgressType
from rich.progress import TaskID as TaskID

class MyProgress(Progress):
    def __init__(
        self,
        *columns: Union[str, ProgressColumn],
        console: Console = ...,
        auto_refresh: bool = ...,
        refresh_per_second: float = ...,
        speed_estimate_period: float = ...,
        transient: bool = ...,
        redirect_stdout: bool = ...,
        redirect_stderr: bool = ...,
        get_time: GetTimeCallable = ...,
        disable: bool = ...
    ) -> None: ...
    def track(
        self,
        sequence: Union[Iterable[ProgressType], Sequence[ProgressType]],
        total: int = ...,
        task_id: Optional[TaskID] = ...,
        description: Any = ...,
        update_period: float = ...,
        remove_finish: bool = ...,
    ) -> Iterable[ProgressType]: ...
