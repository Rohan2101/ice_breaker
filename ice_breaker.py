from dotenv import load_dotenv
import os
from typing import Tuple
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parsers import summary_parser

from third_party.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_party.twitter import scrape_user_tweets


def ice_break_with(name: str) -> Tuple[str, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username)
    summary_template = """
    given the information about a person from linkedin {information} and their latest twitter posts {twitter_posts} I want you to create:
    1. A short summary
    2. two interesting facts about them
    Use information from both twitter and linkedin
    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information","twitter_posts"], template=summary_template,
        partial_variables={"format_instructions":summary_parser.get_format_instructions()}
    )

    # llm = ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo")

    llm = ChatGroq(
        temperature=0,
        groq_api_key="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",
        model_name="llama-3.1-70b-versatile",
    )

    chain = summary_prompt_template | llm | summary_parser
    res:summary = chain.invoke(input={"information": linkedin_data,"twitter_posts": tweets})
    return res, linkedin_data.get("profile_pic_url")
if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_break_with(name="Eden Marco Udemy")




