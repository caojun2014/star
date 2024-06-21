from fastapi import APIRouter,Request
llm_router = APIRouter(prefix="/api/llm", tags=["大模型接口"])
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('.env'))
from langchain_openai import ChatOpenAI
import os

from langchain_core.prompts import PromptTemplate
#llm = Tongyi()
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
template = """

你是一个数据分析师和前端开发专家，接下来我会按照以下固定格式给你提供内容：

分析需求：{target} 数据分析的需求或者目标 
原始数据：{data} csv格式的原始数据


请根据这两部分内容，按照以下指定格式生成内容（此外不要输出任何多余的开头、结尾、注释）

【【【【【 前端 Echarts V5 的 option 配置对象js代码，合理地将数据进行可视化，不要生成任何多余的内容，比如注释
如果用户未指定生成图表样式，你就生成合适的柱状图或者饼状图

【【【【【
明确的数据分析结论、越详细越好，不要生成多余的注释

"""

prompt = PromptTemplate.from_template(template)
chain = prompt | llm
target="帮我分析一下数据的指标"
data = """  日期,用户数
      1号,10,
        2号, 20,
     3号, 30,
"""
print(chain.invoke({"target": target ,"data": data}))