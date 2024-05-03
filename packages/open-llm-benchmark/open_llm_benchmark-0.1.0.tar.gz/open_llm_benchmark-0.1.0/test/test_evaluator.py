import argparse
import os
import sys

from open_llm_benchmark.evaluator import CriteriaGrader, ReferenceGrader
from open_llm_benchmark.llm import LlamaCppLLM


def test_reference_grader():
    print("Test ReferenceGrader")
    evaluator = ReferenceGrader(llm)
    print(evaluator.evaluate(query="kky今年几岁", reference_answer="12岁", generated_answer="12岁"))


def test_criteria_grader():
    print("Test ReferenceGrader")
    evaluator = CriteriaGrader(llm)
    print(evaluator.evaluate(query="kky今年几岁", criteria="12岁", generated_answer="12岁"))


if __name__ == "__main__":
    llm = LlamaCppLLM("/data/hf/Meta-Llama-3-8B-Instruct.Q5_K_M.gguf")
    test_reference_grader()
    test_criteria_grader()
