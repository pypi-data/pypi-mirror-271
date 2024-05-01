from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .action_config import Action_config
    from .action_secrets import Action_secrets
    from .github_issue_comment_action_config import GithubIssueCommentActionConfig
    from .github_issue_create_action_config import GithubIssueCreateActionConfig
    from .http_action_config import HttpActionConfig
    from .slack_channel_message_action_config import SlackChannelMessageActionConfig

@dataclass
class Action(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The active property
    active: Optional[bool] = None
    # The config property
    config: Optional[Action_config] = None
    # The event property
    event: Optional[str] = None
    # The id property
    id: Optional[int] = None
    # The runAlways property
    run_always: Optional[bool] = None
    # The secrets property
    secrets: Optional[Action_secrets] = None
    # The testId property
    test_id: Optional[int] = None
    # The type property
    type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> Action:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Action
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return Action()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .action_config import Action_config
        from .action_secrets import Action_secrets
        from .github_issue_comment_action_config import GithubIssueCommentActionConfig
        from .github_issue_create_action_config import GithubIssueCreateActionConfig
        from .http_action_config import HttpActionConfig
        from .slack_channel_message_action_config import SlackChannelMessageActionConfig

        from .action_config import Action_config
        from .action_secrets import Action_secrets
        from .github_issue_comment_action_config import GithubIssueCommentActionConfig
        from .github_issue_create_action_config import GithubIssueCreateActionConfig
        from .http_action_config import HttpActionConfig
        from .slack_channel_message_action_config import SlackChannelMessageActionConfig

        fields: Dict[str, Callable[[Any], None]] = {
            "active": lambda n : setattr(self, 'active', n.get_bool_value()),
            "config": lambda n : setattr(self, 'config', n.get_object_value(Action_config)),
            "event": lambda n : setattr(self, 'event', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "runAlways": lambda n : setattr(self, 'run_always', n.get_bool_value()),
            "secrets": lambda n : setattr(self, 'secrets', n.get_object_value(Action_secrets)),
            "testId": lambda n : setattr(self, 'test_id', n.get_int_value()),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_bool_value("active", self.active)
        writer.write_object_value("config", self.config)
        writer.write_str_value("event", self.event)
        writer.write_int_value("id", self.id)
        writer.write_bool_value("runAlways", self.run_always)
        writer.write_object_value("secrets", self.secrets)
        writer.write_int_value("testId", self.test_id)
        writer.write_str_value("type", self.type)
        writer.write_additional_data_value(self.additional_data)
    
    from kiota_abstractions.serialization import ComposedTypeWrapper

    @dataclass
    class Action_config(ComposedTypeWrapper, Parsable):
        from kiota_abstractions.serialization import ComposedTypeWrapper

        if TYPE_CHECKING:
            from .github_issue_comment_action_config import GithubIssueCommentActionConfig
            from .github_issue_create_action_config import GithubIssueCreateActionConfig
            from .http_action_config import HttpActionConfig
            from .slack_channel_message_action_config import SlackChannelMessageActionConfig

        """
        Composed type wrapper for classes GithubIssueCommentActionConfig, GithubIssueCreateActionConfig, HttpActionConfig, SlackChannelMessageActionConfig
        """
        @staticmethod
        def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> Action_config:
            """
            Creates a new instance of the appropriate class based on discriminator value
            param parse_node: The parse node to use to read the discriminator value and create the object
            Returns: Action_config
            """
            if not parse_node:
                raise TypeError("parse_node cannot be null.")
            try:
                mapping_value = parse_node.get_child_node("type").get_str_value()
            except AttributeError:
                mapping_value = None
            result = Action_config()
            if mapping_value and mapping_value.casefold() == "github-issue-comment".casefold():
                from .github_issue_comment_action_config import GithubIssueCommentActionConfig

                result.github_issue_comment_action_config = GithubIssueCommentActionConfig()
            elif mapping_value and mapping_value.casefold() == "github-issue-create".casefold():
                from .github_issue_create_action_config import GithubIssueCreateActionConfig

                result.github_issue_create_action_config = GithubIssueCreateActionConfig()
            elif mapping_value and mapping_value.casefold() == "http".casefold():
                from .http_action_config import HttpActionConfig

                result.http_action_config = HttpActionConfig()
            elif mapping_value and mapping_value.casefold() == "slack-channel-message".casefold():
                from .slack_channel_message_action_config import SlackChannelMessageActionConfig

                result.slack_channel_message_action_config = SlackChannelMessageActionConfig()
            return result
        
        def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
            """
            The deserialization information for the current model
            Returns: Dict[str, Callable[[ParseNode], None]]
            """
            from .github_issue_comment_action_config import GithubIssueCommentActionConfig
            from .github_issue_create_action_config import GithubIssueCreateActionConfig
            from .http_action_config import HttpActionConfig
            from .slack_channel_message_action_config import SlackChannelMessageActionConfig

            if self.github_issue_comment_action_config:
                return self.github_issue_comment_action_config.get_field_deserializers()
            if self.github_issue_create_action_config:
                return self.github_issue_create_action_config.get_field_deserializers()
            if self.http_action_config:
                return self.http_action_config.get_field_deserializers()
            if self.slack_channel_message_action_config:
                return self.slack_channel_message_action_config.get_field_deserializers()
            return {}
        
        def serialize(self,writer: SerializationWriter) -> None:
            """
            Serializes information the current object
            param writer: Serialization writer to use to serialize this model
            Returns: None
            """
            if not writer:
                raise TypeError("writer cannot be null.")
            if self.github_issue_comment_action_config:
                writer.write_object_value(None, self.github_issue_comment_action_config)
            elif self.github_issue_create_action_config:
                writer.write_object_value(None, self.github_issue_create_action_config)
            elif self.http_action_config:
                writer.write_object_value(None, self.http_action_config)
            elif self.slack_channel_message_action_config:
                writer.write_object_value(None, self.slack_channel_message_action_config)
        
    

