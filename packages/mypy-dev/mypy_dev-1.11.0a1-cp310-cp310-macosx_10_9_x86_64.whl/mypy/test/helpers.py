from __future__ import annotations

import contextlib
import difflib
import os
import pathlib
import re
import shutil
import sys
import time
from typing import IO, Any, Callable, Iterable, Iterator, Pattern

# Exporting Suite as alias to TestCase for backwards compatibility
# TODO: avoid aliasing - import and subclass TestCase directly
from unittest import TestCase

Suite = TestCase  # re-exporting

import pytest

import mypy.api as api
import mypy.version
from mypy import defaults
from mypy.main import process_options
from mypy.options import Options
from mypy.test.config import test_data_prefix, test_temp_dir
from mypy.test.data import DataDrivenTestCase, DeleteFile, UpdateFile, fix_cobertura_filename

skip = pytest.mark.skip

# AssertStringArraysEqual displays special line alignment helper messages if
# the first different line has at least this many characters,
MIN_LINE_LENGTH_FOR_ALIGNMENT = 5


def run_mypy(args: list[str]) -> None:
    __tracebackhide__ = True
    # We must enable site packages even though they could cause problems,
    # since stubs for typing_extensions live there.
    outval, errval, status = api.run(args + ["--show-traceback", "--no-silence-site-packages"])
    if status != 0:
        sys.stdout.write(outval)
        sys.stderr.write(errval)
        pytest.fail(reason="Sample check failed", pytrace=False)


def diff_ranges(
    left: list[str], right: list[str]
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    seq = difflib.SequenceMatcher(None, left, right)
    # note last triple is a dummy, so don't need to worry
    blocks = seq.get_matching_blocks()

    i = 0
    j = 0
    left_ranges = []
    right_ranges = []
    for block in blocks:
        # mismatched range
        left_ranges.append((i, block.a))
        right_ranges.append((j, block.b))

        i = block.a + block.size
        j = block.b + block.size

        # matched range
        left_ranges.append((block.a, i))
        right_ranges.append((block.b, j))
    return left_ranges, right_ranges


def render_diff_range(
    ranges: list[tuple[int, int]],
    content: list[str],
    *,
    colour: str | None = None,
    output: IO[str] = sys.stderr,
    indent: int = 2,
) -> None:
    for i, line_range in enumerate(ranges):
        is_matching = i % 2 == 1
        lines = content[line_range[0] : line_range[1]]
        for j, line in enumerate(lines):
            if (
                is_matching
                # elide the middle of matching blocks
                and j >= 3
                and j < len(lines) - 3
            ):
                if j == 3:
                    output.write(" " * indent + "...\n")
                continue

            if not is_matching and colour:
                output.write(colour)

            output.write(" " * indent + line)

            if not is_matching:
                if colour:
                    output.write("\033[0m")
                output.write(" (diff)")

            output.write("\n")


def assert_string_arrays_equal(expected: list[str], actual: list[str], msg: str) -> None:
    """Assert that two string arrays are equal.

    Display any differences in a human-readable form.
    """
    actual = clean_up(actual)
    if expected != actual:
        expected_ranges, actual_ranges = diff_ranges(expected, actual)
        sys.stderr.write("Expected:\n")
        red = "\033[31m" if sys.platform != "win32" else None
        render_diff_range(expected_ranges, expected, colour=red)
        sys.stderr.write("Actual:\n")
        green = "\033[32m" if sys.platform != "win32" else None
        render_diff_range(actual_ranges, actual, colour=green)

        sys.stderr.write("\n")
        first_diff = next(
            (i for i, (a, b) in enumerate(zip(expected, actual)) if a != b),
            max(len(expected), len(actual)),
        )
        if 0 <= first_diff < len(actual) and (
            len(expected[first_diff]) >= MIN_LINE_LENGTH_FOR_ALIGNMENT
            or len(actual[first_diff]) >= MIN_LINE_LENGTH_FOR_ALIGNMENT
        ):
            # Display message that helps visualize the differences between two
            # long lines.
            show_align_message(expected[first_diff], actual[first_diff])

        sys.stderr.write(
            "Update the test output using --update-data -n0 "
            "(you can additionally use the -k selector to update only specific tests)\n"
        )
        pytest.fail(msg, pytrace=False)


def assert_module_equivalence(name: str, expected: Iterable[str], actual: Iterable[str]) -> None:
    expected_normalized = sorted(expected)
    actual_normalized = sorted(set(actual).difference({"__main__"}))
    assert_string_arrays_equal(
        expected_normalized,
        actual_normalized,
        ('Actual modules ({}) do not match expected modules ({}) for "[{} ...]"').format(
            ", ".join(actual_normalized), ", ".join(expected_normalized), name
        ),
    )


def assert_target_equivalence(name: str, expected: list[str], actual: list[str]) -> None:
    """Compare actual and expected targets (order sensitive)."""
    assert_string_arrays_equal(
        expected,
        actual,
        ('Actual targets ({}) do not match expected targets ({}) for "[{} ...]"').format(
            ", ".join(actual), ", ".join(expected), name
        ),
    )


def show_align_message(s1: str, s2: str) -> None:
    """Align s1 and s2 so that the their first difference is highlighted.

    For example, if s1 is 'foobar' and s2 is 'fobar', display the
    following lines:

      E: foobar
      A: fobar
           ^

    If s1 and s2 are long, only display a fragment of the strings around the
    first difference. If s1 is very short, do nothing.
    """

    # Seeing what went wrong is trivial even without alignment if the expected
    # string is very short. In this case do nothing to simplify output.
    if len(s1) < 4:
        return

    maxw = 72  # Maximum number of characters shown

    sys.stderr.write("Alignment of first line difference:\n")

    trunc = False
    while s1[:30] == s2[:30]:
        s1 = s1[10:]
        s2 = s2[10:]
        trunc = True

    if trunc:
        s1 = "..." + s1
        s2 = "..." + s2

    max_len = max(len(s1), len(s2))
    extra = ""
    if max_len > maxw:
        extra = "..."

    # Write a chunk of both lines, aligned.
    sys.stderr.write(f"  E: {s1[:maxw]}{extra}\n")
    sys.stderr.write(f"  A: {s2[:maxw]}{extra}\n")
    # Write an indicator character under the different columns.
    sys.stderr.write("     ")
    for j in range(min(maxw, max(len(s1), len(s2)))):
        if s1[j : j + 1] != s2[j : j + 1]:
            sys.stderr.write("^")  # Difference
            break
        else:
            sys.stderr.write(" ")  # Equal
    sys.stderr.write("\n")


def clean_up(a: list[str]) -> list[str]:
    """Remove common directory prefix from all strings in a.

    This uses a naive string replace; it seems to work well enough. Also
    remove trailing carriage returns.
    """
    res = []
    pwd = os.getcwd()
    driver = pwd + "/driver.py"
    for s in a:
        prefix = os.sep
        ss = s
        for p in prefix, prefix.replace(os.sep, "/"):
            if p != "/" and p != "//" and p != "\\" and p != "\\\\":
                ss = ss.replace(p, "")
        # Ignore spaces at end of line.
        ss = re.sub(" +$", "", ss)
        # Remove pwd from driver.py's path
        ss = ss.replace(driver, "driver.py")
        res.append(re.sub("\\r$", "", ss))
    return res


@contextlib.contextmanager
def local_sys_path_set() -> Iterator[None]:
    """Temporary insert current directory into sys.path.

    This can be used by test cases that do runtime imports, for example
    by the stubgen tests.
    """
    old_sys_path = sys.path.copy()
    if not ("" in sys.path or "." in sys.path):
        sys.path.insert(0, "")
    try:
        yield
    finally:
        sys.path = old_sys_path


def testfile_pyversion(path: str) -> tuple[int, int]:
    if path.endswith("python312.test"):
        return 3, 12
    elif path.endswith("python311.test"):
        return 3, 11
    elif path.endswith("python310.test"):
        return 3, 10
    elif path.endswith("python39.test"):
        return 3, 9
    elif path.endswith("python38.test"):
        return 3, 8
    else:
        return defaults.PYTHON3_VERSION


def normalize_error_messages(messages: list[str]) -> list[str]:
    """Translate an array of error messages to use / as path separator."""

    a = []
    for m in messages:
        a.append(m.replace(os.sep, "/"))
    return a


def retry_on_error(func: Callable[[], Any], max_wait: float = 1.0) -> None:
    """Retry callback with exponential backoff when it raises OSError.

    If the function still generates an error after max_wait seconds, propagate
    the exception.

    This can be effective against random file system operation failures on
    Windows.
    """
    t0 = time.time()
    wait_time = 0.01
    while True:
        try:
            func()
            return
        except OSError:
            wait_time = min(wait_time * 2, t0 + max_wait - time.time())
            if wait_time <= 0.01:
                # Done enough waiting, the error seems persistent.
                raise
            time.sleep(wait_time)


def good_repr(obj: object) -> str:
    if isinstance(obj, str):
        if obj.count("\n") > 1:
            bits = ["'''\\"]
            for line in obj.split("\n"):
                # force repr to use ' not ", then cut it off
                bits.append(repr('"' + line)[2:-1])
            bits[-1] += "'''"
            return "\n".join(bits)
    return repr(obj)


def assert_equal(a: object, b: object, fmt: str = "{} != {}") -> None:
    __tracebackhide__ = True
    if a != b:
        raise AssertionError(fmt.format(good_repr(a), good_repr(b)))


def typename(t: type) -> str:
    if "." in str(t):
        return str(t).split(".")[-1].rstrip("'>")
    else:
        return str(t)[8:-2]


def assert_type(typ: type, value: object) -> None:
    __tracebackhide__ = True
    if type(value) != typ:
        raise AssertionError(f"Invalid type {typename(type(value))}, expected {typename(typ)}")


def parse_options(
    program_text: str, testcase: DataDrivenTestCase, incremental_step: int
) -> Options:
    """Parse comments like '# flags: --foo' in a test case."""
    options = Options()
    flags = re.search("# flags: (.*)$", program_text, flags=re.MULTILINE)
    if incremental_step > 1:
        flags2 = re.search(f"# flags{incremental_step}: (.*)$", program_text, flags=re.MULTILINE)
        if flags2:
            flags = flags2

    if flags:
        flag_list = flags.group(1).split()
        flag_list.append("--no-site-packages")  # the tests shouldn't need an installed Python
        targets, options = process_options(flag_list, require_targets=False)
        if targets:
            # TODO: support specifying targets via the flags pragma
            raise RuntimeError("Specifying targets via the flags pragma is not supported.")
        if "--show-error-codes" not in flag_list:
            options.hide_error_codes = True
    else:
        flag_list = []
        options = Options()
        options.error_summary = False
        options.hide_error_codes = True
        options.force_uppercase_builtins = True
        options.force_union_syntax = True

    # Allow custom python version to override testfile_pyversion.
    if all(flag.split("=")[0] != "--python-version" for flag in flag_list):
        options.python_version = testfile_pyversion(testcase.file)

    if testcase.config.getoption("--mypy-verbose"):
        options.verbosity = testcase.config.getoption("--mypy-verbose")

    return options


def split_lines(*streams: bytes) -> list[str]:
    """Returns a single list of string lines from the byte streams in args."""
    return [s for stream in streams for s in stream.decode("utf8").splitlines()]


def write_and_fudge_mtime(content: str, target_path: str) -> None:
    # In some systems, mtime has a resolution of 1 second which can
    # cause annoying-to-debug issues when a file has the same size
    # after a change. We manually set the mtime to circumvent this.
    # Note that we increment the old file's mtime, which guarantees a
    # different value, rather than incrementing the mtime after the
    # copy, which could leave the mtime unchanged if the old file had
    # a similarly fudged mtime.
    new_time = None
    if os.path.isfile(target_path):
        new_time = os.stat(target_path).st_mtime + 1

    dir = os.path.dirname(target_path)
    os.makedirs(dir, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as target:
        target.write(content)

    if new_time:
        os.utime(target_path, times=(new_time, new_time))


def perform_file_operations(operations: list[UpdateFile | DeleteFile]) -> None:
    for op in operations:
        if isinstance(op, UpdateFile):
            # Modify/create file
            write_and_fudge_mtime(op.content, op.target_path)
        else:
            # Delete file/directory
            if os.path.isdir(op.path):
                # Sanity check to avoid unexpected deletions
                assert op.path.startswith("tmp")
                shutil.rmtree(op.path)
            else:
                # Use retries to work around potential flakiness on Windows (AppVeyor).
                path = op.path
                retry_on_error(lambda: os.remove(path))


def check_test_output_files(
    testcase: DataDrivenTestCase, step: int, strip_prefix: str = ""
) -> None:
    for path, expected_content in testcase.output_files:
        if path.startswith(strip_prefix):
            path = path[len(strip_prefix) :]
        if not os.path.exists(path):
            raise AssertionError(
                "Expected file {} was not produced by test case{}".format(
                    path, " on step %d" % step if testcase.output2 else ""
                )
            )
        with open(path, encoding="utf8") as output_file:
            actual_output_content = output_file.read()

        if isinstance(expected_content, Pattern):
            if expected_content.fullmatch(actual_output_content) is not None:
                continue
            raise AssertionError(
                "Output file {} did not match its expected output pattern\n---\n{}\n---".format(
                    path, actual_output_content
                )
            )

        normalized_output = normalize_file_output(
            actual_output_content.splitlines(), os.path.abspath(test_temp_dir)
        )
        # We always normalize things like timestamp, but only handle operating-system
        # specific things if requested.
        if testcase.normalize_output:
            if testcase.suite.native_sep and os.path.sep == "\\":
                normalized_output = [fix_cobertura_filename(line) for line in normalized_output]
            normalized_output = normalize_error_messages(normalized_output)
        assert_string_arrays_equal(
            expected_content.splitlines(),
            normalized_output,
            "Output file {} did not match its expected output{}".format(
                path, " on step %d" % step if testcase.output2 else ""
            ),
        )


def normalize_file_output(content: list[str], current_abs_path: str) -> list[str]:
    """Normalize file output for comparison."""
    timestamp_regex = re.compile(r"\d{10}")
    result = [x.replace(current_abs_path, "$PWD") for x in content]
    version = mypy.version.__version__
    result = [re.sub(r"\b" + re.escape(version) + r"\b", "$VERSION", x) for x in result]
    # We generate a new mypy.version when building mypy wheels that
    # lacks base_version, so handle that case.
    base_version = getattr(mypy.version, "base_version", version)
    result = [re.sub(r"\b" + re.escape(base_version) + r"\b", "$VERSION", x) for x in result]
    result = [timestamp_regex.sub("$TIMESTAMP", x) for x in result]
    return result


def find_test_files(pattern: str, exclude: list[str] | None = None) -> list[str]:
    return [
        path.name
        for path in (pathlib.Path(test_data_prefix).rglob(pattern))
        if path.name not in (exclude or [])
    ]
