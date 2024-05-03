from argparse import ArgumentParser

from ip_reveal.__about__ import __PROG__ as PROG_NAME, __DESCRIPTION__ as PROG_DESCRIPTION, __VERSION__ as VERSION


LEVELS = ['debug', 'info', 'warning', 'error', 'critical']


class Arguments(ArgumentParser):

    __auto_parse       = False
    __prog_name        = PROG_NAME
    __prog_description = PROG_DESCRIPTION
    __parsed           = False
    __parse_on_query   = False


    def __init__(self, *args, auto_parse=__auto_parse, parse_on_query=__parse_on_query, **kwargs):
        super().__init__(*args, **kwargs)

        self.description = self.__prog_description
        self.prog        = self.__prog_name

        self.__auto_parse = auto_parse

        if not self.auto_parse:
            self.parse_on_query = parse_on_query

        self.build_parser()

        if self.auto_parse:
            self.parse_args()

    @property
    def auto_parse(self):
        return self.__auto_parse

    @property
    def parsed(self):
        return self.__parsed

    @property
    def parse_on_query(self):
        return self.__parse_on_query

    @parse_on_query.setter
    def parse_on_query(self, new):
        if self.parsed:
            raise RuntimeError("Cannot change 'parse_on_query' after parsing has occurred!")

        if not isinstance(new, bool):
            raise TypeError('"parse_on_query" must be a boolean value!')

        self.__parse_on_query = new

    def build_parser(self):

        self.add_argument(
            '-l',
            '--log-level',
            action='store',
            required=False,
            choices=LEVELS,
            default='info',
            help='The level at which you\'d like the logger to output.'
        )

        self.add_argument(
            '-m',
            '--mute-all',
            action='store_true',
            required=False,
            help='Starts the program with all program audio muted.',
            default=False
        )

        self.add_argument(
            '-r',
            '--refresh-interval',
            type=int,
            default=30,
            help='Specify the number of seconds you want to have pass before IP-Reveal refreshes your IP '
                 'information. (Defaults to 30)',
            action='store',
            required=False
        )

        self.add_argument(
            '-V',
            '--version',
            action='version',
            version=VERSION,
            required=False,
            help='Show the version number and exit.'
        )

        sub_parsers = self.add_subparsers(
            dest='subcommands',
            help='The sub-commands for IP Reveal'
        )

        ext_ip_parse = sub_parsers.add_parser(
            'get-external',
            help='Return the external IP to the command-line and nothing else.'
        )

        host_parse = sub_parsers.add_parser(
            'get-host',
            help='Return the hostname to the command-line and nothing else.'
        )

        local_parse = sub_parsers.add_parser(
            'get-local',
            help='Return the local IP-Address to the command-line and nothing else.'
        )

        test_audio_parse = sub_parsers.add_parser(
            'test-audio',
            help="To ensure you get notifications you can test IP-Reveal's audio engine with this command."
        )

        test_audio_parse.add_argument(
            '-c',
            '--countdown',
            action='store',
            type=int,
            default=3,
            help="Enter the number to countdown from before starting the test."
        )

        test_audio_parse.add_argument(
            '-f',
            '--full',
            help='Run the full range of audio tests provided by the audio engine',
            action='store_true',
            default=False
        )

    def parse_args(self, *args, **kwargs):
        super().parse_args(*args, **kwargs)
        self.__parsed = True
