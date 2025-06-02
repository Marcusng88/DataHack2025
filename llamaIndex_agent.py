# import time
# # from llama_index.core.llms import ChatMessage
# from utils import get_API
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# import streamlit as st
# import json

# import asyncio


# from llama_index.core.query_pipeline import (
#     QueryPipeline as QP,
#     Link,
#     InputComponent,
# )
# from llama_index.experimental.query_engine.pandas import (
#     PandasInstructionParser,
# )
# from llama_index.core import PromptTemplate
# from llama_index.llms.google_genai import GoogleGenAI


# # Ensure an event loop is created
# try:
#     asyncio.get_running_loop()
# except RuntimeError:
#     asyncio.set_event_loop(asyncio.new_event_loop())

# get_key = get_API()
# key = get_key
# llm = GoogleGenAI(api_key=key, model_name="models/gemma-3-27b-it")

# @st.cache_data
# def load_data():
#     # Replace this with your actual data-loading logic.
#     # For example: pd.read_csv("your_file.csv")
#     # Here we simulate with random data—swap in your real df.
#     n = 1000
#     rng = np.random.default_rng(42)
#     df = pd.read_csv('datasets\Combined_Less.csv')
#     return df

# df = load_data()

# def query_pipeline(df):
#     instruction_str = (
#         "1. Convert the query to executable Python code using Pandas.\n"
#         "2. The final line of code should be a Python expression that can be called with the `eval()` function.\n"
#         "3. The code sh=ould represent a solution to the query.\n"
#         "4. st.warning ONLY THE EXPRESSION.\n"
#         "5. Do not quote the expression.\n"
#     )

#     pandas_prompt_str = (
#         "You are working with a pandas dataframe in Python.\n"
#         "The name of the dataframe is `df`.\n"
#         "This is the result of `st.warning(df.head())`:\n"
#         "{df_str}\n\n"
#         "Follow these instructions:\n"
#         "{instruction_str}\n"
#         "Query: {query_str}\n\n"
#         "Expression:"
#     )
#     response_synthesis_prompt_str = (
#         "Given an input question,PLEASE IGNORE THE JSON VARIABLE. synthesize a response from the query results.\n"
#         "You are an assistant in Data Analystic, your name is 'Hokkien Mee Black Data Analystic Assistant'\n"
#         "Make it interactive and informative with minimum 125 words.\n"
#         "If the user query is irrelevant to the dataset , PROVIDE THEM SOME SUGGESTION"
#         "Please structure the response markdown in a proper way.(eg. Title should have bold and bigger text size, break line after title)"
#         "You may add emoji in your response to make it more interactive.\n"
#         "Query: {query_str}\n\n"
#         "Pandas Instructions (optional):\n{pandas_instructions}\n\n"
#         "Pandas Output: {pandas_output}\n\n"
#         "Graph Generation Output (JSON):\n{llm3_json_output}\n\n"
#         "Response: "
#     )

#     graph_generator_prompt_str = (
#         "Given an input pandas dataframe information {pandas_output} , the input can be None\n"
#         "Figure out whether this information needed to be plot as a graph or not"
#         """Write it in a json format {
#             plot: bool,
#             graph_type: type,
#             title: str,
#             x_label: str,
#             y_label: str,
#             data_x: list,
#             data_y: list,
#             color: str,
#         }\n"""
#         """The plot is True if needed to be plot , False otherwise.
#         graph_type determines which graph is needed to be plot.
#         title will be the name for the graph.
#         x_label is the label for x-axis.
#         y_label is the label for y-axis.
#         data_x is the list of data for x-axis.
#         data_y is the list of data for y-axis.
#         color is the color styling for the plotly graph. Please use color available for plotly\n

#         """
#         "Do not give other output other than the json\n"
#     )

#     pandas_prompt = PromptTemplate(pandas_prompt_str).partial_format(
#         instruction_str=instruction_str, df_str=df.head(5)
#     )
#     pandas_output_parser = PandasInstructionParser(df)
#     response_synthesis_prompt = PromptTemplate(response_synthesis_prompt_str)
#     graph_generator_prompt = PromptTemplate(graph_generator_prompt_str)

#     global qp
#     qp = QP(
#         modules={
#             "input": InputComponent(),
#             "pandas_prompt": pandas_prompt,
#             "llm1": llm,
#             "pandas_output_parser": pandas_output_parser,
#             "response_synthesis_prompt": response_synthesis_prompt,
#             "llm2": llm,
#             "graph_generator_prompt": graph_generator_prompt,
#             "llm3": llm,
#         },
#         verbose=True,
#     )
#     qp.add_chain(["input", "pandas_prompt", "llm1", "pandas_output_parser"])
#     qp.add_links(
#         [
#             Link("input", "response_synthesis_prompt", dest_key="query_str"),
#             Link(
#                 "llm1", "response_synthesis_prompt", dest_key="pandas_instructions"
#             ),
#             Link(
#                 "pandas_output_parser",
#                 "response_synthesis_prompt",
#                 dest_key="pandas_output",
#             ),
#         ]
#     )

#     qp.add_link(
#         "pandas_output_parser",
#         "graph_generator_prompt",
#         dest_key="pandas_output"
#     )

#     qp.add_link(
#         "graph_generator_prompt",
#         "llm3"
#     )
#     qp.add_link(
#         "llm3",
#         "response_synthesis_prompt",
#         dest_key="llm3_json_output"
#     )
#     qp.add_link("response_synthesis_prompt", "llm2")

# def graph_generation(response):

#   try:
#         response = json.loads(response)
#   except json.JSONDecodeError:
#         st.warning("Error: Invalid JSON string provided.")
#         return None

#   if response.get('plot'):
#         graph_type = response.get('graph_type', 'scatter').lower()
#         title = response.get('title', 'Generated Graph')
#         x_label = response.get('x_label', 'X-axis')
#         y_label = response.get('y_label', 'Y-axis')
#         data_x = response.get('data_x', [])
#         data_y = response.get('data_y', [])
#         color = response.get('color')

#         if not data_x or not data_y or len(data_x) != len(data_y):
#             st.warning("Error: Invalid or missing data for plotting.")
#             return None

#         df = pd.DataFrame({'x': data_x, 'y': data_y})
#         if graph_type == 'scatter':
#             fig = go.Figure(data=[
#                 go.Scatter(x=df['x'], y=df['y'],
#                         mode='markers',
#                         marker_color=color,
#                         name=title)
#             ])
#         elif graph_type == 'line':
#             fig = go.Figure(data=[
#                 go.Scatter(x=df['x'], y=df['y'],
#                         mode='lines',
#                         line=dict(color=color),
#                         name=title)
#             ])
#         elif graph_type == 'bar':
#             fig = go.Figure(data=[
#                 go.Bar(x=df['x'], y=df['y'],
#                     marker_color=color,
#                     name=title)
#             ])
#         elif graph_type == 'histogram':
#             fig = go.Figure(data=[
#                 go.Histogram(x=df['x'],
#                             marker_color=color,
#                             name=title)
#             ])
#         else:
#             # Fallback to a scatter plot with a warning.
#             st.warning(f"Warning: Graph type '{graph_type}' is not supported. Defaulting to scatter plot.")
#             fig = go.Figure(data=[
#                 go.Scatter(x=df['x'], y=df['y'],
#                         mode='markers',
#                         marker_color=color,
#                         name=title)
#             ])

#         # Update the layout with a title and axis labels.
#         fig.update_layout(
#             title=title,
#             xaxis_title=x_label,
#             yaxis_title=y_label,
#             template='plotly_white'
#         )
#         return fig
#   else:
#         st.warning("Plotting is disabled in the response.")
#         return None
# def agent_prompt(prompt):
#   chat_history = []
#   user_input = prompt
#   try:
#     response,x = qp.run_with_intermediates(query_str=user_input+" .You may refer the chat history "+str(chat_history),)
#     chat_history.append("User input, "+user_input)
#     chat_history.append("AI answer, "+response.message.content)

#     graph_response_extraction = (str(x.get('llm3')).split('```'))
#     graph_response = graph_response_extraction[1]
#     graph_data = graph_response.replace('json', '').replace('\\n', '')
#     graph = graph_generation(graph_data)
#     return response.message.content, graph

#   except Exception as e:
#     st.warning(f"An error occurred: {e}")
#     st.warning("Attempting to access results directly from pipeline state if possible (this depends on the specific QP implementation)")

# def agent_interface():
#     if "messages" not in st.session_state:
#         st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     col1,col2 = st.columns([3,1])
#     if prompt := st.chat_input("What is up?"):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         with st.chat_message("assistant"):
#             message_placeholder = st.empty()
#             full_response = ""

#             with st.spinner("AI agent is thinking..."):
#                 query_pipeline(df)
#                 assistant_response,graph = agent_prompt(prompt)
#                 if graph is not None and not isinstance(graph, str):
#                     st.plotly_chart(graph)
                
#                 for line in assistant_response.split("\n"):
#                     for chunk in line.split():
#                         full_response += chunk + " "
#                         time.sleep(0.05)
#                         message_placeholder.markdown(full_response + "▌")
#                     full_response += "\n"
#                     message_placeholder.markdown(full_response + "▌")

#             message_placeholder.markdown(full_response)
#         st.session_state.messages.append({"role": "assistant", "content": full_response})