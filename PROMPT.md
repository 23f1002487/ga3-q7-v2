Case Study: Delegating Deep Work to CLI Coding Agents
Scenario: Your team experiments with CLI-based coding copilots (Copilot CLI) to auto-solve well-scoped engineering chores. You must expose a public FastAPI endpoint that receives a task description and passes it to a coding agent that is allowed to create files, run code, and return the tool output safely.

Implement a FastAPI app with a GET /task?q=... route.
Inside the route, forward q to any CLI coding agent documented in AI Coding CLI Playbook and wait for the agent to finish the single task run (no human edits).
Respond with JSON { "task": q, "agent": "copilot-cli", "output": "...", "email": "23f1002487@ds.study.iitm.ac.in" }.
Set CORS to allow cross-origin GET requests and keep logs of the agent run.
For example you'll receive this task: Write and run a program that prints the 24th Fibonacci number (F0 = 0, F1 = 1). Return just the number.
We'll GET /task?q=..., expect application/json, verify agent, output, and email, and confirm the output matches the 24th Fibonacci number.

For outsourcing the task:
Use  https://aipipe.org/openai/v1/... instead of https://api.openai.com/v1/... as the OPENAI_BASE_URL
Use the token from https://aipipe.org/login as the OPENAI_API_KEY

Deployment hosting:
    - Use railway to host server
    OR
    - if its a single function with route /task, use vercel to host the function