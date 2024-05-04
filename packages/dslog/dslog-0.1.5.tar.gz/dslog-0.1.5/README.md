# Dead Simple Logging

> What python's `logging` should've been

## Installation

```bash
pip install dslog
```

## Usage

- Any custom "handler" (aka function to actually print)

```python
import rich
from dslog import Logger

logger = Logger.of(rich.print) \
  .limit('WARNING') \
  .format(lambda *objs, level: (f'[bold][{level}][/]', *objs))

logger('My message', ..., level='INFO')
# doesn't print anything
logger('Oops!', { 'more': 'details' }, level='WARNING')
# [WARNING] Oops! { 'more', 'details' }     ([WARNING] in bold text)
```

- Or some of the predefined ones, which come already formatted

```python
Logger.rich()
Logger.file('log.txt')
```

- Or the best default logger

```python
Logger.empty()
```