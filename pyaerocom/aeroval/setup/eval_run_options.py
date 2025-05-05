from pydantic import BaseModel


class EvalRunOptions(BaseModel):
    clear_existing_json: bool = True
    only_json: bool = False
    only_colocation: bool = False
    #: If True, process only maps (skip obs evaluation)
    only_model_maps: bool = False
    obs_only: bool = False
