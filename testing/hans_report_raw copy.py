import pathlib
import pytest
import time

from pytest_html.util import _read_template
from pytest_html.report_data import ReportData
# from _pytest.reports import TestReport, CollectReport

import pytest_html
from pytest_html.selfcontained_report import SelfContainedReport
from pytest_html.basereport import _fix_py
from _pytest.config import _prepareconfig
from pytest_html.util import _process_css
import os
from pytest_metadata.plugin import metadata_key
import typing
import dataclasses


@dataclasses.dataclass(repr=True)
class CollectReport:
    nodeid: str
    outcome: typing.Literal["failed"]
    # "failed", "rerun"
    #             "failed": {"label": "Failed", "value": 0},
    # "passed": {"label": "Passed", "value": 0},
    # "skipped": {"label": "Skipped", "value": 0},
    # "xfailed": {"label": "Expected failures", "value": 0},
    # "xpassed": {"label": "Unexpected passes", "value": 0},
    # "error": {"label": "Errors", "value": 0},
    # "rerun": {"label": "Reruns", "value": 0},

    longrepr: None
    result: list[str]
    # TODO: List of modules?
    # ["Module test_hans_a.py", "Module test_hans_b.py"],
    when: typing.Literal["str"]
    # "setup"| "teardown"| "collect"]
    longreprtext: str | None = None
    sections: list = dataclasses.field(default_factory=list)


@dataclasses.dataclass(repr=True)
class TestReport(CollectReport):
    location: tuple[str, int] = ("file42", 42)
    # ("file42", 42)
    keywords: dict = dataclasses.field(default_factory=dict)
    # {


class Hook:
    def pytest_html_duration_format(self, duration: int) -> tuple[int]:
        # TODO...
        duration = 42
        return [duration]

    def pytest_html_results_table_row(
        self, report: CollectReport, cells: list[str]
    ) -> None:
        pass

    def pytest_html_results_table_html(self, report: CollectReport, data: int) -> None:
        pass

    def pytest_html_results_summary(
        self,
        prefix,
        summary,
        postfix,
        session=None,
    ) -> None:
        pass


class Config:
    def __init__(self) -> None:
        self.hook = Hook()
        self._config = {
            "render_collapsed": "passed", # "all",
            "initial_sort": "result",
            "max_asset_filename_length": 1024,
        }

    def getini(self, key: str) -> typing.Any:
        return self._config[key]


def main() -> None:
    config = _prepareconfig()

    resources_path = pathlib.Path(pytest_html.__file__).parent.joinpath("resources")
    assert resources_path.is_dir()
    default_css = pathlib.Path(resources_path, "style.css")
    extra_css = [
        pathlib.Path(os.path.expandvars(css)).expanduser()
        for css in config.getoption("css")
    ]
    assert default_css.is_file()
    processed_css = _process_css(default_css, extra_css)

    report_path = pathlib.Path(__file__).with_suffix(".html")
    template = _read_template([resources_path])

    config = Config()

    report_data = ReportData(config=config)

    report = SelfContainedReport(
        report_path,
        config,
        report_data,
        template,
        processed_css,
    )

    environment = {
        "A": "aaa",
        "B": "bbb",
        "Packages": {"pytest": "8.3.4", "pluggy": "1.5.0"},
        "Plugins": {
            "anyio": "4.7.0",
            "html": "0.1.dev534+geb7de8a.d20250104",
            "metadata": "3.1.1",
        },
    }
    report_data.set_data("environment", environment)

    if True:

        def pytest_html_results_table_header(cells):
            cells.insert(2, "<th>Description</th>")
            cells.insert(
                1, '<th class="sortable time" data-column-type="time">Time</th>'
            )

        headers = report_data.table_header
        pytest_html_results_table_header(headers)
        report_data.table_header = _fix_py(headers)

    report.running_state = "started"

    # @pytest.hookimpl(trylast=True)
    # def pytest_collectreport(self, report):
    collect_report = CollectReport(
        nodeid="nodeid-collectreport",
        outcome="failed",
        when="setup",
        longrepr=None,
        result=["Module test_hans_a.py", "Module test_hans_b.py"],
    )
    report._process_report(collect_report, 0, [])

    # @pytest.hookimpl(trylast=True)
    # def pytest_collection_finish(self, session):
    report._report.collected_items = 42

    # @pytest.hookimpl(trylast=True)
    # def pytest_runtest_logreport(self, report):
    # key_when_outcome = ("setup", "passed")
    key_when_outcome = ("teardown", "passed")
    test_report1 = TestReport(
        nodeid="bliblablo",
        location=("file42", 42),
        keywords={},
        result=[],
        outcome="passed",
        longrepr=None,
        when="setup",
    )
    nodeid = test_report1.nodeid
    report._reports[nodeid][key_when_outcome] = [test_report1]

    # @pytest.hookimpl(trylast=True)
    # def pytest_sessionfinish(self, session):

    config.hook.pytest_html_results_summary(
        prefix=report._report.additional_summary["prefix"],
        summary=report._report.additional_summary["summary"],
        postfix=report._report.additional_summary["postfix"],
        session=None,
    )
    report._report.running_state = "finished"
    report._report.total_duration = 4242
    report._generate_report()
    print(f"{report._report_path=}")


if __name__ == "__main__":
    main()
