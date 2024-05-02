from email.policy import default
from typing import Literal, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
from .types import Level, Handler, Formatter, value
from . import loggers, formatters

class LogFn(Protocol):
  def __call__(self, *objs, level: Level = 'INFO'):
    ...

class Logger(ABC, LogFn):
  @abstractmethod
  def __call__(self, *objs, level: Level = 'INFO'):
    ...

  @classmethod
  def of(cls, handler: Handler) -> 'Logger':
    return LoggerOf(handler)

  @classmethod
  def rich(cls) -> 'Logger':
    """Nicely formatted rich logger (use `loggers.rich` aka `Logger.of(rich.print)` for a non-formatted version)"""
    return loggers.rich().format(formatters.rich_formatter)
  
  @classmethod
  def file(cls, filepath: str, *, mode: Literal['w', 'a'] = 'a') -> 'Logger':
    """Default formatted file logger (use `loggers.file` for a non-formatted version)"""
    return loggers.file(filepath, mode=mode).format(formatters.default_formatter)
  
  @classmethod
  def empty(cls) -> 'Logger':
    """A logger that doesn't do anything"""
    return LoggerOf(lambda *_, **_kw: None)

  def limit(self, min_level: Level) -> 'Logger':
    return Limited(min_level, self)
  
  def format(self, format: Formatter) -> 'Logger':
    return Formatted(format, self)
  
  def prefix(self, prefix: str) -> 'Logger':
    return self.format(lambda *objs, **_: (prefix, *objs))
  
  def postfix(self, postfix: str) -> 'Logger':
    return self.format(lambda *objs, **_: (*objs, postfix))
  
@dataclass
class LoggerOf(Logger):
  handler: Handler
  def __call__(self, *objs, **_):
    self.handler(*objs)

@dataclass
class Limited(Logger):
  min_level: Level | int
  logger: Logger

  def __call__(self, *objs, level: Level = 'INFO'):
    if value(level) >= value(self.min_level):
      self.logger(*objs, level=level)

@dataclass
class Formatted(Logger):
  formatter: Formatter
  logger: Logger

  def __call__(self, *objs, level: Level = 'INFO'):
    formatted_objs = self.formatter(*objs, level=level)
    self.logger(*formatted_objs, level=level)