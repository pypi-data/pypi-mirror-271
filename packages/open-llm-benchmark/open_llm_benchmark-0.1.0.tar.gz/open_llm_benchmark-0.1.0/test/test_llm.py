import argparse
import os
import sys

sys.path.append("/home/kky/project/Open-LLM-Benchmark")
from open_llm_benchmark.llm import VLLM, LlamaCppLLM, HuggingFaceLLM, OpenAILLM


messages = [{"role": "system", "content": "Play the role of a mad scientist named KKY, always response with 中文"}, {"role": "user", "content": "你是谁..."}]


def test_vllm():
    model = VLLM("/data/hf/Meta-Llama-3-8B-Instruct")
    print(model.model_name,"@", model.model_loader)
    print(model.generate(messages))
    encoded = model.encode("\n")
    print(encoded)
    print(model.decode(encoded))


def test_hf():
    model = HuggingFaceLLM("/data/hf/Meta-Llama-3-8B-Instruct")
    print(model.model_name,"@", model.model_loader)
    print(model.generate(messages))
    encoded = model.encode("\n")
    print(encoded)
    print(model.decode(encoded))


def test_llamacpp():
    model = LlamaCppLLM("/data/hf/Meta-Llama-3-8B-Instruct.Q5_K_M.gguf")
    print(model.model_name,"@", model.model_loader)
    print(model.generate(messages))
    encoded = model.encode("\n")
    print(encoded)
    print(model.decode(encoded))


def test_openai():
    model = OpenAILLM("gpt-3.5-turbo")
    print(model.model_name,"@", model.model_loader)
    print(model.generate(messages))
    encoded = model.encode("\n")
    print(encoded)
    print(model.decode(encoded))


if __name__ == "__main__":
    # test_hf()
    # test_llamacpp()
    # test_vllm()
    test_openai()
