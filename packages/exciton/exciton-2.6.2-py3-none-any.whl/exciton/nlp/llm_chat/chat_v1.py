import json
import os
from typing import Any, Dict, List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class Llm_Chat_Model(object):
    """AI is creating summary for __init__

    Args:
        path_to_model (str, optional): path to the model. Defaults to None.
    """

    def __init__(
        self,
        path_to_model: str = None,
        system_prompt: str = "You are a pirate chatbot who always responds in pirate speak!",
    ) -> None:
        self.path_to_model = path_to_model
        self.train_modules = {}
        self.base_modules = {}
        self.batch_data = {}
        self.system_prompt = {"role": "system", "content": system_prompt}

        if self.path_to_model is None:
            HOME = os.path.expanduser("~")
            MODEL_DIR = "exciton/models/nlp/llm_chat"
            model = "exciton_v1_meta_llama_3_8b_instruct"
            path_to_model = f"{HOME}/{MODEL_DIR}/{model}"
            self.path_to_model = path_to_model
        assert "exciton_v1" in self.path_to_model
        self.tokenizer = AutoTokenizer.from_pretrained(f"{path_to_model}/tokenizer")
        self.model = AutoModelForCausalLM.from_pretrained(
            f"{path_to_model}/models",
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

    def predict(
        self,
        messages: List[Dict[str, str]] = [],
        max_new_tokens: int = 1028,
        do_sample: bool = False,
        temperature: float = 0.6,
        top_p: float = 0.9,
        device: str = "cuda",
    ) -> Dict[str, Any]:
        """predict result.

        Args:
            messages (List[Dict[str, str]]): messages.
            max_new_tokens (int, optional): max number of new tokens. Defaults to 1028.
            do_sample (bool, optional): do sampling. Defaults to False.
            temperature (float, optional): temperature. Defaults to 0.6.
            top_p (float, optional): top_p. Defaults to 0.9.
            device (str, optional): [description]. Defaults to "cuda".

        Returns:
            Dict[str, Any]: result of llm_chat.
        """
        if len(messages) == 0:
            exout = {"role": "assistant", "content": "How can I help you?"}
            return exout
        if not isinstance(messages, List):
            if not isinstance(messages, Dict):
                messages = [{"role": "user", "content": json.dumps(messages)}]
            else:
                if "role" in messages:
                    messages = [messages]
                else:
                    messages = [{"role": "user", "content": json.dumps(messages)}]
        if not messages[0]["role"] == "system":
            if self.system_prompt["content"]:
                messages = [self.system_prompt] + messages
        input_ids = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        ).to(device)
        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]
        outputs = self.model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            eos_token_id=terminators,
            do_sample=do_sample,
            temperature=temperature,
            top_p=top_p,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        response = outputs[0][input_ids.shape[-1] :]
        out = self.tokenizer.decode(response, skip_special_tokens=True)
        out = out.strip()
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        exout = {"role": "assistant", "content": out}
        return exout
