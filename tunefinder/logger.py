from tunefinder.constants.colors import Colors


def construct_message(message: str, prefix: str = "", color: str = Colors.ENDC):
    return f'{color}{prefix} {message}{Colors.ENDC}'


def info(message: str, end='\n'):
    print(construct_message(message, prefix='ℹ'), end=end)


def warn(message: str, end='\n'):
    print(construct_message(message, prefix='⚠', color=Colors.WARNING), end=end)


def error(message: str, end='\n'):
    print(construct_message(message, prefix='❗', color=Colors.FAIL), end=end)


def success(message: str, end='\n'):
    print(construct_message(message, prefix='✅', color=Colors.OKGREEN), end=end)


def progress(message: str, current: int, total: int):
    print(construct_message(
        f"{message} {current}/{total}...", prefix='⌚', color=Colors.OKBLUE), end='\r')
