# Root level conftest to ignore scripts folder in doctests.
def pytest_ignore_collect(collection_path):
    if "scripts/" in str(collection_path):
        return True
    if "docs/" in str(collection_path):
        return True
