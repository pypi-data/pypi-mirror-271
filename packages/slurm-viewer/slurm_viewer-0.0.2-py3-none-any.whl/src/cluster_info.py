import datetime
import re
import subprocess
from enum import Enum

import dateutil.parser
from pydantic import BaseModel, field_validator

from src.config import Config

NODE_RE = (r'^NodeName=(?P<node_name>.+?)\s+Arch=(?P<arch>.+?)\s+CoresPerSocket=(?P<cores_per_socket>\d+)\s+'
           r'CPUAlloc=(?P<cpu_alloc>\d+)\s+CPUEfctv=(?P<cpu_efctv>\d+)\s+CPUTot=(?P<cpu_tot>\d+)\s+'
           r'CPULoad=(?P<cpuload>\d+\.\d+)\s+AvailableFeatures=(?P<available_features>.+?)\s+'
           r'ActiveFeatures=(?P<active_features>.+?)\s+Gres=(?P<gres>.+?)\s+NodeAddr=(?P<node_addr>.+?)\s+'
           r'NodeHostName=(?P<node_hostname>.+?)\s+Version=(?P<version>.+?)\s+OS=(?P<os>.+?)\s+'
           r'RealMemory=(?P<real_memory>\d+)\s+AllocMem=(?P<alloc_mem>\d+)\s+FreeMem=(?P<freemem>\d+)\s+'
           r'Sockets=(?P<sockets>\d+)\s+Boards=(?P<boards>\d+)\s+State=(?P<state>.+?)\s+'
           r'ThreadsPerCore=(?P<threads_per_core>\d+)\s+TmpDisk=(?P<tmp_disk>\d+)\s+Weight=(?P<weight>.+?)\s+'
           r'Owner=(?P<owner>.+?)\s+MCS_label=(?P<mcs_label>.+?)\s+Partitions=(?P<partitions>.+?)\s+'
           r'BootTime=(?P<boot_time>.+?)\s+SlurmdStartTime=(?P<slurmd_start_time>.+?)\s+'
           r'LastBusyTime=(?P<last_busy_time>.+?)\s+ResumeAfterTime=(?P<resume_after_time>.+?)\s+'
           r'CfgTRES=(?P<cfgtres>.+?)\s+AllocTRES=(?P<alloc_tres>.+?)\s+')

CFGTRESS_RE = r'^cpu=(?P<cpu>\d+),mem=(?P<mem>\d+\w),billing=(?P<billing>\d+),gres/gpu=(?P<gpu>\d+)$'
ALLOCTRESS_RE = (r'^cpu=(?P<cpu>\d+),mem=(?P<mem>\d+\w)(?:,gres/gpu=(?P<gpu_alloc>\d+))'
                 r'(?:,gres/gpu:(?P<gpu_type>\S+)=(?P<gpu_total>\d+))?$')


class State(Enum):
    IDLE = 'IDLE'
    MIXED = 'MIXED'
    ALLOCATED = 'ALLOCATED'
    DRAIN = 'DRAIN'
    MIXED_DRAIN = 'MIXED+DRAIN'
    MIXED_COMPLETING = 'MIXED+COMPLETING'
    IDLE_DRAIN = 'IDLE+DRAIN'


class CfgTRES(BaseModel):
    cpu: int = -1
    mem: str = 'NA'
    billing: int = -1
    gpu: int = -1


class AllocTRES(BaseModel):
    cpu: int = -1
    mem: str = 'NA'
    gpu_alloc: int | None = None
    gpu_type: str | None = None
    gpu_total: int | None = None


class GPU(BaseModel):
    name: str
    amount: int


# noinspection PyNestedDecorators
class ClusterNode(BaseModel):
    node_name: str
    arch: str
    cores_per_socket: int
    cpu_alloc: int
    cpu_efctv: int
    cpu_tot: int
    cpuload: float
    available_features: list[str]
    active_features: list[str]
    gres: GPU | None
    node_addr: str
    node_hostname: str
    version: str
    os: str
    real_memory: int
    alloc_mem: int
    freemem: int
    sockets: int
    boards: int
    state: State
    threads_per_core: int
    tmp_disk: int
    weight: int
    owner: str
    mcs_label: str
    partitions: list[str]
    boot_time: datetime.datetime
    slurmd_start_time: datetime.datetime
    last_busy_time: datetime.datetime
    resume_after_time: datetime.datetime | None
    cfgtres: CfgTRES
    alloc_tres: AllocTRES

    @property
    def cpu_avail(self) -> int:
        return self.cpu_tot - self.cpu_alloc

    @property
    def gpu_tot(self) -> int:
        if self.gres:
            return self.gres.amount
        return 0

    @property
    def gpu_alloc(self) -> int:
        if self.alloc_tres.gpu_alloc:
            return self.alloc_tres.gpu_alloc
        return 0

    @property
    def gpu_avail(self) -> int:
        if self.gres:
            return self.gpu_tot - self.gpu_alloc
        return 0

    @property
    def gpu_type(self) -> str:
        if self.gres:
            return self.gres.name
        return ''

    @property
    def mem_tot(self) -> int:
        return self.real_memory // 1024

    @property
    def mem_alloc(self) -> int:
        return self.alloc_mem // 1024

    @property
    def mem_avail(self) -> int:
        return self.mem_tot - self.mem_alloc

    @property
    def gpu_mem(self) -> str:
        for feature in self.available_features:
            if feature.startswith('gpu-'):
                return feature.lstrip('gpu-')
        return ''

    @property
    def short_name(self) -> str:
        return self.node_name[8:]

    @property
    def cpu_gpu(self) -> float | None:
        if self.gpu_avail == 0:
            return None
        return self.cpu_avail / self.gpu_avail

    @property
    def mem_gpu(self) -> float | None:
        if self.gpu_avail == 0:
            return None
        return self.mem_avail / self.gpu_avail

    @field_validator('resume_after_time', mode='before')
    @classmethod
    def date_validator(cls, value: str) -> datetime.datetime | None:
        if not isinstance(value, datetime.datetime) and len(value) > 0:
            return None
        return dateutil.parser.parse(value)

    @field_validator('available_features', 'active_features', 'partitions', mode='before')
    @classmethod
    def list_validator(cls, value: str) -> list[str]:
        return value.split(',')

    @field_validator('gres', mode='before')
    @classmethod
    def split_validator(cls, value: str) -> GPU | None:
        data = value.split(':')
        if len(data) != 3:
            return None
        return GPU(name=data[1], amount=int(data[2]))

    @field_validator('cfgtres', mode='before')
    @classmethod
    def cfgtres_validator(cls, value: str) -> CfgTRES:
        m = re.search(CFGTRESS_RE, value)
        if not m:
            return CfgTRES()

        return CfgTRES(**m.groupdict())

    @field_validator('alloc_tres', mode='before')
    @classmethod
    def alloctres_validator(cls, value: str) -> AllocTRES:
        m = re.search(ALLOCTRESS_RE, value)
        if not m:
            return AllocTRES()

        return AllocTRES(**m.groupdict())


def create_node_info(node_str: str) -> ClusterNode | None:
    m = re.search(NODE_RE, node_str)
    if not m:
        return None

    return ClusterNode(**m.groupdict())


def cluster_info(config: Config) -> list[ClusterNode]:
    try:
        arguments = f'ssh -t {config.server} ' if config.server is not None else ''
        arguments += 'scontrol -o show nodes'

        with subprocess.Popen(arguments, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as process:
            stdout, _ = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        print('TimeoutExpired')
        return []
    except subprocess.CalledProcessError:
        print('CalledProcessError')
        return []

    nodes = []
    for node_str in stdout.splitlines():
        node_info = create_node_info(node_str)
        if node_info is None:
            continue

        nodes.append(node_info)

    return nodes
