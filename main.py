from dotenv import load_dotenv
load_dotenv()

from crewai import LLM, Agent, Task, Crew  
from email_tool import MyCustomTool

email_tool = MyCustomTool()  

llm=LLM(
    model="gpt-4o-mini",
    temperature=0.1
)

researcher= Agent(
    role="researcher agent",
    goal="analyze trips and give best planning for the trip.",
    backstory=" highly experienced skilled in researcher in planning trips.",
    verbose=True,
    llm=llm
)

optimizer= Agent(
    role="optimizer agent",
    goal="analyze trips and give best planning for the trip.",
    backstory="highly experienced skilled in researcher in planning trips. give efficent and budget friendly hotels and route costs ",
    verbose=True,
    llm=llm
)

writer=Agent(
    role="writer agent, Give planning, schedules and costing required.",
    goal="write costing , weather , requirements for trip etc for the trip.",
    backstory="highly experienced skilled in giving well planned trips.Give a short summary.",
    verbose=True,
    llm=llm,
    tools=[email_tool]  
)

task1 = Task(
    description="Find hotels , resorts , and places to stay in {city} for {travelers}.",  
    expected_output="Give names of hotels to stay"
                    "give summary in one short and concise paragraph( give bullet points)",
    agent=researcher,
)

task2 = Task(
    description="find best budget friendly places to stay , and give day wise planner to visit places and give efficient routes and costs.",
    expected_output="summary for planning trips."
                    "give summary in one short and concise paragraph(give bullet points)",
    agent=optimizer,
    context=[task1],
)

task3 = Task(
    description="write well planned/short and concise guide to visit {city} for {travelers} starting {start_date}. Special requirements: {special_requirements}. After writing, use the email sender tool to send the complete trip plan.",  # ✅ removed {topic}, added email instruction
    expected_output="summary for planning trips in a short and concise way."
                    "give summary in one short and concise paragraph( give bullet points)."
                    "Confirm email was sent.",
    agent=writer,
    context=[task2],
)

crew= Crew(
    agents=[researcher,optimizer,writer],
    tasks=[task1,task2,task3],
    verbose=True,
)

result = crew.kickoff(inputs={
    "city": "Mumbai, India",
    "travelers": "4 adults",
    "duration": "2 days",
    "budget": "Moderate (Comfortable but not luxury)",
    "interests": "Street food, historical landmarks, and coastal views",
    "start_date": "March 15, 2026",
    "special_requirements": "Need a vehicle that fits 4 people + luggage; prefer staying near South Mumbai."
})

email_tool.run(str(result))  
