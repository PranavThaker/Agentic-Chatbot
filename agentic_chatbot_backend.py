from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage
from typing import TypedDict,Annotated
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
load_dotenv()

 
llm = ChatGroq(model='openai/gpt-oss-120b')


 
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

 
def chat_node(state:ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages':[response]}

 
checkpoint = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

workflow = graph.compile(checkpointer=checkpoint)
