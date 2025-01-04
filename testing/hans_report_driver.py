import pathlib
import pytest

from pytest_html.util import _read_template
from pytest_html.report_data import ReportData
from _pytest.reports import TestReport, CollectReport

import pytest_html
from pytest_html.selfcontained_report import SelfContainedReport
from pytest_html.basereport import _fix_py
from _pytest.config import _prepareconfig
from pytest_html.util import _process_css
import os
from pytest_metadata.plugin import metadata_key


def main() -> None:
    config = _prepareconfig()

    resources_path = pathlib.Path(pytest_html.__file__).parent.joinpath("resources")
    assert resources_path.is_dir()
    default_css = pathlib.Path(resources_path, "style.css")
    template = _read_template([resources_path])
    extra_css = [
        pathlib.Path(os.path.expandvars(css)).expanduser()
        for css in config.getoption("css")
    ]
    assert default_css.is_file()
    processed_css = _process_css(default_css, extra_css)

    report_path = pathlib.Path(__file__).with_suffix(".html")
    template = _read_template([resources_path])

    report_data = ReportData(config=config)
    report_data.set_data("a", "b")
    test_report = TestReport(
        nodeid="bliblablo",
        location=("file42", 42),
        keywords={},
        outcome="passed",
        longrepr=None,
        when="setup",
    )
    if False:
        outcome = "Passed"
        logs = ["No log output captured."]
        test_data = {
            "extras": [],
            "result": "Passed",
            "testId": "testing/test_hans.py::test_fail::setup",
            "duration": "1 ms",
            "resultsTableRow": [
                '<td class="col-result">Passed</td>',
                '<td class="col-testId">testing/test_hans.py::test_fail::setup</td>',
                '<td class="col-duration">1 ms</td>',
                '<td class="col-links"></td>',
            ],
        }
        report_data.add_test(test_data, test_report, outcome, logs)

    report = SelfContainedReport(
        report_path,
        config,
        report_data,
        template,
        processed_css,
    )

    # @pytest.hookimpl(trylast=True)
    # def pytest_sessionstart
    report._config.stash[metadata_key] = {
        "A": "aaa",
        "B": "bbb",
    }
    report_data.set_data("environment", report._generate_environment())

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
        outcome="passed",
        longrepr=None,
        when="setup",
    )
    nodeid = test_report1.nodeid
    report._reports[nodeid][key_when_outcome] = [test_report1]

    report._generate_report()
    print(f"{report._report_path=}")


if __name__ == "__main__":
    main()
