**CrowdWisdomTrading AI Agent**   
**Intern position assessment**

Hi,  
The document gives a brief introduction to an assignment to check your qualifications for the internship. Please complete it on your own time and submit it up to 1 week.

**Project Overview**  
Create a backend Python script using CrewAI that unifies different gambling websites by product and writes a news review  

**Technical Requirements**  
\- Language: Python  
\- Framework: [CrewAI](https://github.com/crewAIInc/crewAI) (latest), [browser-use](https://github.com/browser-use/browser-use)   
\- LLM Provider: [litellm](https://www.litellm.ai/) \+ any model you want

**Project Scope**  
Develop a CrewAI agents that:  
1\. Scrape data from at least 3 different websites:  
 polymarket.com, prediction-market.com, kalshi.com, (or any other sit ein [https://www.cbinsights.com/company/predictit/alternatives-competitors](https://www.cbinsights.com/company/predictit/alternatives-competitors))  and build a unified products board  
2\. Uses CrewAI agents to:  
2.1 analyze the different products  
2.2 sort and compare them  
3\. Generates a CSV with:  
3.1 unified product list  
3.2 its price among the different sites  
3.3 confidence level for same product

Agent Design  
Agent 1: X Data Collector  
\- Retrieve data using scrape tools   
\- Provide a JSON format results

Agent 2: identify products and if they are the same or not  
\- Process collected data  
\- Provide a JSON format results

Agent 3: re-arrange the unified data in a great UI  
\- Provide a CSV format results

**you must use crewai flow with guardrails\!**

**Deliverables**  
1\. Python script with CrewAI implementation  
2\. Sample input/output examples

**Evaluation Criteria**  
**\- working output**  
**\- Effective use of CrewAI Flow \+ tools \+ RAG**  
\- Data retrieval and processing  
\- Code clarity and organization  
\- using tools with building code agents like [cursor.com](http://cursor.com) / [https://windsurf.com/](https://windsurf.com/)  etc. 

**Extra points for (for example):**  
 \- logging and error handling   
 \- chatting with the RAG about the different products

**examples related information:**  
https://github.com/crewAIInc/crewAI-quickstarts  
[https://www.youtube.com/watch?v=e3xP\_lAjktI](https://www.youtube.com/watch?v=e3xP_lAjktI)  
[https://medium.com/@ShaniCodes/so-i-built-my-own-social-media-ai-crew-because-i-didnt-want-to-pay-for-jasper-ai-40a279ffe89a](https://medium.com/@ShaniCodes/so-i-built-my-own-social-media-ai-crew-because-i-didnt-want-to-pay-for-jasper-ai-40a279ffe89a)  
https://github.com/Folken2/ag-ui-crewai-research  
[https://www.youtube.com/watch?v=B8RvpUGD2Uw](https://www.youtube.com/watch?v=B8RvpUGD2Uw)  
[https://github.com/patchy631/ai-engineering-hub/tree/main/content\_planner\_flow](https://github.com/patchy631/ai-engineering-hub/tree/main/content_planner_flow)  
[https://github.com/alexfazio/viral-clips-crew](https://github.com/alexfazio/viral-clips-crew)  
[https://www.youtube.com/watch?v=8PtGcNE01yo](https://www.youtube.com/watch?v=8PtGcNE01yo)  
[https://github.com/codebasics/crewai-crash-course](https://github.com/codebasics/crewai-crash-course)

**Submission Requirements**  
\- Runnable Python code (no dockers etc. keep it simple)  
\- Clear documentation of the approach  
\- video of running code

---

## **Timeline**

You will have **5 \- 7 days** to complete this task. Please ensure you submit the deliverables by the end of this period.

---

## **Submission by email**  [gilad@crowdwisdomtrading.com](mailto:gilad@crowdwisdomtrading.com)

Submit the following:

* A link to your GitHub/GitLab repository.  
* output examples.

We look forward to seeing your solution\!

Thanks for applying\!  
Gilad  
CrowdWisdomTrading CEO