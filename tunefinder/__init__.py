import sys
from tunefinder import logger

MIN_SUPPORTED_PYTHON_VERSION = (3, 10)
if sys.version_info < MIN_SUPPORTED_PYTHON_VERSION:
    raise ImportError(
        f'You are using an unsupported version of Python. Only Python versions {MIN_SUPPORTED_PYTHON_VERSION[0]}.{MIN_SUPPORTED_PYTHON_VERSION[1]} and above are supported.')


def parse_arguments():
    from tunefinder.platforms import SUPPORTED_DESTINATION_PLATFORMS
    from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

    parser = ArgumentParser(prog='tunefinder',
                            description='Tunefinder', formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("source", help="Source URL")
    parser.add_argument(
        "destination", help="Target platform", choices=SUPPORTED_DESTINATION_PLATFORMS)

    parser.add_argument("--minimal", "-m", help="Generate minimal output",
                        action="store_true", default=False)
    parser.add_argument("--output-format", "-f", help="Output format",
                        choices=['json', 'txt'], default='json')

    return parser.parse_args()


def write_results_to_file(date, args, result):
    file_ext = 'txt' if args.output_format == 'txt' else 'json'
    file_name = f"{date}_{result.source.id}-to-{result.destination.id}.{file_ext}"

    f = open(file_name, mode="w", encoding="utf-8")
    if (args.output_format == 'txt'):
        f.write(result.toTXT())
    else:
        f.write(result.toJSON(minimal=args.minimal))
    f.close()

    logger.success(f'Result written to {file_name}')


async def main():
    try:
        args = parse_arguments()

        from .Tunefinder import Tunefinder
        results = await Tunefinder(args).main()

        from datetime import datetime
        date = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')

        write_results_to_file(date, args, results)
    except KeyboardInterrupt:
        logger.error('Execution interrupted')
        exit(1)
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        exit(1)


def __main__():
    from asyncio import get_event_loop
    loop = get_event_loop()
    loop.run_until_complete(main())
