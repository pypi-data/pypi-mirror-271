from __future__ import annotations


from pathlib import Path
from typing import Dict, List, Optional

from langchain.chat_models.base import BaseChatModel
from langchain.llms.base import BaseLLM
from numpy import add

from ..tool import AssistantProject
from ..assistant import AssistantProject, RevaTool, BaseLLM, register_tool
from ..assistant_api_server import get_channel

from ..reva_exceptions import RevaToolException

import logging

# TODO: I think the word tool is used too much in the project... It's a bit confusing...
class RevaRemoteTool(RevaTool):
    @property
    def channel(self):
        return get_channel()


@register_tool
class RevaDecompilationIndex(RevaRemoteTool):
    """
    An index of decompiled functions available to the
    reverse engineering assistant.
    """
    index_name = "decompilation"
    description = "Used for retrieving decompiled functions"
    logger = logging.getLogger("reverse_engineering_assistant.RevaDecompilationIndex")

    def __init__(self, project: AssistantProject, llm: BaseLLM) -> None:
        super().__init__(project, llm)
        self.description = "Used for retrieveing decompiled functions"
        self.tool_functions = [
            self.get_decompilation_for_function,
            # TODO: Implement these functions
            #self.get_defined_function_list_paginated,
            #self.get_defined_function_count,
        ]

    def get_decompilation_for_function(self, function_name_or_address: str | int) -> Dict[str, str]:
        """
        Return the decompilation for the given function. The function can be specified by name or address.
        Hint: It is too slow to decompile _all_ functions, so use get_defined_function_list_paginated to get a list of functions
        and be sure to specify the function name or address exactly.
        """

        # First normalise the argument
        address: Optional[int] = None
        name: Optional[str] = None
        if isinstance(function_name_or_address, int):
                address = function_name_or_address
        elif isinstance(function_name_or_address, str):
            name = function_name_or_address

        if address is None and name is None:
            raise RevaToolException("function_name_or_address must be an address or function name")

        if address and address <= 0:
            raise RevaToolException("function_name_or_address must be a positive integer or a function name")

        # Now we can create the message and call over the RPC
        from ..protocol import RevaGetDecompilation_pb2_grpc, RevaGetDecompilation_pb2
        stub = RevaGetDecompilation_pb2_grpc.RevaDecompilationServiceStub(self.channel)

        request = RevaGetDecompilation_pb2.RevaGetDecompilationRequest()

        if name:
            request.function = name
        if address:
            request.address = address

        response: RevaGetDecompilation_pb2.RevaGetDecompilationResponse = stub.GetDecompilation(request)

        # Finally we can return the response
        return {
            "function": response.function,
            "function_signature": response.function_signature,
            "address": hex(response.address),
            "decompilation": response.decompilation,
            "listing": response.listing,
            "variables": response.variables, #type: ignore # We can ignore this because it can be serialised to a dict
            "incoming_calls": response.incoming_calls,
            "outgoing_calls": response.outgoing_calls,
        }


    def get_defined_function_list_paginated(self, page: int, page_size: int = 20) -> List[str]:
        """
        Return a paginated list of functions in the index. Use get_defined_function_count to get the total number of functions.
        page is 1 indexed. To get the first page, set page to 1. Do not set page to 0.
        """
        raise NotImplementedError("This function is not implemented yet")
        return response.function_list

    def get_defined_function_count(self) -> int:
        """
        Return the total number of defined functions in the program.
        """

        raise NotImplementedError("This function is not implemented yet")
        return response.function_count

# TODO: This tool is not implemented yet
#@register_tool
class RevaRenameFunctionVariable(RevaRemoteTool):
    """
    A tool for renaming variables used in functions
    """

    description = "Used for renaming variables used in functions"
    logger = logging.getLogger("reverse_engineering_assistant.RevaRenameFunctionVariable")

    def __init__(self, project: AssistantProject, llm: BaseLLM | BaseChatModel) -> None:
        super().__init__(project, llm)
        self.description = "Used for renaming variables used in functions"
        self.tool_functions = [
            self.rename_multiple_variables_in_function,
            self.rename_variable_in_function
        ]

    def rename_multiple_variables_in_function(self, new_names: Dict[str, str], containing_function: str) -> List[str]:
        """
        Change the names of multiple variables in the function `containing_function` to the new names specified in `new_names`.
        `new_names` is a dictionary where the keys are the old names and the values are the new names.

        If there are many variables to rename in a function, use this. It is more efficient than calling rename_variable_in_function multiple times.
        After calling this, you can confirm the changes by decompiling the function again.
        If there is a failure, retrying the operation will not help.
        """
        outputs: List[str] = []
        for old_name, new_name in new_names.items():
            outputs.append(self.rename_variable_in_function(new_name, old_name, containing_function))
        return outputs

    def rename_variable_in_function(self, new_name: str, old_name: str, containing_function: str):
        """
        Change the name of the variable with the name `old_name` in `containing_function` to `new_name`.
        If the thing you want to rename is not in a function, you should use rename symbol instead,
        """
        raise NotImplementedError("This function is not implemented yet")
        return f"Renamed {old_name} to {new_name} in {containing_function}"

#TODO: This tool is not implemented yet
#@register_tool
class RevaCrossReferenceTool(RevaRemoteTool):
    """
    An tool to retrieve cross references, to and from, addresses.
    """
    index_directory: Path
    def __init__(self, project: AssistantProject, llm: BaseLLM) -> None:
        super().__init__(project, llm)
        self.description = "Used for retrieving cross references to and from addresses"

        self.tool_functions = [
            self.get_references,
        ]

    def get_references(self, address_or_symbol: str) -> Optional[Dict[str, List[str]]]:
        """
        Return a list of references to and from the given address or symbol.
        These might be calls from/to other functions, or data references from/to this address.
        """
        from ..protocol import RevaGetReferences_pb2_grpc, RevaGetReferences_pb2

        stub = RevaGetReferences_pb2_grpc.RevaGetReferencesServiceStub(self.channel)

        request = RevaGetReferences_pb2.RevaGetReferencesRequest()
        request.address_or_symbol = address_or_symbol

        response: RevaGetReferences_pb2.RevaGetReferencesResponse = stub.GetReferences(request)

        return {
            "references_to": response.references_to,
            "references_from": response.references_from,
        }

@register_tool
class RevaGetSymbols(RevaRemoteTool):
    """
    A tool for listing symbols in a program.
    These could be functions, global variables, or other named entities.
    """
    logger = logging.getLogger("reverse_engineering_assistant.RevaGetSymbols")


    def __init__(self, project: AssistantProject, llm: BaseLLM) -> None:
        super().__init__(project, llm)
        self.description = "Used for retrieving symbols in the program"

        self.tool_functions = [
            self.get_symbol_count,
            self.get_symbols,
            self.get_symbol,
            self.get_function_count,
            self.get_functions,
        ]

    def _get_symbol_list(self) -> List[str]:
        from ..protocol import RevaGetSymbols_pb2_grpc, RevaGetSymbols_pb2
        stub = RevaGetSymbols_pb2_grpc.RevaToolSymbolServiceStub(self.channel)

        request = RevaGetSymbols_pb2.RevaGetSymbolsRequest()

        response: RevaGetSymbols_pb2.RevaGetSymbolsResponse = stub.GetSymbols(request)

        return response.symbols

    def _get_function_list(self) -> List[str]:
        function_list: List[str] = []
        for symbol_name in self._get_symbol_list():
            symbol = self.get_symbol(symbol_name)
            if symbol["type"] == "FUNCTION":
                function_list.append(symbol_name)
        return function_list

    def get_function_count(self) -> int:
        """
        Return the total number of functions in the program.
        Useful before calling get_functions.
        """
        return len(self._get_function_list())

    def get_functions(self, page: int = 0, page_size: int = 20) -> List[Dict[str, str]]:
        """
        Return a list of functions in the program.
        Please check the total number of functions with get_function_count before calling this.
        The page is 0 indexed. To get the first page, set page to 0.
        Pick a page_size that is reasonable for your context size.
        """
        if page < 0:
            raise RevaToolException("page must be 0 or a positive integer")
        if page_size <= 0:
            raise RevaToolException("page_size must be a positive integer")

        function_list = self._get_function_list()
        start = (page - 1) * page_size
        end = page * page_size

        function_details: List[Dict[str, str]] = []
        for function in function_list[start:end]:
            # TODO: Replace with get_function
            function_details.append(self.get_symbol(function))
        return function_details

    def get_symbol_count(self) -> int:
        """
        Return the total number of symbols in the program.
        Useful before calling get_symbols.
        """
        return len(self._get_symbol_list())

    def get_symbols(self, page: int = 0, page_size: int = 20) -> List[Dict[str, str]]:
        """
        Return a list of symbols in the program.
        Please check the total number of symbols with get_symbol_count before calling this.
        The page is 0 indexed. To get the first page, set page to 0.
        Pick a page_size that is reasonable for your context size.
        """
        if page < 0:
            raise RevaToolException("page must be 0 or a positive integer")
        if page_size <= 0:
            raise RevaToolException("page_size must be a positive integer")

        symbol_list = self._get_symbol_list()
        start = (page - 1) * page_size
        end = page * page_size

        symbol_details: List[Dict[str, str]] = []
        for symbol in symbol_list[start:end]:
            symbol_details.append(self.get_symbol(symbol))
        return symbol_details

    def get_symbol(self, address_or_name: str) -> Dict[str, str]:
        """
        Return information about the symbol at the given address or with the given name.
        Returns a dictionary with the keys "name", "address", and "type".
        """
        from ..protocol import RevaGetSymbols_pb2_grpc, RevaGetSymbols_pb2
        stub = RevaGetSymbols_pb2_grpc.RevaToolSymbolServiceStub(self.channel)

        request = RevaGetSymbols_pb2.RevaSymbolRequest()
        request.address_or_name = address_or_name
        self.logger.debug(f"Getting symbol {address_or_name} request: {request}")
        response: RevaGetSymbols_pb2.RevaSymbolResponse = stub.GetSymbol(request)
        self.logger.debug(f"Got symbol {address_or_name} response: {response}")
        return {
            "name": response.name,
            "address": response.address,
            "type": RevaGetSymbols_pb2.SymbolType.Name(response.type),
        }


@register_tool
class RevaSetSymbolName(RevaRemoteTool):
    """
    A tool for creating or changing the name for a global symbol.
    This could be a function name, or a global variable name.
    """

    def __init__(self, project: AssistantProject, llm: BaseLLM) -> None:
        super().__init__(project, llm)
        self.description = "Used for retrieving cross references to and from addresses"

        self.tool_functions = [
            self.set_symbol_name,
        ]

    def set_symbol_name(self, new_name: str, old_name_or_address: str) -> Dict[str, str]:
        """
        Set the name of the symbol at the given address to `new_name`. If an old name is
        provided, rename the symbol to `new_name`.
        """
        from ..protocol import RevaGetSymbols_pb2_grpc, RevaGetSymbols_pb2
        stub = RevaGetSymbols_pb2_grpc.RevaToolSymbolServiceStub(self.channel)

        request = RevaGetSymbols_pb2.RevaSetSymbolNameRequest()
        request.new_name = new_name
        request.old_name_or_address = old_name_or_address

        response: RevaGetSymbols_pb2.RevaSetSymbolNameResponse = stub.SetSymbolName(request)

        return {
            "old_name": old_name_or_address,
            "new_name": new_name,
        }

@register_tool
class RevaSetComment(RevaRemoteTool):
    """
    A tool for setting comments on addresses, functions and symbols.
    """

    def __init__(self, project: AssistantProject, llm: BaseLLM) -> None:
        super().__init__(project, llm)
        self.description = "Used for setting comments on addresses, functions and symbols"

        self.tool_functions = [
            self.set_comment,
        ]

    def set_comment(self, comment: str, address_or_symbol: str) -> Dict[str, str]:
        """
        Set the comment at the given address, function or symbol to `comment`.
        Use this when you want to add an explanation or note to a specific part
        of the code.
        """
        raise NotImplementedError("This function is not implemented yet")
        return response.model_dump()