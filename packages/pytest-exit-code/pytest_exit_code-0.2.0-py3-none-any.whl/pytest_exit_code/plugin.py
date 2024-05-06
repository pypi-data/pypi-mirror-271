import pytest

from pytest_exit_code import ExitCode

stash_key = pytest.StashKey["ExitCodePlugin"]()


class ExitCodePlugin:
    def __init__(self) -> None:
        self.exit_code = ExitCode.ALL_PASSED

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.passed and report.when in ["call"]:
            if hasattr(report, "wasxfail"):
                self.exit_code |= ExitCode.TESTS_XPASSED
            else:
                self.exit_code |= ExitCode.TESTS_PASSED

        if report.failed:
            if report.when in ["setup", "teardown"]:
                self.exit_code |= ExitCode.TESTS_ERRORED
            else:
                self.exit_code |= ExitCode.TESTS_FAILED

        if report.skipped:
            if hasattr(report, "wasxfail"):
                self.exit_code |= ExitCode.TESTS_XFAILED
            else:
                self.exit_code |= ExitCode.TESTS_SKIPPED

    @pytest.hookimpl
    def pytest_sessionfinish(self, session: pytest.Session):
        if self.exit_code > ExitCode.TESTS_PASSED:
            session.exitstatus = self.exit_code
        else:
            session.exitstatus = ExitCode.ALL_PASSED


def pytest_configure(config: pytest.Config) -> None:
    plugin = ExitCodePlugin()
    config.stash[stash_key] = plugin
    config.pluginmanager.register(plugin, "exit_code")


def pytest_unconfigure(config: pytest.Config) -> None:
    if plugin := config.stash.get(stash_key, None):
        config.pluginmanager.unregister(plugin)
