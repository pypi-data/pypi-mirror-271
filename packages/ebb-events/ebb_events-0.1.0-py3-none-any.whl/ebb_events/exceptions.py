class TopicFormatException(Exception):
    """Exception type raised for invalid topic structure/format"""

    pass


class PayloadFormatException(Exception):
    """Exception type raised for invalid payload structure/format"""

    def __init__(self, message="Payload does not match required ebb_event format"):
        self.message = message
        super().__init__(self.message)
