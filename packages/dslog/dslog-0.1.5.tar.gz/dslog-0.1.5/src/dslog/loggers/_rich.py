from rich import print
from ..logger import Logger

def rich() -> Logger:
  return Logger.of(print)