from .._core import NamedModel, Message, MissingDependencyError
from .._util import sha_digest

try:
    from transformers import pipeline
except ImportError as err:
    raise MissingDependencyError("Please install transformers library") from err


class HFModelPipeline(NamedModel):
    """
    Model loaded from HuggingFace hub.

    - **hf_name** (`str`): name of the model on HuggingFace hub.
    - **model_params** (`dict[str,Any]`): Other pipeline params, will be passed as-is to the
            HF pipeline constructor.
    """

    def __init__(
        self,
        hf_name: str,
        **pipeline_params,
    ):
        self.__pipeline = pipeline(task="conversational", model=hf_name, **pipeline_params, use_fast=False)

        name = "hf:" + hf_name
        if len(pipeline_params) > 0:
            obj = {x: str(pipeline_params[x]) for x in pipeline_params}
            name += "@" + sha_digest(obj)[:6]

        super().__init__(name, self.__predict)
        print(f"HFModelPipeline {hf_name} placed on device {self.__pipeline.device}")

    def __predict(self, messages: list[Message]) -> str:
        out = self.__pipeline(messages)
        assert out[-1]["role"] == "assistant", out
        return out[-1]["content"]
