# BEGIN
# UNCOMMENT from MODULE import Pipelines
# LOOP TSKID
# UNCOMMENT from ._TSKID import TSKID
# END
from ._types import Pipelines # DELETE
from typing import Any # DELETE
TSKID: Any = ... # DELETE

PIPELINES: Pipelines = Pipelines(
  # LOOP TSKID
  TSKID=TSKID,
  # END
)

__all__ = [
  # LOOP TSKID
  'TSKID',
  # END
  'PIPELINES',
]
# END
from typing import Sequence
from templang import parse

def pipelines_init(tasks: Sequence[str], types_module: str):
  with open(__file__) as f:
    source = f.read()
  return parse(source, { 'TSKID': tasks, 'MODULE': types_module })