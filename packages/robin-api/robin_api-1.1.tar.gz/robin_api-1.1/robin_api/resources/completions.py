


from typing import TYPE_CHECKING, Dict, List, Union, Optional, overload, Iterator
from ..types import Completion, CompletionChoice, ChatCompletionChunk
from .._streaming import Stream
from typing_extensions import Literal
import httpx
from .._types import NOT_GIVEN, NotGiven
from .._resource import SyncAPIResource
from .._models import construct_type, construct_type_v2
import json

if TYPE_CHECKING:
    from .._client import RobinAIClient

__all__ = ["Completions"]



def ensure_list(value, key):
    if key in value and not isinstance(value[key], list):
        value[key] = [value[key]]


class Completions(SyncAPIResource):
    #from .._client import RobinAIClient
    def __init__(self, client) -> None:
        super().__init__(client)

    

    def create(
        self,
        *,
        model: Union[
            str,
            Literal[
                "ROBIN_4",
                "ROBIN_3",
            ],
        ],
        conversation: Union[str, List[str], List[int], List[List[int]], None],
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        save_response: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,

    ) -> Completion | Stream[Completion] | Iterator[Stream[Completion]]:
        
        with self._client.http_client.stream(
             url = "get-response",
             #url = "https://localhost:8443/api/api-response-service/get-response",
             method="POST",
             json= {
                    "model": model,
                    "conversation": conversation,
                    "max_new_tokens": max_tokens,
                    "stream": stream,
                    "temperature": temperature,
                    "save_response": save_response
                },
             ) as response:
            if response.status_code == 200:
                for data in response.iter_bytes():
                    json_part = data.decode('utf-8').split("data: ", 1)[1]
                    if json_part.startswith("DONE"):
                        break
                    objeto = json.loads(json_part)
                    ensure_list(objeto, 'choices')
                    completion_obj = construct_type_v2(type_=ChatCompletionChunk, value=objeto)
                    yield completion_obj
            else:
                raise ConnectionError(f"Error: {str(response.status_code)}")
                
        

        """return self.client.http_client._post(
            "/completions",
            body=maybe_transform(
                {
                    "model": model,
                    "conversation": conversation,
                    "best_of": best_of,
                    "echo": echo,
                    "frequency_penalty": frequency_penalty,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_tokens": max_tokens,
                    "n": n,
                    "presence_penalty": presence_penalty,
                    "seed": seed,
                    "stop": stop,
                    "stream": stream,
                    "suffix": suffix,
                    "temperature": temperature,
                    "top_p": top_p,
                    "user": user,
                },
                completion_create_params.CompletionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Completion,
            stream=stream or False,
            stream_cls=Stream[Completion],
        ) """




