import datetime
import json
import os
from copy import copy
from typing import Type, List, Callable, Union, Literal

from llama_cpp import Llama
from pydantic import BaseModel, Field

from .llm_settings import LlamaLLMGenerationSettings, LlamaLLMSettings
from .llm_agent import LlamaCppAgent, StreamingResponse
from .messages_formatter import MessagesFormatterType, MessagesFormatter
from .function_calling import LlamaCppFunctionTool
from .gbnf_grammar_generator.gbnf_grammar_from_pydantic_models import (
    create_dynamic_model_from_function,
    create_dynamic_models_from_dictionaries,
    add_run_method_to_dynamic_model,
)
from .providers.llama_cpp_endpoint_provider import (
    LlamaCppGenerationSettings,
    LlamaCppEndpointSettings,
)
from .providers.openai_endpoint_provider import (
    OpenAIGenerationSettings,
    OpenAIEndpointSettings,
)


class activate_message_mode(BaseModel):
    """
    Activates message mode.
    """

    def run(self, agent: "GroupChatAgent"):
        agent.without_grammar_mode = True
        agent.without_grammar_mode_function.append(agent.send_message_to_user)
        return True


class activate_write_text_file(BaseModel):
    """
    Activates write text file mode.
    """

    file_path: str = Field(..., description="The path to the file.")

    def run(self, agent: "GroupChatAgent"):
        agent.without_grammar_mode = True
        agent.without_grammar_mode_function.append(self.write_file)
        return True

    def write_file(self, content: str):
        """
        Write content to a file.

        Args:
            content (str): The content to write to the file.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return None


class read_text_file(BaseModel):
    """
    Reads the content of a file.
    """

    file_path: str = Field(..., description="The path to the file.")

    def run(self):
        return self.read_file()

    def read_file(self):
        """
        Reads the content of a file.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            return f"File not found."


class GroupChatAgentConfig(BaseModel):
    name: str = Field(..., alias="name")
    agent_role: str = Field(..., alias="agent_role")


class GroupChatAgent:
    """
    An agent that uses function calling to interact with its environment and the user.

    Args:
        llama_llm (Union[Llama, LlamaLLMSettings, LlamaCppEndpointSettings, OpenAIEndpointSettings]): An instance of Llama, LlamaLLMSettings, LlamaCppServerLLMSettings as LLM.
        llama_generation_settings (Union[LlamaLLMGenerationSettings, LlamaCppGenerationSettings, OpenAIGenerationSettings]): Generation settings for Llama.
        messages_formatter_type (MessagesFormatterType): Type of messages formatter.
        custom_messages_formatter (MessagesFormatter): Custom messages formatter.
        streaming_callback (Callable[[StreamingResponse], None]): Callback function for streaming responses.
        k_last_messages_from_chat_history (int): Number of last messages to consider from chat history.
        system_prompt (str): System prompt for interaction.
        open_ai_functions (Tuple[List[dict], List[Callable]]): OpenAI function definitions and a list of the actual functions as tuple.
        python_functions (List[Callable]): Python functions for interaction.
        pydantic_functions (List[Type[BaseModel]]): Pydantic models representing functions.
        add_send_message_to_user_function (bool): Flag to add send_message_to_user function.
        send_message_to_user_callback (Callable[[str], None]): Callback for sending a message to the user.
        debug_output (bool): Enable debug output.

    Attributes:
        pydantic_functions (List[Type[BaseModel]]): List of Pydantic models representing functions.
        send_message_to_user_callback (Callable[[str], None]): Callback for sending a message to the user.
        llama_cpp_tools (List[LlamaCppFunctionTool]): List of LlamaCppFunctionTool instances.
        tool_registry (LlamaCppFunctionToolRegistry): Function tool registry.
        llama_generation_settings (LlamaLLMGenerationSettings): Generation settings for Llama.
        system_prompt (str): System prompt for interaction.
        llama_cpp_agent (LlamaCppAgent): LlamaCppAgent instance for interaction.
        k_last_messages_from_chat_history (int): Number of last messages to consider from chat history.
        streaming_callback (Callable[[StreamingResponse], None]): Callback function for streaming responses.

    Methods:
        save(file_path: str): Save the agent's state to a file.
        load_from_file(file_path: str, llama_llm, python_functions, pydantic_functions, send_message_to_user_callback, streaming_callback) -> FunctionCallingAgent:
            Load the agent's state from a file.
        load_from_dict(agent_dict: dict) -> FunctionCallingAgent: Load the agent's state from a dictionary.
        as_dict() -> dict: Convert the agent's state to a dictionary.
        generate_response(message: str): Generate a response based on the input message.
        send_message_to_user(message: str): Send a message to the user.

    """

    def __init__(
        self,
        llama_llm: Union[
            Llama, LlamaLLMSettings, LlamaCppEndpointSettings, OpenAIEndpointSettings
        ],
        group_agents: List[GroupChatAgentConfig],
        llama_generation_settings: Union[
            LlamaLLMGenerationSettings,
            LlamaCppGenerationSettings,
            OpenAIGenerationSettings,
        ] = None,
        messages_formatter_type: MessagesFormatterType = MessagesFormatterType.CHATML,
        custom_messages_formatter: MessagesFormatter = None,
        streaming_callback: Callable[[StreamingResponse], None] = None,
        k_last_messages_from_chat_history: int = 0,
        system_prompt: str = None,
        open_ai_functions: (List[dict], List[Callable]) = None,
        python_functions: List[Callable] = None,
        pydantic_functions: List[Type[BaseModel]] = None,
        basic_file_tools: bool = False,
        allow_parallel_function_calling=False,
        add_send_message_to_user_function: bool = True,
        send_message_to_user_callback: Callable[[str], None] = None,
        debug_output: bool = False,
    ):
        """
        Initialize the FunctionCallingAgent.

        Args:
            llama_llm (Union[Llama, LlamaLLMSettings, OpenAIEndpointSettings]): An instance of Llama, LlamaLLMSettings or LlamaCppServerLLMSettings as LLM.
            llama_generation_settings (Union[LlamaLLMGenerationSettings, LlamaCppGenerationSettings, OpenAIGenerationSettings]): Generation settings for Llama.
            messages_formatter_type (MessagesFormatterType): Type of messages formatter.
            custom_messages_formatter (MessagesFormatter): Optional Custom messages formatter.
            streaming_callback (Callable[[StreamingResponse], None]): Callback function for streaming responses.
            k_last_messages_from_chat_history (int): Number of last messages to consider from chat history.
            system_prompt (str): System prompt for interaction.
            open_ai_functions (Tuple[List[dict], List[Callable]]): OpenAI function definitions and a list of the actual functions as tuple.
            python_functions (List[Callable]): Python functions for interaction.
            pydantic_functions (List[Type[BaseModel]]): Pydantic models representing functions.
            allow_parallel_function_calling (bool): Allow parallel function calling (Default=False)
            add_send_message_to_user_function (bool): Flag to add send_message_to_user function.
            send_message_to_user_callback (Callable[[str], None]): Callback for sending a message to the user.
            debug_output (bool): Enable debug output.
        """
        if pydantic_functions is None:
            self.pydantic_functions = []
        else:
            self.pydantic_functions = pydantic_functions

        if python_functions is not None:
            for tool in python_functions:
                self.pydantic_functions.append(create_dynamic_model_from_function(tool))

        if open_ai_functions is not None:
            open_ai_models = create_dynamic_models_from_dictionaries(
                open_ai_functions[0]
            )
            count = 0
            for func in open_ai_functions[1]:
                model = open_ai_models[count]
                self.pydantic_functions.append(
                    add_run_method_to_dynamic_model(model, func)
                )
                count += 1

        self.send_message_to_user_callback = send_message_to_user_callback
        if add_send_message_to_user_function:
            self.llama_cpp_tools = [
                LlamaCppFunctionTool(activate_message_mode, agent=self)
            ]
        else:
            self.llama_cpp_tools = []
        if basic_file_tools:
            self.llama_cpp_tools.append(LlamaCppFunctionTool(read_text_file))
            self.llama_cpp_tools.append(
                LlamaCppFunctionTool(activate_write_text_file, agent=self)
            )
        for tool in self.pydantic_functions:
            self.llama_cpp_tools.append(LlamaCppFunctionTool(tool))

        self.tool_registry = LlamaCppAgent.get_function_tool_registry(
            self.llama_cpp_tools,
            add_inner_thoughts=True,
            allow_parallel_function_calling=allow_parallel_function_calling,
        )
        print(self.tool_registry.gbnf_grammar)
        if llama_generation_settings is None:
            if isinstance(llama_llm, Llama) or isinstance(llama_llm, LlamaLLMSettings):
                llama_generation_settings = LlamaLLMGenerationSettings()
            else:
                llama_generation_settings = LlamaCppGenerationSettings()

        if isinstance(
            llama_generation_settings, LlamaLLMGenerationSettings
        ) and isinstance(llama_llm, LlamaCppEndpointSettings):
            raise Exception(
                "Wrong generation settings for llama.cpp server endpoint, use LlamaCppServerGenerationSettings under llama_cpp_agent.providers.llama_cpp_server_provider!"
            )
        if (
            isinstance(llama_llm, Llama)
            or isinstance(llama_llm, LlamaLLMSettings)
            and isinstance(llama_generation_settings, LlamaCppGenerationSettings)
        ):
            raise Exception(
                "Wrong generation settings for llama-cpp-python, use LlamaLLMGenerationSettings under llama_cpp_agent.llm_settings!"
            )

        if isinstance(llama_llm, OpenAIEndpointSettings) and not isinstance(
            llama_generation_settings, OpenAIGenerationSettings
        ):
            raise Exception(
                "Wrong generation settings for OpenAI endpoint, use CompletionRequestSettings under llama_cpp_agent.providers.openai_endpoint_provider!"
            )

        self.llama_generation_settings = llama_generation_settings

        self.without_grammar_mode = False
        self.without_grammar_mode_function = []
        self.prompt_suffix = ""
        self.group_agents = group_agents
        if system_prompt is not None:
            self.system_prompt = system_prompt
        else:
            # You can also request to return control back to you after a function call is executed by setting the 'return_control' flag in a function call object.
            self.system_prompt = (
                """You are Funky, an AI assistant that calls functions to perform tasks. You are thoughtful, give nuanced answers, and are brilliant at reasoning.
    
    To call functions, you respond with a JSON object containing three fields:
    "thoughts "and reasoning": Your thoughts and reasoning behind the function call.
    "function": The name of the function you want to call.
    "parameters": The arguments required for the function.
    
    After performing a function call, you will receive a response containing the return values of the function calls.
    
    For direct communication with the user, employ the 'activate_message_mode' function. After you have finished your call to 'activate_message_mode', you can freely write a response to the user without any JSON constraints. This enables you to converse naturally. Ensure to end your message with '(End of message)' to signify its conclusion.
    
    ### Functions:
    Below is a list of functions you can use to interact with the system. Each function has specific parameters and requirements. Make sure to follow the instructions for each function carefully.
    Choose the appropriate function based on the task you want to perform. Provide your function calls in JSON format.
    
    """
                + self.tool_registry.get_documentation().strip()
            )
        self.llama_cpp_agent = LlamaCppAgent(
            llama_llm,
            debug_output=debug_output,
            system_prompt="",
            predefined_messages_formatter_type=messages_formatter_type,
            custom_messages_formatter=custom_messages_formatter,
        )

        self.k_last_messages_from_chat_history = k_last_messages_from_chat_history
        self.streaming_callback = streaming_callback

    def as_dict(self) -> dict:
        """
        Convert the agent's state to a dictionary.

        Returns:
           dict: The dictionary representation of the agent's state.
        """
        return self.__dict__

    def generate_response(
        self,
        initial_message: str,
        number_of_turns: int = 4,
        additional_stop_sequences: List[str] = None,
    ):
        responses = [
            {
                "role": "user",
                "content": initial_message,
            }
        ]
        for _ in range(number_of_turns):
            for a in self.group_agents:
                self.llama_cpp_agent.messages = copy(responses)
                for response in self.llama_cpp_agent.messages:
                    if response["content"].strip().startswith(a.name):
                        response["role"] = "assistant"
                self.prompt_suffix = f"\n{a.name}:"
                result = self.intern_get_response(
                    system_message=f"""You are {a.name}, a {a.agent_role}, collaborating with other experts. You use tools to communicate with other agents and to write files.\n\nAvailable function tools:\n{self.tool_registry.get_documentation()}""",
                    additional_stop_sequences=additional_stop_sequences,
                )
                while True:
                    if isinstance(result, str):
                        if len(self.without_grammar_mode_function) > 0:
                            func_list = []
                            for func in self.without_grammar_mode_function:
                                if func.__name__ not in func_list:
                                    func(result.strip())
                                    func_list.append(func.__name__)
                        break
                    function_message = f""""""
                    count = 0
                    if result is not None:
                        for res in result:
                            count += 1
                            if not isinstance(res, str):
                                function_message += f"""Function: "{res["function"]}"\nReturn Value: {res["return_value"]}\n"""
                            else:
                                function_message += f"" + res + "\n\n"
                        responses.append(
                            {
                                "role": "user",
                                "content": self.llama_cpp_agent.last_response.strip(),
                            }
                        )
                        responses.append(
                            {
                                "role": "function",
                                "content": function_message.strip(),
                            }
                        )

                        self.llama_cpp_agent.add_message(
                            role="function", message=function_message.strip()
                        )
                    result = self.intern_get_response(
                        system_message=f"""You are {a.name}, a {a.agent_role}, collaborating with other experts. You use tools to communicate with other agents and to write files.\n\nAvailable function tools:\n{self.tool_registry.get_documentation()}""",
                        additional_stop_sequences=additional_stop_sequences,
                    )
                response = f"{a.name}:{result}"
                responses.append(
                    {
                        "role": "user",
                        "content": response,
                    }
                )

    def intern_get_response(
        self, system_message, additional_stop_sequences: List[str] = None
    ):
        without_grammar_mode = False
        if self.without_grammar_mode:
            without_grammar_mode = True
            self.without_grammar_mode = False
        if additional_stop_sequences is None:
            additional_stop_sequences = []
        additional_stop_sequences.append("(End of message)")
        result = self.llama_cpp_agent.get_chat_response(
            system_prompt=system_message,
            streaming_callback=self.streaming_callback,
            function_tool_registry=self.tool_registry
            if not without_grammar_mode
            else None,
            prompt_suffix=self.prompt_suffix,
            additional_stop_sequences=additional_stop_sequences,
            **self.llama_generation_settings.as_dict(),
        )
        if without_grammar_mode:
            self.prompt_suffix = ""
        return result

    def send_message_to_user(self, message: str):
        """
        Send a message to the user.

        Args:
            message: The message send to the user.
        """
        if self.send_message_to_user_callback:
            self.send_message_to_user_callback(message)
        else:
            print(message)
