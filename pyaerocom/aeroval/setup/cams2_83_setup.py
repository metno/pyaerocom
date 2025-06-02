from pydantic import BaseModel


class CAMS2_83Setup(BaseModel):
    use_cams2_83: bool = False
    use_cams2_83_fairmode: bool = False
