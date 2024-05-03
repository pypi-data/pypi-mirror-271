import sys
from typing import Union

sys.path.append("/home/kky/project/Open-LLM-Benchmark")
from open_llm_benchmark.llm import VLLM
from open_llm_benchmark.agent.react_agent import ReActAgent

if __name__ == "__main__":

    def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Multiple two numbers and returns the result"""
        return a * b


    def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Add two numbers and returns the result"""
        return a + b


    def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Subtract two numbers and returns the result"""
        return a - b


    def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Divides two numbers and returns the result"""
        return a / b

    def query_weather(city: str, date: str) -> str:
        # Query the weather for a specified date (YYYY-MM-DD format) and city.
        if city == "New York" or city == "NewYork":
            return f"The weather in New York on {date} is cloudy with a temperature of 23 degrees."
        elif city == "Bei Jing" or city == "BeiJing":
            return f"The weather in Bei Jing on {date} is rainy with a temperature of 21 degrees."
        else:
            return f"The weather in {city} on {date} is sunny with a temperature of 20 degrees."


    query_and_answer = [
        ("What is 188+133", "321"),
        ("What is 188 * 13", "2444"),
        ("What is (121 + 2) * 5 * (100-2)?", "60270"),
        ("What is (44 + 2) * 5 * (13-2)?", "2530"),
        ("What is (23 + 2) * (10-3)?", "175"),
        ("What is ((23 + 2) * (10-3)) * 3?", "525"),
        ("What is the weather like in New York on April 2nd, 2023?", "The weather in New York on 2023-04-02 is cloudy with a temperature of 23 degrees."),
        ("What is the weather like in Bei Jing on April 2nd, 2023?", "The weather in Bei Jing on 2023-04-02 is cloudy with a temperature of 21 degrees."),
        ("Today is May 2nd, 2024, how many degrees lower is the temperature in Paris compared to New York?", "The temperature in Paris is 3 degrees lower than in New York."),
        ("Today is April 2nd, 2023, how many degrees higher is the temperature in New York compared to Bei Jing?", "The temperature in New York is 2 degrees higher than in Bei Jing."),
    ]


    tools = [multiply, add, subtract, divide, query_weather]

    from open_llm_benchmark.llm import VLLM, LlamaCppLLM, OpenAILLM
    # llm = VLLM("/data/hf/Meta-Llama-3-8B-Instruct")
    # llm = LlamaCppLLM("/data/hf/Meta-Llama-3-8B-Instruct.Q5_K_M.gguf")
    llm = OpenAILLM("gpt-4-turbo")

    print("Test ReAct Agent")
    agent = ReActAgent(llm, tools)
    agent.run(query_and_answer[0][0], verbose=True)
