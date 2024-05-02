"""System / OS related inventory model."""

import platform
import subprocess
import time
from contextlib import suppress
from datetime import datetime
from typing import Optional

from typing_extensions import Self

from ..data_models.base.timezone import local_now
from ..logger import logger

try:
    import psutil
except ImportError:
    psutil = None

from pydantic import ConfigDict
from pydantic.types import PositiveInt

from ..data_models import ShpModel


class SystemInventory(ShpModel):
    """System / OS related inventory model."""

    uptime: PositiveInt
    # ⤷ seconds
    timestamp: datetime
    # time_delta: timedelta = timedelta(0)  # noqa: ERA001
    # ⤷ lag behind earliest observer, TODO: wrong place

    system: str
    release: str
    version: str

    machine: str
    processor: str

    ptp: Optional[str] = None

    hostname: str

    interfaces: dict = {}  # noqa: RUF012
    # ⤷ tuple with
    #   ip IPvAnyAddress
    #   mac MACStr

    model_config = ConfigDict(str_min_length=0)

    @classmethod
    def collect(cls) -> Self:
        ts = local_now()

        if psutil is None:
            ifs2 = {}
            uptime = 0
            logger.warning(
                "Inventory-Parameters will be missing. "
                "Please install functionality with "
                "'pip install shepherd_core[inventory] -U' first"
            )
        else:
            ifs1 = psutil.net_if_addrs().items()
            ifs2 = {name: (_if[1].address, _if[0].address) for name, _if in ifs1 if len(_if) > 1}
            uptime = time.time() - psutil.boot_time()

        model_dict = {
            "uptime": round(uptime),
            "timestamp": ts,
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node(),
            "interfaces": ifs2,
            # TODO: add free space on /
        }

        with suppress(FileNotFoundError):
            ret = subprocess.run(["/usr/sbin/ptp4l", "-v"], check=False)  # noqa: S603
            model_dict["ptp"] = ret.stdout
            # alternative: check_output - seems to be lighter

        return cls(**model_dict)
