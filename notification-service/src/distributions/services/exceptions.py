class NoUserDataExceptionError(Exception):

    def __init__(self, messsage) -> None:
        self.messsage = messsage
        super().__init__(self.messsage)


class RepeatTaskExceptionError(Exception):

    def __init__(self, messsage) -> None:
        self.messsage = messsage
        super().__init__(self.messsage)
