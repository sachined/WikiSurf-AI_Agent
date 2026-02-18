This was inspired by a YouTube video by "Tech With Tim" (https://www.youtube.com/watch?v=bTMPwUgLZf0), where he built an AI Agent in Python last year.

The Process:

Since then, there have been many changes to a few libraries used in this project (especially langchain and its friends). 
So I researched with AI on snippets of code that were functioning but deprecated.
That was mostly my first day and a bit of the second day.
Once that was done, I abstracted few classes from a wall of text into few Python files.
So far, the AI Agent has a Wiki tool that can look up information on its website (Wikipedia), a DuckDuckGo (DDG) tool that functions like Google Search.

How It Works:

You can ask the Agent (best to ask about well-documented matters; it is not a social search engine).
You can also leave it blank, and it will tell you about the Eiffel Tower.
If the Wiki tool fails, the DDG tool will be used. 
If that also fails, the buck stops with the AI agent (LLM-powered). Only Anthropic and OpenAI...for now (Langchain-dependent).
It will show a Progress bar for all steps, and clean up the text into a neat box for each step (Agent Action/Output, Tool Output). 
Each step is shown in a different color for better viewability.
Ultimately, it will show a box with the topic, summary, sources, and tools used for the query (Structured Research Response).
Will provide screenshots soon.

Thoughts:
I am happy that this AI Agent works! I spent too much time trying to get color on the Terminal. It was a simple checkbox option in its settings after looking all over (even with AI).
Still saved some code that might work for others. Would appreciate any feedback. Now it's 🕡 in the morning 😢

Future Plans:
Possibly add 2 more tools, but must be relevant to AI Agent progression, such as utilizing sub-agents while providing a supervisory role for the existing agent (WikiSurf). 🤷‍♂️

<img width="336" height="167" alt="image" src="https://github.com/user-attachments/assets/b00fc5e0-e932-46bb-837e-5703c1225795" />


