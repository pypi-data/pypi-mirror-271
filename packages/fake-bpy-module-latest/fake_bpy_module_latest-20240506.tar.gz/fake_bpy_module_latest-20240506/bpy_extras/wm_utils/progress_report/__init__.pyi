import typing

GenericType = typing.TypeVar("GenericType")

class ProgressReport:
    """ """

    curr_step: typing.Any
    """ """

    running: typing.Any
    """ """

    start_time: typing.Any
    """ """

    steps: typing.Any
    """ """

    wm: typing.Any
    """ """

    def enter_substeps(self, nbr, msg):
        """

        :param nbr:
        :param msg:
        """
        ...

    def finalize(self):
        """ """
        ...

    def initialize(self, wm):
        """

        :param wm:
        """
        ...

    def leave_substeps(self, msg):
        """

        :param msg:
        """
        ...

    def start(self):
        """ """
        ...

    def step(self, msg, nbr):
        """

        :param msg:
        :param nbr:
        """
        ...

    def update(self, msg):
        """

        :param msg:
        """
        ...

class ProgressReportSubstep:
    """ """

    final_msg: typing.Any
    """ """

    level: typing.Any
    """ """

    msg: typing.Any
    """ """

    nbr: typing.Any
    """ """

    progress: typing.Any
    """ """

    def enter_substeps(self, nbr, msg):
        """

        :param nbr:
        :param msg:
        """
        ...

    def leave_substeps(self, msg):
        """

        :param msg:
        """
        ...

    def step(self, msg, nbr):
        """

        :param msg:
        :param nbr:
        """
        ...
