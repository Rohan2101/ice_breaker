from langchain.chains.summarize.refine_prompts import prompt_template
from langchain_groq import ChatGroq
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from dotenv import load_dotenv
from numpy.f2py.crackfortran import verbose

from tools.tools import get_profile_url_tavily
load_dotenv()
def lookup(name:str) -> str:
    llm = ChatGroq(
        temperature=0,
        groq_api_key="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",
        model_name="llama-3.1-70b-versatile"
    )

    template = """
       given the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username
       In Your Final answer only the person's username
       which is extracted from: https://x.com/USERNAME"""

    prompt_template = PromptTemplate(input_variables=["name_of_person"],template=template)

    tools_for_agent_twitter = [
        Tool(
        name="Crawl Google 4 twitter profile page",
        func = get_profile_url_tavily,
        description="useful for when you need get the Twitter Page URL",
        ),
    ]

    react_promt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm,tools=tools_for_agent_twitter,prompt=react_promt
    )
    agent_executor = AgentExecutor(
        agent=agent,tools= tools_for_agent_twitter,verbose=True
    )
    result= agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    twitter_usename=result["output"]
    print(twitter_usename)
    return twitter_usename

if __name__=="__main__":
    lookup("Eden Marco")