from dslog.types import Level

def default_formatter(*objs, level: Level):
  return (f'[{level}]', *objs)

def level_color(level: Level):
  match level:
    case 'DEBUG': return 'blue'
    case 'INFO': return 'green'
    case 'WARNING': return 'yellow'
    case 'ERROR': return 'red'
    case 'CRITICAL': return 'bold red'

def rich_formatter(*objs, level: Level):
  col = level_color(level)
  return (f'[{col}][{level}][/{col}]', *objs)