import json
import re
from dataclasses import dataclass, field
from pprint import pprint

from llama_index import ServiceContext, SQLDatabase
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine
from pi_conf import AttrDict
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    select,
    text,
)

from chatbot import DATA_DIR, cfg
from chat.layers.llm.assistant.assistant_schema import (
    people_columns,
    people_columns_2_idx,
    technologies,
)
from chat.layers.llm.assistant.assistant_tools import (
    break_into_steps,
    default_email_examples,
)
from chat.layers.llm.chatbot import LLM
import logging
log = logging.getLogger(__name__)
connection_string = f"sqlite:///{DATA_DIR}/enhanced_enrichment.db"



class AssistantConfig(AttrDict):
    system_message: dict[str, str] = None


def generate_openai_prompt(
    from_person: dict,
    to_person: dict,
    from_company: dict,
    to_company: dict,
    from_technologies: list[str] = None,
    to_technologies: list[str] = None,
    use_examples: bool = True,
    examples: list[str] = None,
) -> str:
    """
    Generate an OpenAI prompt for a cold email from a person at a company to a person at another company.

    Args:
        from_person (dict): A dictionary containing information about the sender of the email.
        to_person (dict): A dictionary containing information about the recipient of the email.
        from_company (dict): A dictionary containing information about the sender's company.
        to_company (dict): A dictionary containing information about the recipient's company.
        from_technologies (list[str], optional): A list of technologies used by the sender's company. Defaults to None.
        to_technologies (list[str], optional): A list of technologies used by the recipient's company. Defaults to None.

    Returns:
        str: The OpenAI prompt.
    """
    f = from_person
    t = to_person
    fc = from_company
    tc = to_company

    prompt = (
        f"Write a professional and engaging email from {f['first_name']} {f['last_name']}, {f['job_title']}, in 1 paragraph or less, "
        f"of {fc['name']}, to {t['first_name']} {t['last_name']}, {t['job_title']} of {tc['name']}. "
        f"Keep it simple without flowery language. "
    )
    if from_technologies:
        prompt += (
            f"The email should introduce {fc['name']}, which specializes in {from_technologies} "
        )
        # f"and briefly summarize its strengths and achievements ({qrev_summary}). "
    prompt += f"The email aims to propose a collaboration between {fc['name']} and {tc['name']}, "
    if to_technologies:
        prompt += f"emphasizing how {fc['name']}'s technologies can add value to {tc['name']}'s work in {to_technologies}. "
        # f"Include a personal touch based on {from_person_summary} and suggest a meeting or call for further discussion. "

    prompt += f"End the email with contact details.\n"
    prompt += f"Return the result as a json object with the following fields: [email_subject, email_body]\n"

    if f.get("linkedin_url"):
        prompt += f"including LinkedIn ({f['linkedin_url']}), "
    if f.get("twitter_url"):
        prompt += f"Twitter ({f['twitter_url']}), "
    if f.get("work_email"):
        prompt += f"and email ({f['work_email']})."
    if use_examples:
        if examples is None:
            examples = default_email_examples
        prompt += "\nExamples of emails that have worked in the past: "
        for i, ex in enumerate(examples):
            prompt += f"Example {i+1}: {ex} \n"
    return prompt


@dataclass
class Assistant:
    thread_id: str = None
    user_id: str = None
    company_id: str = None

    def _refine_step_queries(self, steps: list[dict[str, str]]) -> list[dict[str, str]]:
        """
        Refine the step queries by replacing the technology names with the correct case from the database.

        Args:
            steps (list[dict[str, str]]): The list of steps to refine.

        Returns:
            list[dict[str, str]]: The refined list of steps.
        """

        ## separate company and people steps. Merge filters into the same step.
        def merge_steps(steps: list[dict[str, str]]) -> list[dict[str, str]]:
            """Merge the steps into a list of steps with the same category.

            Args:
                steps (list[dict[str, str]]): The list of steps to merge.

            Returns:
                list[dict[str, str]]: The merged list of steps.
            """
            new_steps = []
            old_step = None
            for d in steps:
                cat, s = d["category"], d["sentence"]
                is_company_step = cat.startswith("company")
                is_person_step = cat.startswith("people")
                if is_company_step:
                    if old_step == is_company_step:
                        new_steps[-1][1] += " " + s
                    else:
                        new_steps.append(["company", s])
                    old_step = is_company_step
                elif is_person_step:
                    if old_step == is_person_step:
                        new_steps[-1][1] += " " + s
                    else:
                        new_steps.append(["people", s])
                    old_step = is_person_step
                else:
                    new_steps.append([cat, s])
                    old_step = None
            return new_steps

        steps = merge_steps(steps)

        def replace(sentence: str) -> str:
            for tech, proper_name in technologies.items():
                ## Replace the potentially wrong case technology name with the correct case from the database
                sentence = re.sub(tech, proper_name, sentence, flags=re.IGNORECASE)
            return sentence

        refined_steps = []
        for cat, sentence in steps:
            refined_steps.append([cat, replace(sentence)])
        return refined_steps

    def _break_into_steps(self, text: str, model_config: dict = None) -> list[dict[str, str]]:
        if model_config is None:
            model_config = cfg["model"]

        """Separate the text into a list of logical execution steps for a business user. The steps should be in the order of execution. Non business steps should be classified as extraneous."""
        messages: list = break_into_steps["messages"].copy()
        messages.append({"role": "user", "content": text})
        tools: list = break_into_steps["tools"].copy()
        llm = LLM(config=cfg.model)
        r = llm.simple_query(
            messages=messages,
            tools=tools,
            tool_choice="break_into_steps",
        )
        # for i, val in enumerate(r.arguments()):
        #     print(i, val)
        new_steps = self._refine_step_queries(r.arguments()["steps"])

        return new_steps

    @staticmethod
    def _modify_sql_query(original_sql, prefix=""):
        """
        Modifies the provided SQL query by replacing the initial SELECT statement
        with 'SELECT id'. This function assumes the query contains joins from multiple tables.

        Args:
        original_sql (str): The original SQL query string.

        Returns:
        str: The modified SQL query with 'SELECT id' as the initial statement.
        """

        # Split the query into segments
        segments = original_sql.split("FROM")

        # Check if the query is valid (has at least one FROM segment)
        if len(segments) < 2:
            raise ValueError("The SQL query does not seem to contain a valid 'FROM' clause.")

        # Replace the initial SELECT statement with 'SELECT id'
        segments[0] = f"SELECT {prefix}id "

        # Reassemble the query
        modified_sql = "FROM".join(segments)

        return modified_sql

    def query(
        self,
        query_str: str,
        model_config: dict = None,
        limit: int = 4,
        from_person: dict = None,
        from_company: dict = None,
    ) -> list[dict[str, str]]:
        if model_config is None:
            model_config = cfg["model"]
        tables = ["people", "companies", "technologies", "company_2_technologies"]

        engine = create_engine(connection_string)
        sql_database = SQLDatabase(engine, include_tables=tables)
        query_engine = NLSQLTableQueryEngine(
            sql_database=sql_database,
            tables=tables,
        )

        steps = self._break_into_steps(text=query_str, model_config=model_config)

        if not steps:
            return [
                {
                    "type": "more_information_needed",
                    "reason": "no_steps",
                    "content": ["I'm sorry, I don't understand. Could you rephrase that?"],
                }
            ]
        for step, sentence in steps:
            print(f"Step: {step}, Sentence: {sentence}")

        company_ids = {}
        people_ids = {}
        return_response = []
        for step, sentence in steps:
            if step == "company":
                response = query_engine.query(sentence)
                print("!!!!!!!!!!")
                print(response.response, response.metadata["sql_query"])
                log.debug(response.response)

                id_query = response.metadata["sql_query"].replace("\n", " ")
                id_query = Assistant._modify_sql_query(id_query, prefix="c.")

                with engine.connect() as con:
                    result = con.execute(text(id_query))
                    company_ids = [row[0] for row in result]
                print(f"Found company ids {company_ids}")
                log.debug(f"Found company ids {company_ids}")
                r = {
                    "type": "company_list",
                    "content": [response.response],
                }
                return_response.append(r)
            elif step == "people":
                response = query_engine.query(sentence)

                log.debug(response.response)
                print(response.metadata["sql_query"].replace("\n", " "))
                r = {
                    "type": "people_list",
                    "content": [response.response],
                }
                return_response.append(r)
            elif step == "action_email":
                r = {
                    "type": "campaign",
                    "how": ["email"],
                    "content": [],
                }
                return_response.append(r)
                if company_ids and not people_ids:
                    ## Get list of people where company_id in company_ids and job_title like Sales
                    query = 'SELECT * from people where company_id in ({}) and job_title LIKE "%sale%" and work_email is not NULL'.format(
                        ",".join([f"'{str(id)}'" for id in company_ids])
                    )
                    print(f"Query = {query}")
                    log.debug(f"Query = {query}")
                    with engine.connect() as con:
                        result = con.execute(text(query))
                        people = [row for row in result]
                        pids = [r[people_columns_2_idx["id"]].strip("'").strip('"') for r in people]
                    people_ids = {}
                    for p in people:
                        np = {}
                        np = {k: v for k, v in zip(people_columns, p)}
                        people_ids[p[people_columns_2_idx["id"]]] = np

                    print(f"people are: {pids}")
                    log.debug(f"people are: {pids}")

                # print("action_email")
                if not people_ids:
                    print("No people to email")
                    return [
                        {
                            "type": "more_information_needed",
                            "content": ["No people to email. Could you refine your query?"],
                        }
                    ]
                    # raise Exception("No people to email. Could you refine your query?")

                i = 0
                for pid, p in people_ids.items():
                    i += 1
                    if limit and i > limit:
                        break
                    print("Emailing person ", i, p["first_name"], p["last_name"])
                    # for i, val in enumerate(p.items()):
                    #     k, v = val
                    #     print(i, k,v )
                    prompt = generate_openai_prompt(
                        from_person=from_person,
                        to_person=p,
                        from_company=from_company,
                        to_company={
                            "name": "6sense",
                        },
                    )
                    pprint(prompt)

                    llm = LLM(config=cfg.model)
                    result = llm.simple_query(prompt)
                    pprint(result)
                    print("##############")
                    print(result.response)
                    d = json.loads(result.response)
                    if not "email_subject" in d:
                        raise Exception("No email subject found")
                    if not "email_body" in d:
                        raise Exception("No email body found")
                    # print(result.arguments())
                    print("@@@@@@@@@@@@@@")
                    r["content"].append(
                        {
                            "type": "email",
                            "user_email": p["work_email"],
                            "user_name": p["first_name"] + " " + p["last_name"],
                            "user_id": p["id"],
                            "company_id": p["company_id"],
                            "email_subject": d["email_subject"],
                            "email_body": d["email_body"],
                        }
                    )

                    ## From the prompt, get the email from OpenAI
                    ## return that response as a json
            else:
                print(step, sentence)
        if len(return_response) == 0:
            return_response = [{"type": "extraneous", "content": [query_str]}]
        return return_response
