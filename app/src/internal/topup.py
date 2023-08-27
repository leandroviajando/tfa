import logging
import random
from typing import Protocol

from src import models

logger = logging.getLogger(__name__)


class TopupService(Protocol):
    async def __call__(self, transfer_command: models.TransferCommand) -> None:
        ...


class WireTransferService(TopupService):
    async def __call__(self, transfer_command: models.TransferCommand) -> None:
        if random.random() < 0.5:
            raise Exception("Simulate wire transfer failure")

        logger.info("Performing wire transfer: %s", transfer_command)
