import datetime
import subprocess
from dataclasses import dataclass
from typing import Set, Any, Callable, Generator

import textual.widget
from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Grid, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Footer, Header, TabbedContent, TabPane, Checkbox, Button, Label, SelectionList, Collapsible, \
    RadioSet, RadioButton
from textual.widgets.selection_list import Selection
from textual_plotext import PlotextPlot

from src.cluster_info import cluster_info, ClusterNode
from src.config import Config
from src.node_acct import account_info
from src.queue_info import queue_info
from src.sortable_data_table import SortableDataTable


def partitions(data: list[ClusterNode]) -> list[str]:
    result: Set[str] = {ALL_PARTITIONS}
    for value in data:
        result.update(value.partitions)

    return sorted(result)


def group_users(config: Config, group: str) -> list[str]:
    try:
        arguments = f'ssh -t {config.server} ' if config.server is not None else ''
        arguments += f'getent group {group}'

        with subprocess.Popen(arguments, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as process:
            stdout, _ = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        print('TimeoutExpired')
        return []
    except subprocess.CalledProcessError:
        print('CalledProcessError')
        return []

    return sorted(stdout.rsplit(':', maxsplit=1)[-1].split(','))


@dataclass
class FilterOptions:
    gpu: bool
    gpu_available: bool
    partition: str | None


ALL_PARTITIONS = 'ALL'


def filter_nodes(nodes: list[ClusterNode], node_filter: FilterOptions) -> list[ClusterNode]:
    result = []
    for node in nodes:
        if node.gpu_tot == 0 and node_filter.gpu:
            continue

        if node.gpu_avail == 0 and node_filter.gpu_available:
            continue

        if node_filter.partition != ALL_PARTITIONS and node_filter.partition not in node.partitions:
            continue

        result.append(node)
    return result


class Loading:
    def __init__(self, widget: textual.widget.Widget) -> None:
        self.widget = widget

    def __enter__(self) -> None:
        self.widget.loading = True

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.widget.loading = False


class ColumnSelectionScreen(Screen):
    CSS = """
    ColumnSelectionScreen {
        align: center middle;
    }
    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        border: thick $background 80%;
        background: $surface;
    }
    #selection {
        column-span: 2;
        height: 100%;
        width: 100%;
    }
    """

    def __init__(self, selection: list[Selection]) -> None:
        super().__init__()
        self.selection = selection

    def compose(self) -> ComposeResult:
        yield Grid(
            SelectionList(*self.selection, id='selection'),
            Button('OK', variant='success', id='ok'),
            Button('Cancel', variant='primary', id='cancel'),
            id='dialog',
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'ok':
            self.dismiss(self.query_one(SelectionList).selected)
        else:
            self.dismiss(None)


def sort_column(value: Any) -> Any:
    if value is None:
        return ''

    if isinstance(value, Text):
        return value.plain

    return value


class SlurmViewer(App):
    CSS = """
    #cluster_horizontal {
        height: auto;
    }
    
    #cluster_label {
        width: 1fr;
        padding: 1 1;
        text-align: right;
    }
    
    #cluster_data_table {
        height: 100%;
    }
    
    #queue_horizontal {
        height: auto;
    }
    
    #queue_label {
        width: 1fr;
        padding: 1 1;
        text-align: right;
    }
    
    #queue_data_table {
        height: 100%;
    }    
    """

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.title = f'{self.__class__.__name__} ({config.server})'
        self.config = config
        self.cluster_info = cluster_info(self.config)
        self.queue_info = queue_info(self.config)
        self.gpu_history = 4  # weeks
        self.gpu_usage = account_info(self.config, self.gpu_history)
        self.partitions = partitions(self.cluster_info)
        # self.users = group_users(self.config, 'lkeb-hpc')
        self.sort_function: Callable[[Any], Any] | None = sort_column

    def compose(self) -> ComposeResult:
        yield Header(name=self.config.server, show_clock=False)
        with TabbedContent():
            with TabPane('Cluster', id='tab_cluster'):
                yield from self._setup_cluster_tab()
            with TabPane('Queue', id='tab_queue'):
                yield from self._setup_queue_tab()
            with TabPane('GPU usage', id='tab_gpu_usage'):
                yield PlotextPlot(id='plot')
        yield Footer()

    @staticmethod
    def _setup_queue_tab() -> Generator:
        with Vertical():
            with Horizontal(id='queue_horizontal'):
                yield Label(f'Last update: {datetime.datetime.now().strftime("%H:%M:%S")}', id='queue_label')
                yield Button(label='Refresh', id='queue_refresh')
            yield SortableDataTable(id='job_queue_table')

    def _setup_cluster_tab(self) -> Generator:
        with Vertical():
            with Horizontal(id='cluster_horizontal'):
                yield Checkbox(label='GPU only', id='cluster_show_gpu')
                yield Checkbox(label='GPU available', id='cluster_show_gpu_available')
                with Collapsible(title='Partitions', id='cluster_collapsible'):
                    with RadioSet(id='cluster_partitions'):
                        for label in self.partitions:
                            yield RadioButton(label, value=label == ALL_PARTITIONS)
                yield Label(f'Last update: {datetime.datetime.now().strftime("%H:%M:%S")}', id='cluster_label')
                yield Button(label='Refresh', id='cluster_refresh')
                yield Button(label='Select columns', id='cluster_show_columns')
            with ScrollableContainer():
                table = SortableDataTable(id='cluster_data_table')
                table.sort_function = self.sort_function
                yield table

    async def on_mount(self) -> None:
        await self._cluster_data_table()
        await self._queue_data_table()
        await self._gpu_usage_plot()

    @on(Checkbox.Changed, '#cluster_show_gpu')
    @on(Checkbox.Changed, '#cluster_show_gpu_available')
    def show_gpu(self, _: Checkbox.Changed) -> None:
        self.update_cluster_info()

    @on(Button.Pressed, '#cluster_show_columns')
    def select_columns(self, _: Checkbox.Changed) -> None:
        def check_result(result: list[str] | None) -> None:
            if result is None:
                return
            self.config.node_columns = result

            data_table = self.query_one('#cluster_data_table', SortableDataTable)
            data_table.clear(columns=True)
            data_table.add_columns(*self.config.node_columns)

            self.update_cluster_info()

        current_columns = [x.label.plain for x in self.query_one('#cluster_data_table', SortableDataTable).columns.values()]
        all_columns = sorted(ClusterNode.model_fields.keys())
        all_columns.extend([name for name, value in vars(ClusterNode).items() if isinstance(value, property)])

        columns = [Selection(prompt=x, value=x, initial_state=x in current_columns) for x in all_columns]

        screen = ColumnSelectionScreen(columns)
        self.push_screen(screen, check_result)

    @work(thread=True)
    @on(Button.Pressed, '#cluster_refresh')
    def refresh_info(self, _: Checkbox.Changed) -> None:
        data_table = self.query_one('#cluster_data_table', SortableDataTable)

        with Loading(data_table):
            self.cluster_info = cluster_info(self.config)

        self.update_cluster_info()
        self.query_one('#cluster_label', Label).update(f'Last update: {datetime.datetime.now().strftime("%H:%M:%S")}')

    @on(RadioSet.Changed, '#cluster_partitions')
    def partitions_changed(self, value: RadioSet.Changed) -> None:
        data_table = self.query_one('#cluster_data_table', SortableDataTable)
        data_table.clear()
        checkboxes = self._checkbox_values()
        options = FilterOptions(gpu=checkboxes['GPU only'], gpu_available=checkboxes['GPU available'],
                                partition=value.pressed.label.plain)
        self._update_data_table(filter_nodes(self.cluster_info, options), data_table)

    def _checkbox_values(self) -> dict[str, bool]:
        return {x.label.plain: x.value for x in self.query(Checkbox).nodes}

    def update_cluster_info(self) -> None:
        data_table = self.query_one('#cluster_data_table', SortableDataTable)
        data_table.clear()
        checkboxes = self._checkbox_values()
        button = self.query_one('#cluster_partitions', RadioSet).pressed_button
        partition = button.label.plain if button is not None else None
        options = FilterOptions(gpu=checkboxes['GPU only'], gpu_available=checkboxes['GPU available'], partition=partition)
        self._update_data_table(filter_nodes(self.cluster_info, options), data_table)

    def _update_data_table(self, nodes: list[ClusterNode], table: SortableDataTable) -> None:
        for index, row in enumerate(nodes, 1):
            label = Text(str(index), style='#B0FC38 italic')
            data = []
            for key in self.config.node_columns:
                value = getattr(row, key)
                data.append(value if value is not None else '')
            table.add_row(*data, label=label)

    async def _queue_data_table(self) -> None:
        data_table = self.query_one('#job_queue_table', SortableDataTable)
        data_table.cursor_type = 'row'
        data_table.clear(columns=True)
        data_table.zebra_stripes = True
        data_table.add_columns(*self.config.queue_columns)
        data_table.border_title = f'{len(self.queue_info)} nodes'

        for index, row in enumerate(self.queue_info, 1):
            label = Text(str(index), style='#B0FC38 italic')
            data = [getattr(row, key) for key in self.config.queue_columns]
            data_table.add_row(*data, label=label)

    async def _cluster_data_table(self) -> None:
        data_table = self.query_one('#cluster_data_table', SortableDataTable)
        data_table.cursor_type = 'row'
        data_table.clear(columns=True)
        data_table.zebra_stripes = True
        data_table.add_columns(*self.config.node_columns)
        data_table.border_title = f'{len(self.cluster_info)} nodes'

        self._update_data_table(self.cluster_info, data_table)

    async def _gpu_usage_plot(self) -> None:
        data = []
        for value in self.gpu_usage:
            if not value.TRESUsageInAve.gpu_mem or not value.TRESUsageInAve.gpu_mem.value:
                continue
            data.append(value.TRESUsageInAve.gpu_mem.GB)

        plotextplot = self.query_one('#plot', PlotextPlot)
        plt = plotextplot.plt
        plt.clear_figure()
        bins = 48
        plt.hist(data, bins)
        plt.title(f'Job GPU size last {self.gpu_history} weeks ({len(data)} jobs)')
        plt.xlabel('GPU Mem (GB)')
        plt.ylabel('# jobs')
        plotextplot.refresh()


if __name__ == "__main__":
    app = SlurmViewer(Config.init())
    app.run()
