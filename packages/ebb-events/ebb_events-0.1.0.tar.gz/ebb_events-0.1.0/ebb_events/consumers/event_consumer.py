import copy
from datetime import datetime
from marshmallow import ValidationError
from ebb_events.constants import DATA, ID, METADATA, SOURCE, TIME, TYPE
from ebb_events.builders.event_builder import EventEnvelope
from ebb_events.event_schema import EventPayloadSchema
from ebb_events.exceptions import PayloadFormatException


class EventConsumer:
    """
    Class to consume and parse events that follow the ebb_event structure
    """

    def __init__(self, payload: dict = {}) -> None:
        """
        Initializes an EventConsumer object with payload data
        """
        self.raw_payload: dict = payload
        self.is_ebb_event_structure: bool = self.check_is_ebb_event_structure(
            payload=self.raw_payload
        )

    def check_is_ebb_event_structure(self, payload: dict) -> bool:
        """
        Helper checks the payload structure to see if it matches our EventPayloadSchema
        """
        payload_schema = EventPayloadSchema()
        try:
            payload_schema.load(data=payload)
            return True
        except ValidationError:
            return False

    def get_event_id(self) -> str:
        """
        Helper to fetch event's id field as str(id)

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            str: event's string id
        """
        if self.is_ebb_event_structure:
            return str(self.raw_payload.get(ID))
        raise PayloadFormatException()

    def get_event_time_str(self) -> str:
        """
        Helper to fetch event's time field in RFC3339 format: YYYY-MM-DDThh:mm:ss.ssssss+/-hh:mm

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            str: event's time field
        """
        if self.is_ebb_event_structure:
            return str(self.raw_payload.get(TIME))
        raise PayloadFormatException()

    def get_event_time(self) -> datetime:
        """
        Helper to fetch event's time field as python datetime object

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            datetime: event's time field
        """
        if self.is_ebb_event_structure:
            return datetime.fromisoformat(self.raw_payload.get(TIME))
        raise PayloadFormatException()

    def get_event_source(self) -> str:
        """
        Helper to fetch event's source as string. For ebb_events, the `source` field matches the MQTT `topic`

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            str: event's source field
        """
        if self.is_ebb_event_structure:
            return str(self.raw_payload.get(SOURCE))
        raise PayloadFormatException()

    def get_event_topic(self) -> str:
        """
        Helper to fetch event's topic string. For ebb_events, the MQTT `topic` field matches the event's source

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            str: event's topic string
        """
        return self.get_event_source()

    def get_event_type(self) -> str:
        """
        Helper to fetch event's type as string

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            str: event's type field
        """
        if self.is_ebb_event_structure:
            return str(self.raw_payload.get(TYPE))
        raise PayloadFormatException()

    def get_event_organization(self) -> str:
        """
        Helper to fetch event's organization portion of topic hierarchy as string
        This is the top level of the topic hierarchy

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            str: event's organization portion of the topic hierarchy
        """
        # This ensures that the `source` field matches the expected topic structure
        if self.is_ebb_event_structure:
            topic_list = self.raw_payload.get(SOURCE).split("/")
            return topic_list[0]
        raise PayloadFormatException()

    def get_event_system_id(self) -> str:
        """
        Helper to fetch event's system_id portion of topic hierarchy as string
        This is the second level of the topic hierarchy

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            str: event's system_id portion of the topic hierarchy
        """
        # This ensures that the `source` field matches the expected topic structure
        if self.is_ebb_event_structure:
            topic_list = self.raw_payload.get(SOURCE).split("/")
            return topic_list[1]
        raise PayloadFormatException()

    def get_event_subsystem_id(self) -> str:
        """
        Helper to fetch event's subsystem_id portion of topic hierarchy as string
        This is the fourth level of the topic hierarchy

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            str: event's subsystem_id portion of the topic hierarchy
        """
        # This ensures that the `source` field matches the expected topic structure
        if self.is_ebb_event_structure:
            topic_list = self.raw_payload.get(SOURCE).split("/")
            return topic_list[3]
        raise PayloadFormatException()

    def get_event_device_id(self) -> str:
        """
        Helper to fetch event's device_id portion of topic hierarchy as string
        This is the fourth level of the topic hierarchy

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            str: event's device_id portion of the topic hierarchy
        """
        # This ensures that the `source` field matches the expected topic structure
        if self.is_ebb_event_structure:
            topic_list = self.raw_payload.get(SOURCE).split("/")
            return topic_list[4]
        raise PayloadFormatException()

    def get_event_envelope(self) -> EventEnvelope:
        """
        Helper to build and return EventEnvelope from payload

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            EventEnvelope: event envelope object with expected fields
        """
        if self.is_ebb_event_structure:
            return EventEnvelope(
                organization=self.get_event_organization(),
                system_id=self.get_event_system_id(),
                event_type=self.get_event_type(),
                subsystem_id=self.get_event_subsystem_id(),
                device_id=self.get_event_device_id(),
            )
        raise PayloadFormatException()

    def get_event_message(self, metadata_included=True) -> dict:
        """
        Helper fetches and returns message json from payload
        Metadata field in the message json is included by default but can be parsed out

        Args:
            metadata_included (bool, optional): If set to False, returned dict will remove the `metadata` portion of the message.
                                                Defaults to True.

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            dict: Message value of payload with or without the `metadata` field depending on metadata_included parameter
        """
        if self.is_ebb_event_structure:
            # Copy of message so that we don't actually alter the raw_payload itself
            message: dict = copy.deepcopy(self.raw_payload.get(DATA))
            if not metadata_included:
                message.pop(METADATA, {})
            return message
        raise PayloadFormatException()

    def get_event_message_metadata(self) -> dict:
        """
        Helper to fetch and return the metadata dictionary within the payload's event message json

        Raises:
            PayloadFormatException: Raised if event does not match ebb_event structure

        Returns:
            dict: Metadata included in event message json
        """
        if self.is_ebb_event_structure:
            return self.raw_payload.get(DATA, {}).get(METADATA, {})
        raise PayloadFormatException()
