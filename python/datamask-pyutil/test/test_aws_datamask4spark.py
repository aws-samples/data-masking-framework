import pytest


@pytest.mark.xfail
def test_that_you_wrote_tests():
    from textwrap import dedent

    assertion_string = dedent(
        """\
    No, you have not written tests.

    However, unless a test is run, the pytest execution will fail
    due to no tests or missing coverage. So, write a real test and
    then remove this!
    """
    )
    assert False, assertion_string


def test_aws_datamask4spark_importable():
    import aws_datamask4spark  # noqa: F401
