import logging
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class CAMS2_83Setup(BaseModel):
    use_cams2_83: bool = False
