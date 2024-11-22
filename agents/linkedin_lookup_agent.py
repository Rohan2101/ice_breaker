import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
from tools.tools import get_profile_url_tavily
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub


def lookup(name: str) -> str:

    llm = ChatGroq(
        temperature=0,
        groq_api_key="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",
        model_name="llama-3.1-70b-versatile",
    )
    template = """given the full name {name_of_person} I want you to get me a link to their linkedin profile page. Your answer should contain only the URL"""
    prompt_template = PromptTemplate(
        template=template,input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get linkedin page url",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent,tools=tools_for_agent,verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url

if __name__=="__main__":
    linkedin_url = lookup(name="Eden Marco Udemy")
    print(linkedin_url)