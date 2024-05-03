import datetime
import re
import subprocess
from pathlib import Path

import dateutil.parser
from pydantic import BaseModel, field_validator, ConfigDict

from src.common_types import CPU_TIME_RE, MemoryUsed
from src.config import Config

QUEUE_RE = (r'^(?P<account>[\w\d-]+)[|](?P<tres_per_node>[\w\:]+)[|](?P<min_cpu>\d+)[|](?P<min_tmp_disk>\d+)[|]'
            r'(?P<end_time>[\w\d:-]+)[|](?P<features>[^|]+)[|](?P<group>[^|]+)[|](?P<over_subscribe>[^|]+)[|]'
            r'(?P<job_id>\d+)[|](?P<name>[^|]+)[|](?P<comment>[^|]+)[|](?P<time_limit>[^|]+)[|]'
            r'(?P<min_memory>[^|]+)[|](?P<req_nodes>[^|]*)[|](?P<command>[^|]+)[|](?P<priority>[^|]+)[|]'
            r'(?P<qos>[^|]+)[|](?P<reason>[^|]+)[|](?P<st>[^|]+)[|](?P<user>[^|]+)[|](?P<reservation>[^|]+)[|]'
            r'(?P<wc_key>[^|]+)[|](?P<excluded_nodes>[^|]*)[|](?P<nice>[^|]+)[|](?P<s_c_t>[^|]+)[|]'
            r'(?P<job_id_2>[^|]+)[|](?P<exec_host>[^|]+)[|](?P<cpus>[^|]+)[|](?P<nodes>[^|]+)[|]'
            r'(?P<dependency>[^|]+)[|](?P<array_job_id>[^|]+)[|](?P<group_2>[^|]+)[|](?P<sockets_per_node>[^|]+)[|]'
            r'(?P<cores_per_socket>[^|]+)[|](?P<threads_per_core>[^|]+)[|](?P<array_task_id>[^|]+)[|]'
            r'(?P<time_left>[^|]+)[|](?P<time>[^|]+)[|](?P<nodelist>[^|]+)[|](?P<contiguous>[^|]+)[|]'
            r'(?P<partition>[^|]+)[|](?P<priority_2>[^|]+)[|](?P<nodelist_reason>[^|]+)[|](?P<start_time>[^|]+)[|]'
            r'(?P<state>[^|]+)[|](?P<uid>[^|]+)[|](?P<submit_time>[^|]+)[|](?P<licenses>[^|]+)[|](?P<core_spec>[^|]+)[|]'
            r'(?P<scheduled_nodes>[^|]+)[|](?P<work_dir>[^|]+)$')


# noinspection PyNestedDecorators
class NodeQueue(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    account: str
    tres_per_node: str
    min_cpu: int
    min_tmp_disk: int
    end_time: datetime.datetime
    features: str
    group: str
    over_subscribe: str
    job_id: int
    name: str
    comment: str
    time_limit: datetime.timedelta
    min_memory: MemoryUsed
    req_nodes: str
    command: str
    priority: float
    qos: str
    reason: str
    st: str
    user: str
    reservation: str
    wc_key: str
    excluded_nodes: str
    nice: int
    s_c_t: str
    exec_host: str
    cpus: int
    nodes: int
    dependency: str
    array_job_id: int
    sockets_per_node: str
    cores_per_socket: str
    threads_per_core: str
    array_task_id: str
    time_left: datetime.timedelta
    time: datetime.datetime
    nodelist: str
    contiguous: int
    partition: str
    nodelist_reason: str
    start_time: datetime.datetime
    state: str
    uid: int
    submit_time: datetime.datetime
    licenses: str
    core_spec: str
    scheduled_nodes: str
    work_dir: str

    @property
    def start_delay(self) -> datetime.timedelta:
        return self.start_time - self.submit_time

    @field_validator('time_limit', 'time_left', mode='before')
    @classmethod
    def timedelta_validator(cls, value: str) -> datetime.timedelta:
        m = re.search(CPU_TIME_RE, value)
        if not m:
            return datetime.timedelta(0)

        return datetime.timedelta(**{k: float(v) for k, v in m.groupdict().items() if v is not None})

    @field_validator('time', 'start_time', 'end_time', mode='before')
    @classmethod
    def datetime_validator(cls, value: str) -> datetime.datetime:
        try:
            return dateutil.parser.parse(value)
        except ValueError:
            return datetime.datetime(year=1970, month=1, day=1)

    @field_validator('min_memory', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)


def create_output(lines: list[str]) -> list[NodeQueue]:
    def _create_node_queue(data: str) -> NodeQueue | None:
        m = re.search(QUEUE_RE, data)
        if not m:
            return None

        return NodeQueue(**m.groupdict())

    result = []
    for x in lines[1:]:
        val = _create_node_queue(x.rstrip())
        if val is None:
            continue

        result.append(val)

    return result


def queue_info(config: Config) -> list[NodeQueue]:
    if config.debug:
        with (Path(__file__).parent / '_data/squeue.csv').open('r', encoding='utf8') as log:
            lines = log.readlines()

        return create_output(lines)

    try:
        arguments = f'ssh -t {config.server} ' if config.server is not None else ''
        arguments += f'squeue -w {",".join(config.node_list)} --format=%all'

        with subprocess.Popen(arguments, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as process:
            stdout, _ = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        print('TimeoutExpired')
        return []
    except subprocess.CalledProcessError:
        print('CalledProcessError')
        return []

    return create_output(stdout.splitlines())
