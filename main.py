import re
from typing import Optional, List, Tuple, Any, Dict, Type

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

from tools import wikipedia_tool, search_tool
import ui

# Load .env for local development
load_dotenv()

class Settings(BaseSettings):
    """Configuration settings for the research agent."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_default_model: str = "claude-3-5-sonnet-20240620"
    openai_default_model: str = "gpt-4o"
    timeout: int = 600

class ResearchResponse(BaseModel):
    """The structured research response from the agent."""
    topic: str = Field(description="The main topic of the research")
    summary: str = Field(description="A comprehensive summary of the findings")
    sources: List[str] = Field(description="List of sources used")
    tools_used: List[str] = Field(description="List of tools used by the agent")

class ModelFactory:
    """Factory to instantiate LLMs based on provider and model."""

    _PROVIDERS = {
        "anthropic": ChatAnthropic,
        "openai": ChatOpenAI,
    }

    @classmethod
    def get_llm(cls, settings: Settings, provider: str = "anthropic", model: Optional[str] = None):
        """Returns the desired LLM instance."""
        provider = provider.lower()
        llm_class = cls._PROVIDERS.get(provider)

        if not llm_class:
            supported = ", ".join([f"'{p}'" for p in cls._PROVIDERS.keys()])
            raise ValueError(
                f"Unsupported provider: '{provider}'. Supported providers: {supported}."
            )

        model_name_param = "model_name" if provider == "anthropic" else "model"
        kwargs = {
            model_name_param: model or (
                settings.anthropic_default_model if provider == "anthropic" 
                else settings.openai_default_model
            ),
            "timeout": settings.timeout
        }

        return llm_class(**kwargs)

class ResearchAgent:
    """Encapsulates the research agent creation and execution logic."""

    SYSTEM_PROMPT = (
        "You are a research assistant that will help generate a research paper. "
        "Answer the user query and use necessary tools. "
        "IMPORTANT: Your final response MUST be a valid JSON object. "
        "Escape any double quotes within string values (e.g., use \\\" instead of \"). "
        "Wrap the final output in <result> tags.\n{format_instructions}"
    )

    def __init__(self, llm):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=ResearchResponse)
        self.tools = [search_tool, wikipedia_tool]
        self.agent_executor = self._create_executor()

    def _create_executor(self) -> AgentExecutor:
        """Sets up the agent with tools and prompt."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ]).partial(format_instructions=self.parser.get_format_instructions())
        
        agent = create_tool_calling_agent(llm=self.llm, prompt=prompt, tools=self.tools)
        return AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=10
        )

    def run(self, query: str) -> Tuple[ResearchResponse, Dict[str, Any]]:
        """Main execution flow for a research query."""
        handler = ui.get_callback_handler()
        
        with ui.get_status("[bold blue]Agent is researching...[/bold blue]"):
            config: RunnableConfig = {
                "callbacks": [handler],
                "tags": ["research-agent"],
                "metadata": {"topic": query},
                "run_name": "ResearchAgent.run"
            }
            raw_response = self.agent_executor.invoke(
                {"input": query, "chat_history": []}, 
                config
            )
        
        text_to_parse = self._extract_text_to_parse(raw_response)
        try:
            structured_response = self.parser.parse(text_to_parse)
        except Exception as e:
            raise ValueError(f"Failed to parse structured response: {e}. Raw text: {text_to_parse}")
        
        return structured_response, raw_response

    @staticmethod
    def _extract_text_to_parse(raw_response: Dict[str, Any]) -> str:
        """Safely extracts and cleans text from the raw response."""
        output = raw_response.get("output", "")
        
        if isinstance(output, list) and output:
            first_item = output[0]
            text_to_parse = first_item.get("text", str(first_item)) if isinstance(first_item, dict) else str(first_item)
        else:
            text_to_parse = str(output)

        # Robust extraction of content between <result> tags
        match = re.search(r"<result>(.*?)(?:</result>|$)", text_to_parse, re.DOTALL)
        return match.group(1).strip() if match else text_to_parse

def run_research(query: str, provider: str = "anthropic"):
    """Entry point to execute the research workflow."""
    raw_response = None
    try:
        settings = Settings()
        llm = ModelFactory.get_llm(settings, provider=provider)
        
        agent = ResearchAgent(llm)
        structured_response, raw_response = agent.run(query)
        
        ui.display_agent_output(raw_response)
        ui.display_structured_response(structured_response)
    except Exception as e:
        ui.display_error(str(e), raw_response=raw_response)

if __name__ == "__main__":
    import sys
    # Default query
    DEFAULT_TOPIC = "Interesting facts about the Eiffel Tower"
    
    # Use command-line arguments if provided
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        # Prompt user for query
        user_query = ui.get_user_input("Enter your research topic", default_value=DEFAULT_TOPIC)
    
    run_research(user_query)
