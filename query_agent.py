from cat.utils import singleton
from cat.looking_glass.prompts import MAIN_PROMPT_PREFIX
from cat.log import log

import json
from .settings import datasources

from langchain.agents import create_sql_agent, create_json_agent
#from langchain.agents import create_csv_agent
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit, JsonToolkit 
from langchain.sql_database import SQLDatabase 
from langchain.agents.agent_types import AgentType
from langchain.tools.json.tool import JsonSpec

from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import Qdrant

from langchain.schema.document import Document
from langchain.chains import RetrievalQA
from langchain.agents import Tool
from typing import Sequence

@singleton
class QueryCatAgent:

    TRAINING_KEY = "query_cat_training_mode"

    def __init__(self, cat) -> None:
        self.cat = cat
        self.settings = None


    # Load configurations
    def _load_configurations(self):

        # Acquire settings
        settings = self.cat.mad_hatter.get_plugin().load_settings()

        # If the settings are the same, skip function
        if self.settings and self.settings == settings:
            return

        log.critical("Load query examples..")

        # Set settings
        self.settings = settings

        self._load_query_examples()
        self._load_ddl_examples()


    # Load query examples from settings
    def _load_query_examples(self):

        # Get user message
        self.user_message = self.cat.working_memory["user_message_json"]["text"]

        # Acquire the agent type
        datasource_type = self.settings["ds_type"]
        self.agent_type = datasources[datasource_type]["agent_type"]

        # Create prompt_template from examples
        self.query_prompt_tpl = None
        if self.settings["query_examples"] != '':
            
            # Get query examples
            query_examples = json.loads(self.settings["query_examples"])

            if query_examples:
                # Create query_example selector
                query_example_selector = SemanticSimilarityExampleSelector.from_examples(
                    query_examples, 
                    self.cat.embedder, 
                    Qdrant,
                    k=1,
                    collection_name='query_examples',
                    location=':memory:'
                )
                
                # Create example prompt
                query_example_prompt = PromptTemplate(
                    input_variables=["question", "answer"], 
                    template="Question: {question}\n{answer}"
                )
                
                # Create query_prompt_tpl from examples_selector and example_prompt
                self.query_prompt_tpl = FewShotPromptTemplate(
                    example_selector = query_example_selector,
                    example_prompt   = query_example_prompt,
                    suffix="Question: {input}",
                    input_variables=["input"]
                )


    # Load ddl examples from settings
    def _load_ddl_examples(self):
        
        '''
        # Get ddl examples
        ddl_examples = [
            {"ddl": "<ddl description 1>", "metadata": {"attr1": "value 1", "attr2": "value 2"}},
            {"ddl": "<ddl description 2>", "metadata": {"attr1": "value 1", "attr2": "value 2"}},
            # ...
        ]
        '''

        # Create prompt_template from examples
        self.additional_tools = []
        if self.settings["ddl_examples"] != '':

            # Get ddl examples
            ddl_examples = json.loads(self.settings["ddl_examples"])
            
            if ddl_examples:
            
                # Transform json to Document array
                data_ddl = [
                    Document(page_content=item["ddl"], metadata=item["metadata"])
                    for item in ddl_examples
                ]

                # Create DocSearch
                ddl_docsearch = Qdrant.from_documents(
                    data_ddl, 
                    self.cat._embedding, 
                    collection_name="ddl_examples",
                    location=":memory:"
                )

                # Get Retrieval chain
                ddl_retrieval_chain = RetrievalQA.from_chain_type(
                    llm=self.cat._llm, 
                    chain_type="stuff", 
                    retriever=ddl_docsearch.as_retriever()
                )

                # Set Tool description
                ddl_tool_name = "DDL Explanation"
                ddl_tool_description = """
                useful for when you need to know the details 
                of a particular sql entity present in the database.
                """

                # Create Retrieval Tool
                ddl_retrieval_tool = Tool(
                    func=ddl_retrieval_chain.run,
                    name=ddl_tool_name,
                    description=ddl_tool_description,
                )

                # Add tool in additional_tools array
                self.additional_tools = [ddl_retrieval_tool]


    # Execute agent to get a final thought, based on the type 
    def get_reasoning_agent(self) -> str:
        
        # Load configurations
        self._load_configurations()

        # Get input prompt
        self.input_prompt = self._get_input_prompt()
        
        # Execute agent based on the type
        if self.agent_type == "sql":
            return self._get_reasoning_sql_agent()
        if self.agent_type == "csv":
            return self._get_reasoning_csv_agent()
        if self.agent_type == "json":
            return self._get_reasoning_json_agent()
        
        return ""


    # Get agent input prompt
    def _get_input_prompt(self):
    
        if self.query_prompt_tpl:
            # Get input prompt from query_prompt_tpl
            input_prompt = self.query_prompt_tpl.format(input=self.user_message)
        else:
            # Get input prompt from settings
            input_prompt = self.user_message
            if self.settings["input_prompt"] != '':
                input_prompt = self.settings["input_prompt"].format(
                    user_message=self.user_message
                )

        print("=====================================================")
        print(f"Input prompt:\n{input_prompt}")
        print("=====================================================")

        return input_prompt


    # Return final response, based on the user's message and reasoning
    def get_final_output(self, thought):

        # Load configurations
        self._load_configurations()

        # Get prompt
        prompt_prefix = self.cat.mad_hatter.execute_hook("agent_prompt_prefix", MAIN_PROMPT_PREFIX, cat=self.cat)

        # Get user message and chat history
        chat_history = self.cat.agent_manager.agent_prompt_chat_history(
            self.cat.working_memory["history"]
        )

        # Default output Prompt
        output_prompt = f"""{prompt_prefix}
        You have elaborated the user's question, 
        you have searched for the answer and now you 
        have the solution in your Thought; 
        reply to the user briefly, 
        precisely and based on the context 
        of the dialogue.
        - Human: {self.user_message}
        - Thought: {thought}
        - AI:"""

        # Set output prompt from settings
        if self.settings["output_prompt"] != '':
            output_prompt = self.settings["output_prompt"].format(
                prompt_prefix = prompt_prefix, 
                user_message  = self.user_message, 
                thought       = thought, 
                chat_history  = chat_history
            )

        # Invoke LLM and obtain final and contestual response
        print("=====================================================")
        print(f"Output prompt:\n{output_prompt}")
        print("=====================================================")
        return self.cat.llm(output_prompt)


    # Execute sql agent
    def _get_reasoning_sql_agent(self):

        # Create connection string
        datasource_type = self.settings["ds_type"]
        connection_string = datasources[datasource_type]["conn_str"].format(**self.settings)
        log.warning(f"Connection string: {connection_string}")

        # Create sql connection
        try:
            db = SQLDatabase.from_uri(connection_string)

            # Create SQL DB Toolkit
            sqldbtlk = SQLDatabaseToolkit(db=db, llm=self.cat._llm)

            # Create SQL Agent
            agent_executor = create_sql_agent(
                llm         = self.cat._llm,
                toolkit     = sqldbtlk,
                verbose     = True,
                agent_type  = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                extra_tools = self.additional_tools
            )
        except Exception as e:
            log.error(f"Failed to create SQL connection: {e}")
            return f"it was not possible to connect to the selected data source: {e}"

        # Obtain final thought, after agent reasoning steps
        final_thought = agent_executor.run(self.input_prompt)
        return final_thought


    # Execute csv agent
    def _get_reasoning_csv_agent(self):

        # Get csv file path
        csv_file_path = self.settings["host"]
        delimiter = self.settings["extra"] if self.settings["extra"].strip() else ";"

        # Create CSV agent
        try:
            agent_executor = create_csv_agent(self.cat._llm, csv_file_path, verbose=True)
            #agent_executor = create_csv_agent(self.cat._llm, csv_file_path, pandas_kwargs={'delimiter': delimiter}, verbose=True)
        except Exception as e:
            log.error(f"Failed to create SQL connection: {e}")
            return f"it was not possible to connect to the selected data source: {e}"

        # Obtain final thought, after agent reasoning steps
        final_thought = agent_executor.run(self.input_prompt)
        return final_thought


    # Execute json agent
    def _get_reasoning_json_agent(self):

        # Get json file path
        json_file_path = self.settings["host"]

        # Get json data
        with open(json_file_path, 'r') as reader:
            data = json.load(reader)

        # Create JSON toolkit
        json_spec = JsonSpec(dict_= data, max_value_length=4000)
        json_toolkit = JsonToolkit(spec=json_spec)

        # Create JSON agent
        try:
            agent_executor = create_json_agent(
                llm=self.cat._llm,
                toolkit=json_toolkit,
                verbose=True
            )
        except Exception as e:
            log.error(f"Failed to create SQL connection: {e}")
            return f"it was not possible to connect to the selected data source: {e}"

        # Obtain final thought, after agent reasoning steps
        final_thought = agent_executor.run(self.input_prompt)
        return final_thought


    #############################
    ######### TRAINING ##########
    #############################

    # Check if is in training mode
    def training_mode(self):

        # If training is not set, return false
        if self.settings["training"] is False:
            return False

        # Return Training mode state
        if QueryCatAgent.TRAINING_KEY in self.cat.working_memory.keys():
            return self.cat.working_memory[QueryCatAgent.TRAINING_KEY]
        
        return False
    

    def add_training_data(self):
        # Get user message
        self.user_message = self.cat.working_memory["user_message_json"]["text"]

        #TODO ...
        
        return "The data has been acquired"
