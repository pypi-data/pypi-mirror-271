# Copyright (c) Alibaba, Inc. and its affiliates.
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional


def random_uuid() -> str:
    return str(uuid.uuid4().hex)


@dataclass
class Model:
    id: str  # model_type
    object: str = 'model'
    created: int = field(default_factory=lambda: int(time.time()))
    owned_by: str = 'swift'


@dataclass
class ModelList:
    data: List[Model]
    object: str = 'list'


@dataclass
class XRequestConfig:
    """NOTE: The following behavior is inconsistent with the OpenAI API.
    Default values for OpenAI:
        temperature = 1.
        top_k = -1
        top_p = 1.
        repetition_penalty = 1.
    """
    max_tokens: Optional[int] = None  # None: max_model_len - num_tokens
    # None: use deploy_args
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    repetition_penalty: Optional[float] = None

    n: int = 1
    seed: Optional[int] = None
    stop: List[str] = field(default_factory=list)
    stream: bool = False

    best_of: Optional[int] = None
    presence_penalty: float = 0.
    frequency_penalty: float = 0.
    length_penalty: float = 1.

    # additional
    num_beams: int = 1
    top_k: Optional[int] = None  # None: use deploy_args


@dataclass
class CompletionRequestMixin:
    model: str
    prompt: str


@dataclass
class ChatCompletionRequestMixin:
    model: str
    messages: List[Dict[str, str]]


@dataclass
class CompletionRequest(XRequestConfig, CompletionRequestMixin):
    pass


@dataclass
class ChatCompletionRequest(XRequestConfig, ChatCompletionRequestMixin):
    pass


@dataclass
class UsageInfo:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass
class ChatMessage:
    role: Literal['system', 'user', 'assistant']
    content: str


@dataclass
class ChatCompletionResponseChoice:
    index: int
    message: ChatMessage
    finish_reason: Literal['stop', 'length', None]  # None: for infer_backend='pt'


@dataclass
class CompletionResponseChoice:
    index: int
    text: str
    finish_reason: Literal['stop', 'length', None]  # None: for infer_backend='pt'


@dataclass
class ChatCompletionResponse:
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: UsageInfo
    id: str = field(default_factory=lambda: f'chatcmpl-{random_uuid()}')
    object: str = 'chat.completion'
    created: int = field(default_factory=lambda: int(time.time()))


@dataclass
class CompletionResponse:
    model: str
    choices: List[CompletionResponseChoice]
    usage: UsageInfo
    id: str = field(default_factory=lambda: f'cmpl-{random_uuid()}')
    object: str = 'text_completion'
    created: int = field(default_factory=lambda: int(time.time()))


@dataclass
class DeltaMessage:
    role: Literal['system', 'user', 'assistant']
    content: str


@dataclass
class ChatCompletionResponseStreamChoice:
    index: int
    delta: DeltaMessage
    finish_reason: Literal['stop', 'length', None]


@dataclass
class ChatCompletionStreamResponse:
    model: str
    choices: List[ChatCompletionResponseStreamChoice]
    usage: UsageInfo
    id: str = field(default_factory=lambda: f'chatcmpl-{random_uuid()}')
    object: str = 'chat.completion.chunk'
    created: int = field(default_factory=lambda: int(time.time()))


@dataclass
class CompletionResponseStreamChoice:
    index: int
    text: str
    finish_reason: Literal['stop', 'length', None]


@dataclass
class CompletionStreamResponse:
    model: str
    choices: List[CompletionResponseStreamChoice]
    usage: UsageInfo
    id: str = field(default_factory=lambda: f'cmpl-{random_uuid()}')
    object: str = 'text_completion.chunk'
    created: int = field(default_factory=lambda: int(time.time()))
