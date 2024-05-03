from dig_ass_critic_protos.DigitalAssistantCritic_pb2_grpc import (
    DigitalAssistantCriticStub,
)
from dig_ass_critic_protos.DigitalAssistantCritic_pb2 import (
    DigitalAssistantCriticRequest,
    DigitalAssistantCriticResponse,
    ChatItem,
    OuterContextItem,
    InnerContextItem,
    ReplicaItem,
)

from .abstract_client import AbstractClient


class CriticClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantCriticStub(self._channel)

    def __call__(self, text: str, chat: dict):
        outer_context = chat['OuterContext']
        inner_context = chat['InnerContext']
        request = DigitalAssistantCriticRequest(
            Text=text,
            Chat=ChatItem(
                OuterContext=OuterContextItem(
                    Sex=outer_context['Sex'],
                    Age=outer_context['Age'],
                    UserId=outer_context['UserId'],
                    SessionId=outer_context['SessionId'],
                    ClientId=outer_context['ClientId'],
                ),
                InnerContext=InnerContextItem(
                    Replicas=[
                        self.rep_to_obj(replica)
                        for replica in inner_context['Replicas']
                    ]
                ),
            ),
        )
        response: DigitalAssistantCriticResponse = self._stub.GetTextResponse(request)
        return response.Score

    def rep_to_obj(self, replica_dict):
        return ReplicaItem(
            Body=replica_dict['Body'],
            Role=replica_dict['Role'],
            DateTime=replica_dict['DateTime'],
        )
