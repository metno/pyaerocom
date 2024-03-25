import json
from importlib import metadata
from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyaerocom.scripts.cams2_83.cli import main

runner = CliRunner()



@pytest.fixture()
def config_json(monkeypatch, tmp_path: Path, eval_config: dict) -> Path:
    def do_not_run(self, model_name=None, obs_name=None, var_list=None, update_interface=True):
        assert model_name is None
        assert obs_name is None
        assert var_list is None
        assert update_interface is True

    monkeypatch.setattr("pyaerocom.scripts.cli.ExperimentProcessor.run", do_not_run)

    path = tmp_path / "conf.json"
    path.write_text(json.dumps(eval_config))
    return path


#@pytest.mark.parametrize("cfg", ("cfgexp1",))
#def test_aeroval(config_json: Path):
#    assert config_json.is_file()
#    result = runner.invoke(main, ["aeroval", str(config_json)])
#    assert result.exit_code == 0
