from enum import IntFlag


class ExitCode(IntFlag):
    ALL_PASSED = 0
    TESTS_PASSED = 1
    TESTS_FAILED = 2
    TESTS_ERRORED = 4
    TESTS_SKIPPED = 8
    TESTS_XFAILED = 16
    TESTS_XPASSED = 32
