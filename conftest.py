# Root level conftest to ignore scripts folder in doctests.
def pytest_ignore_collect(path):
    if "scripts/" in str(path):
        return True
    if "docs/" in str(path):
        return True
