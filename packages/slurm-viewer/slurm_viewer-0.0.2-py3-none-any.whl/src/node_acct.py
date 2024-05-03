from __future__ import annotations

import datetime
import re
import subprocess
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, field_validator, ConfigDict

from src.common_types import MemoryUsed, CPU_TIME_RE, PostFixUnit
from src.config import Config

TRES_USAGE_IN_AVE_RE = (r'^cpu=(?P<cpu>(?:\d+-)?\d+:\d+:\d+),energy=(?P<energy>\d+),fs/disk=(?P<disk>\d+),'
                        r'gres/gpumem=(?P<gpu_mem>\w+),gres/gpuutil=(?P<gpu_util>\d+),mem=(?P<mem>\d+K),'
                        r'pages=(?P<pages>\d+),vmem=(?P<vmem>\d+K)$')

REQ_ALLOC_TRES_RE = (r'^(?:billing=(?P<billing>\d+),)?cpu=(?P<cpu>\d+)(?:,energy=(?P<energy>\d+))?,'
                     r'gres/gpu=(?P<gpu>\d+),mem=(?P<mem>\d+\w),node=(?P<node>\d+)$')


class ExitCodeSignal:  # pylint: disable=too-few-public-methods
    def __init__(self, value: str) -> None:
        self.code: int | None
        self.signal: int | None

        data = value.split(':')
        if len(data) == 2:
            self.code = int(data[0])
            self.signal = int(data[1])
            return

        if len(data) == 1:
            self.code = int(data[0])
            self.signal = None
            return

        self.code = None
        self.signal = None


# noinspection PyNestedDecorators
class TrackableResourceUsage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cpu: datetime.timedelta | None = None
    energy: int | None = None
    disk: MemoryUsed | None = None
    gpu_mem: MemoryUsed | None = None
    gpu_util: int | None = None
    mem: MemoryUsed | None = None
    pages: int | None = None
    vmem: MemoryUsed | None = None

    @field_validator('cpu', mode='before')
    @classmethod
    def timedelta_validator(cls, value: str) -> datetime.timedelta:
        m = re.search(CPU_TIME_RE, value)
        if not m:
            return datetime.timedelta(0)

        return datetime.timedelta(**{k: float(v) for k, v in m.groupdict().items() if v is not None})

    @field_validator('gpu_mem', 'mem', 'vmem', 'disk', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)


# noinspection PyNestedDecorators
class ReqAllocTrackableResources(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cpu: int | None = None
    mem: MemoryUsed | None = None
    billing: int | None = None
    gpu: int | None = None
    node: int | None = None
    energy: int | None = None

    @field_validator('mem', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)


class JobStateCodes(Enum):
    BOOT_FAIL = 'BOOT_FAIL'
    CANCELLED = 'CANCELLED'
    COMPLETED = 'COMPLETED'
    DEADLINE = 'DEADLINE'
    FAILED = 'FAILED'
    NODE_FAIL = 'NODE_FAIL'
    OUT_OF_MEMORY = 'OUT_OF_MEMORY'
    PENDING = 'PENDING'
    PREEMPTED = 'PREEMPTED'
    RUNNING = 'RUNNING'
    REQUEUED = 'REQUEUED'
    RESIZING = 'RESIZING'
    REVOKED = 'REVOKED'
    SUSPENDED = 'SUSPENDED'
    TIMEOUT = 'TIMEOUT'


# noinspection PyNestedDecorators
class NodeAcct(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    JobID: str
    JobIDRaw: str
    JobName: str
    Partition: str
    MaxVMSize: MemoryUsed
    MaxVMSizeNode: str
    MaxVMSizeTask: str
    AveVMSize: MemoryUsed
    MaxRSS: MemoryUsed
    MaxRSSNode: str
    MaxRSSTask: str
    AveRSS: MemoryUsed
    MaxPages: str
    MaxPagesNode: str
    MaxPagesTask: str
    AvePages: str
    MinCPU: datetime.timedelta
    MinCPUNode: str
    MinCPUTask: str
    AveCPU: datetime.timedelta
    NTasks: str
    AllocCPUS: int
    Elapsed: datetime.timedelta
    State: JobStateCodes
    ExitCode: ExitCodeSignal
    AveCPUFreq: PostFixUnit
    ReqCPUFreqMin: PostFixUnit
    ReqCPUFreqMax: PostFixUnit
    ReqCPUFreqGov: PostFixUnit
    ReqMem: MemoryUsed
    ConsumedEnergy: PostFixUnit
    MaxDiskRead: MemoryUsed
    MaxDiskReadNode: str
    MaxDiskReadTask: str
    AveDiskRead: MemoryUsed
    MaxDiskWrite: MemoryUsed
    MaxDiskWriteNode: str
    MaxDiskWriteTask: str
    AveDiskWrite: MemoryUsed
    ReqTRES: ReqAllocTrackableResources
    AllocTRES: ReqAllocTrackableResources
    TRESUsageInAve: TrackableResourceUsage
    TRESUsageInMax: TrackableResourceUsage
    TRESUsageInMaxNode: str
    TRESUsageInMaxTask: str
    TRESUsageInMin: TrackableResourceUsage
    TRESUsageInMinNode: str
    TRESUsageInMinTask: str
    TRESUsageInTot: TrackableResourceUsage
    TRESUsageOutMax: str
    TRESUsageOutMaxNode: str
    TRESUsageOutMaxTask: str
    TRESUsageOutAve: str
    TRESUsageOutTot: str

    @field_validator('TRESUsageInAve', 'TRESUsageInMax', 'TRESUsageInMin', 'TRESUsageInTot', mode='before')
    @classmethod
    def tres_usage_in_ave_validator(cls, value: str) -> TrackableResourceUsage:
        m = re.search(TRES_USAGE_IN_AVE_RE, value)
        if not m:
            return TrackableResourceUsage()

        return TrackableResourceUsage(**m.groupdict())

    @field_validator('ReqTRES', 'AllocTRES', mode='before')
    @classmethod
    def req_alloc_tres_validator(cls, value: str) -> ReqAllocTrackableResources:
        m = re.search(REQ_ALLOC_TRES_RE, value)
        if not m:
            return ReqAllocTrackableResources()

        return ReqAllocTrackableResources(**m.groupdict())

    @field_validator('State', mode='before')
    @classmethod
    def state_validator(cls, value: str) -> JobStateCodes:
        return JobStateCodes(value.split()[0])

    @field_validator('ExitCode', mode='before')
    @classmethod
    def exit_code_validator(cls, value: str) -> ExitCodeSignal:
        return ExitCodeSignal(value)

    @field_validator('ReqMem', 'AveDiskWrite', 'AveDiskRead', 'MaxDiskWrite', 'MaxDiskRead', 'MaxVMSize', 'AveVMSize',
                     'AveRSS', 'MaxRSS', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)

    @field_validator('AveCPUFreq', 'ReqCPUFreqMin', 'ReqCPUFreqMax', 'ReqCPUFreqGov', 'ConsumedEnergy', mode='before')
    @classmethod
    def post_fix_validator(cls, value: str) -> PostFixUnit:
        return PostFixUnit(value)

    @field_validator('Elapsed', 'MinCPU', 'AveCPU', mode='before')
    @classmethod
    def timedelta_validator(cls, value: str) -> datetime.timedelta:
        m = re.search(CPU_TIME_RE, value)
        if not m:
            return datetime.timedelta(0)

        return datetime.timedelta(**{k: float(v) for k, v in m.groupdict().items() if v is not None})


def create_node_acct(data: str, header: list[str]) -> NodeAcct:
    return NodeAcct(**dict(zip(header, data.rstrip().split('|'))))


def _get_lines(server: str | None, nodelist: list[str], num_weeks: int = 4, debug: bool = False) -> list[str]:
    if debug:
        with (Path(__file__).parent / '_data/sacct.csv').open('r', encoding='utf8') as log:
            return log.readlines()

    try:
        arguments = f'ssh -t {server} ' if server is not None else ''
        arguments += f'sacct --starttime now-{num_weeks}week --long --allusers --parsable2 --nodelist={",".join(nodelist)}'

        with subprocess.Popen(arguments, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as process:
            stdout, _ = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        print('TimeoutExpired')
        return []
    except subprocess.CalledProcessError:
        print('CalledProcessError')
        return []
    return stdout.splitlines()


def account_info(config: Config, num_weeks: int) -> list[NodeAcct]:
    lines = _get_lines(config.server, config.node_list, num_weeks=num_weeks, debug=config.debug)
    header = lines[0].rstrip().split('|')
    return [create_node_acct(x, header) for x in lines[1:]]
