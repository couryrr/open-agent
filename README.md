# The Process of Building an Agent
---

## The platform so far

I wanted something that could be a cheap experiment. Saying that though is not totally true.
To run this you need a machine with enough RAM and a GPU to handle llms. 

The interface is a TUI using the python Textual library.

The interaction with llms is with the python ollama sdk. There is a plan to expand 
on this with other providers via APIs.

## My First approach

I just took a markdown and appended to it. I would then feed that entire document
into the llm as the user prompt. It was not planned to work and it did not work.

With some of these smaller models it was pretty funny. I did not save the output 
but since the entire conversation was being re-feed in the llm would just follow the
structure and create its own conversation.

I had a conversation that started with "This is a test of the context window. Where are my shoes?"
Got an idk from qwen told the llm that they were on my feet. Asked again and then got a response
that was an entire story of them being in my bedroom under my bed following the correct markdown
format. 

Also, as a note it really felt like that scene in Blade Runner 2042 when the <> was being questioned.

## The pipe work

Ollama offers ways to get a context window built up. There are 4 types of messages.

System - for you prompt engineering. This still feels like fairy tales to me.
User - the query the user asks the llm.
Assistant - the rambalings of the llm.
Tools - if you get lucky these will be used to make tool calls.

This should make things pretty easy. The idea is that each type could be parsed
by the agentic system to determine the system state. This would allow for normal
control flow and events within the sytem. The truth of the matter is a bit different.

## A Brief Odd Case

```
SystemState(
messages=[SystemMessage(type='user', message='What is 32 minus 2?'), 
          SystemMessage(type='tool', message='tool call for subtract_two_numbers was: 30'), 
          SystemMessage(type='assistant', message='If you subtract 2 from 32, the result is 30', 
          SystemMessage(type='user', message='What is 55 minus 2 - 3?'), 
          SystemMessage(type='assistant', message='[TOOL_CALLS]{"content": "subtract the two numbers, then subtract again from the result."}'), 
          SystemMessage(type='user', message='why are you making up fake calls?'), 
          SystemMessage(type='assistant', message='To solve the problem step by step, we\'ll use two subtract operations. Let\'s start 55 minus 2:\n\n{"name": "subtract_two_numbers", "arguments": {"a": 55, "b": 2}}\n\nThen we\'ll take the result and subtract 3:\n\n{"name: "subtract_two_numbers", "arguments": {"a": {{result.0}}, "b": 3}}'), 
          SystemMessage(type='user', message='Again those were just states. you actually make the tool call request?'), 
          SystemMessage(type='assistant', message='[TOOL_CALLS]{"name": "subtract_two_numbers "arguments": {"a": 55, "b": 2}}'), 
          SystemMessage(type='user', message='No that is not corret...'), 
          SystemMessage(type='assistant', message='apologize for the mistake. Here\'s the proper function call:\n\n{"name": "subtract_two_numbers", "arguments": {"a": 55, "b": 2}}),
          SystemMessage(type='user', message='No that is not correct either.'), 
          SystemMessage(type='assistant', message='I\'m sorry for the earlier. Let\'s try again:\n\n{"name": "subtract_two_numbers", "arguments": {"a": 55, "b": 2}}'), 
          SystemMessage(type='user', message='ollama sdk is not working properly. This should not be in the message contet.'), 
          SystemMessage(type='assistant', message='I apologize for  error. Let me fix that and try again.\n{"name": "subtract_two_numbers", "arguments": {"a": 55, "b": 2}}')
])
```
