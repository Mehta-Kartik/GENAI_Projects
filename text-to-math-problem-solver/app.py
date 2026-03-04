# import streamlit as st
# from langchain_groq import ChatGroq
# from langchain_classic.chains import LLMChain, LLMMathChain  # Math chains OK
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.utilities import WikipediaAPIWrapper
# from langchain_core.tools import Tool  # ✅ Fixed: Tool here
# from langchain_classic.agents import initialize_agent  # ✅ AgentType + initialize_agent OK (legacy)
# from langchain_community.callbacks import StreamlitCallbackHandler  # ✅ Fixed callback
# from langchain_classic.agents import AgentType
# from langchain_community.tools import WikipediaQueryRun


# st.set_page_config(page_title="Text to Math Problem Solver and Data Search Assistant")

# st.title("Text To MAth Problem Solver")

# api_key=st.sidebar.text_input("Enter your Groq API key",type="password")


# if not api_key:
#     st.info("Please add your Groq API key to continue")
#     st.stop

# llm=ChatGroq(groq_api_key=api_key,model="llama3-70b-8192")


# wikipedia=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
# # wikipedia=Tool(
# #     name="Wikipedia",
# #     func=wikipedia.run,
# #     description="A tool for searching the internet and solving our math problem to find various info"
# # )

# math_chain=LLMMathChain.from_llm(llm=llm)
# calculator=Tool(
#     name="calculator",
#     func=math_chain.run,
#     description="A tool for answering math related questions. Only input mathematical expression needs to be provided"
# )

# prompt="""
# You are an agent tasked for solving users mathematical problems. Logically arrive to the solution and display the solution in point wise for the question below
# Question:{question}
# """

# prompt=ChatPromptTemplate.from_template(
#     """
#     You are an agent tasked for solving users mathematical problems. Logically arrive to the solution and display the solution in point wise for the question below
#     Question:{question}
#     """
# )

# #Combines all the problem to chain
# chain=LLMChain(llm=llm,prompt=prompt)

# reasoning_tool=Tool(
#     name="Reasoning tools",
#     func=chain.run,
#     description="A tool for answering logic-based and reasoning questions."
# )

# # assistant_agent=initialize_agent(
# #     tools=[wikipedia,calculator,reasoning_tool],
# #     llm=llm,
# #     agent=AgentType.OPENAI_FUNCTIONS,
# #     verbose=False,
# #     handle_parsing_errors=True
# # )


# assistant_agent = AgentExecutor(
#     agent=agent, 
#     tools=[wikipedia, calculator, reasoning_tool], 
#     verbose=True,
#     handle_parsing_errors=True
# )


# if "messages" not in st.session_state:
#     st.session_state["messages"]=[
#         {"role":"assistant","content":"Hi I am a math chatbot who can answer all your math question"},
        
#     ]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])



# ##function to generate the response

# def generate_response(userq):
#     response=assistant_agent.invoke({"input":userq})
#     return response

# #Let's start the interaction
# question=st.text_area("Enter your question","what is 8+2")
# # if st.button("Find my answer"):
# #     if question:
# #         with st.spinner("Waiting..."):
# #             st.session_state.messages.append({"role":"user","content":question})
# #             st.chat_message("user").write(question)
# #             st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
# #             response=assistant_agent.invoke({'input':question})
# #             st.session_state.messages.append({"role":"assistant","content":response})
# #             st.write(response)
# #             st.success()
# #     else:
# #         st.warning("Please enter the question")


# # if st.button("Find my answer"):
# #     if question:
# #         # Add user message to state and display
# #         st.session_state.messages.append({"role": "user", "content": question})
# #         st.chat_message("user").write(question)
        
# #         with st.chat_message("assistant"):
# #             # 1. Initialize the callback handler
# #             st_cb = StreamlitCallbackHandler(st.container())
            
# #             # 2. Pass callbacks directly into invoke to avoid the TypeError
# #             # Note: config is the standard way to pass callbacks in newer LangChain
# #             response = assistant_agent.invoke(
# #                 {"input": question}, 
# #                 config={"callbacks": [st_cb]}
# #             )
            
# #             # 3. Extract the 'output' string from the response dictionary
# #             answer = response["output"]
            
# #             st.session_state.messages.append({"role": "assistant", "content": answer})
# #             st.write(answer)
# #     else:
# #         st.warning("Please enter the question")


# # ... (Previous code remains the same until the button)

# if st.button("Find my answer"):
#     if not question.strip():
#         st.warning("Please enter a question")
#     else:
#         # Display user question
#         st.session_state.messages.append({"role": "user", "content": question})
#         st.chat_message("user").write(question)

#         with st.chat_message("assistant"):
#             # Set up the Streamlit callback to show thoughts
#             st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
            
#             try:
#                 # pass callbacks in the config dictionary
#                 full_response = assistant_agent.invoke(
#                     {"input": question},
#                     {"callbacks": [st_cb]}
#                 )
                
#                 final_answer = full_response["output"]
#                 st.session_state.messages.append({"role": "assistant", "content": final_answer})
#                 st.write(final_answer)
                
#             except Exception as e:
#                 st.error(f"An error occurred: {e}")



import streamlit as st
from langchain_groq import ChatGroq
from langchain_classic.chains import LLMMathChain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent  # <--- Changed this
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.tools import WikipediaQueryRun

st.set_page_config(page_title="Text to Math Problem Solver", layout="wide")
st.title("Text To Math Problem Solver")

api_key = st.sidebar.text_input("Enter your Groq API key", type="password")

if not api_key:
    st.info("Please add your Groq API key in the sidebar to continue")
    st.stop()

# 1. Initialize LLM
# Removed streaming=True here because it can sometimes interfere with tool-calling logic on certain Groq models
llm = ChatGroq(
    groq_api_key=api_key, 
    model="llama-3.1-8b-instant", 
    temperature=0
)

# 2. Define Tools
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="Useful for when you need to answer questions about math. Input should be a mathematical expression."
)

tools = [wikipedia, calculator]

# 3. Define the Prompt (Updated for Tool Calling)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that solves math problems and searches for info. Logically arrive at the solution step-by-step."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. Create the Tool Calling Agent (More compatible with Groq)
agent = create_tool_calling_agent(llm, tools, prompt)
assistant_agent = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! How can I help you with math today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

question = st.text_area("Enter your question")

if st.button("Find my answer"):
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)

        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container())
            
            try:
                # Still using config to avoid the previous TypeError
                response = assistant_agent.invoke(
                    {"input": question},
                    config={"callbacks": [st_cb]}
                )
                
                final_answer = response["output"]
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                st.write(final_answer)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a question.")