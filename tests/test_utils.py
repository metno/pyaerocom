from pathlib import Path

import pytest

from pyaerocom import utils


def test_print_file(tmp_path: Path, capsys):
    path = tmp_path / "file.txt"
    text = "Blaaaa\nBlub\n"
    path.write_text(text)

    utils.print_file(path)
    captured = capsys.readouterr()
    assert captured.out == text


def test_print_file_error(tmp_path: Path):
    path = tmp_path / "file.txt"
    assert not path.exists()
    with pytest.raises(IOError) as e:
        utils.print_file(path)
    assert str(e.value) == "File not found..."

    folder = tmp_path / "not_a_file"
    folder.mkdir()
    with pytest.raises(ValueError) as e:
        utils.print_file(folder)
    assert str(e.value) == f"{folder} is not a file"


@pytest.mark.parametrize(
    "kwargs,tabshape",
    [
        pytest.param(
            dict(model_ids="TM5-met2010_CTRL-TEST", vars_or_var_patterns="abs550*"),
            (2, 11),
            id="varinfo abs550*",
        ),
        pytest.param(
            dict(model_ids="TM5-met2010_CTRL-TEST", vars_or_var_patterns="*550*"),
            (4, 11),
            id="varinfo *550*",
        ),
        pytest.param(
            dict(
                model_ids="TM5-met2010_CTRL-TEST", vars_or_var_patterns="od550aer", read_data=True
            ),
            (2, 11),
            id="read od550aer",
        ),
    ],
)
def test_create_varinfo_table(kwargs, tabshape):
    df = utils.create_varinfo_table(**kwargs)
    assert df.shape == tabshape


@pytest.mark.parametrize(
    "kwargs,error",
    [
        pytest.param(
            dict(),
            "missing 2 required positional arguments: 'model_ids' and 'vars_or_var_patterns'",
            id="no args",
        ),
        pytest.param(
            dict(model_ids="TM5-met2010_CTRL-TEST"),
            "missing 1 required positional argument: 'vars_or_var_patterns'",
            id="no vars_or_var_patterns",
        ),
        pytest.param(
            dict(vars_or_var_patterns="od550aer"),
            "missing 1 required positional argument: 'model_ids'",
            id="no model_ids",
        ),
    ],
)
def test_create_varinfo_table_error(kwargs, error):
    with pytest.raises(TypeError) as e:
        utils.create_varinfo_table(**kwargs)
    assert str(e.value).endswith(error)
