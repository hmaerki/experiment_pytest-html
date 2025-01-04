import pathlib
import pytest

from pytest_html.util import _read_template
from pytest_html.report_data import ReportData
from _pytest.reports import TestReport

import pytest_html
from pytest_html.selfcontained_report import SelfContainedReport
from _pytest.config import _prepareconfig


def main() -> None:
    config = _prepareconfig()

    report_path = pathlib.Path(__file__).with_suffix(".html")
    resources_path = pathlib.Path(pytest_html.__file__).parent.joinpath("resources")
    assert resources_path.is_dir()
    css = resources_path / "style.css"
    assert css.is_file()
    template = _read_template([resources_path])

    report_data_dict = {
        "tests": [
            {
                "id": "passed_1",
                "result": "passed",
            },
            {
                "id": "failed_2",
                "result": "failed",
            },
            {
                "id": "passed_3",
                "result": "passed",
            },
            {
                "id": "passed_4",
                "result": "passed",
            },
            {
                "id": "passed_5",
                "result": "passed",
            },
            {
                "id": "passed_6",
                "result": "passed",
            },
        ],
    }
    report_data = ReportData(config=config)
    report_data.set_data("a", "b")
    report = TestReport(
        nodeid="bliblablo",
        location=("file42", 42),
        keywords={},
        outcome="passed",
        longrepr=None,
        when="setup",
    )
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
    report_data.add_test(test_data, report, outcome, logs)
    # report_data.add_test( test_data, report, outcome, logs)

    report = SelfContainedReport(report_path, config, report_data, template, css)
    report._generate_report()
    print(f"{report._report_path=}")


def main_bak() -> None:
    pluginmanager = pytest.PytestPluginManager()
    config = pytest.Config(pluginmanager=pluginmanager)
    # config.addinivalue_line("max_asset_filename_length", "max_asset_filename_length=42")
    # config.getini("max_asset_filename_length")
    # config.option.max_asset_filename_length = 12
    # config._parser.addini(
    #     "max_asset_filename_length",
    #     default=255,
    #     help="set the maximum filename length for assets "
    #     "attached to the html report.",
    # )
    # config.option.max_asset_filename_length = 42
    # config.option["inifilename"] = "Hallo inifilename"
    config.option.rootdir = pathlib.Path(__file__).parent
    config.option.inifilename = "Hallo inifilename"
    config.option.override_ini = False
    # config.option.max_asset_filename_length = "Hallo max_asset_filename_length"
    config.option.confcutdir = False
    config.option.pyargs = False
    # description, type, default
    config._parser._inidict["testpaths"] = ("Testpath", "str", [])
    config._parser._inidict["consider_namespace_packages"] = (
        "Description consider_namespace_packages",
        "str",
        [],
    )
    config.option.noconftest = False
    config.option.importmode = "importlib"
    c = config.pytest_cmdline_parse(
        pluginmanager=pluginmanager, args=["max_asset_filename_length=42"]
    )
    config._parser.addini(
        "max_asset_filename_length",
        default=255,
        help="set the maximum filename length for assets "
        "attached to the html report.",
    )
    config.getini("max_asset_filename_length")

    report_path = pathlib.Path(__file__).with_suffix(".html")
    resources_path = pathlib.Path(pytest_html.__file__).parent.joinpath("resources")
    assert resources_path.is_dir()
    css = resources_path / "style.css"
    assert css.is_file()
    template = _read_template([resources_path])

    report_data = {
        "tests": [
            {
                "id": "passed_1",
                "result": "passed",
            },
            {
                "id": "failed_2",
                "result": "failed",
            },
            {
                "id": "passed_3",
                "result": "passed",
            },
            {
                "id": "passed_4",
                "result": "passed",
            },
            {
                "id": "passed_5",
                "result": "passed",
            },
            {
                "id": "passed_6",
                "result": "passed",
            },
        ],
    }
    report = SelfContainedReport(report_path, config, report_data, template, css)
    report.xy()


if __name__ == "__main__":
    main()
