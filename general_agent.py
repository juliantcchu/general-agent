import openai
import re

# openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ]
# )
openai.api_key = "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" #"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"

class Agent:

    # llm_api_key = ''
    choice_log = []

    def __init__(self, task, log_prcess=True, preplanning=False):
        # initialize variables
        self.task = task
        self.log_prcess = log_prcess

        self.context = "You are a decision engine that picks which action to perform from the options given to you. At each step, the user will give you multiple choices of actions you can perform. " \
            + "Choose one action each time and give one word answers such as 'Option (1)' or Option (2). \n The task you are given is: " + task #+ '. \n This is your plan: ' + self.plan



        # get a high level plan from LLM if preplanning=True
        if preplanning:
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant. "},
                    {"role": "user", "content": task + ". Create a plan on what you will do. "},
                ]
            )
            self.plan = completion['choices'][0]['message']['content']
            self.context += '\n This is your plan: ' + self.plan
            if self.log_prcess:
                print('\n --------- \n basic plan: \n', self.plan)


        self.history = [
            {"role": "system", "content": self.context}
        ]

    def decide(self, action_space, state = ''):
        # using LLM as a decision enginer, choose one action over a discrete action space, 
        # represented as a list of text description of actions. e.g. ['turn right', 'turn left']
        # returns the integer corresponding to the index of the action in the input list
        # might work better if state speicifies what action the model took and what happened as a result. 
        
        prompt = 'Here are your options:'
        options = []
        for i, action in enumerate(action_space):
            options.append('Option(' + str(i) + '): ' + action)
        prompt += ' \n ' + ' \n '.join(options)

        if self.log_prcess:
            print('\n --------- \nprompt: ', state + prompt)
        
        self.history.append({
            'role': 'user', 
            'content': state + prompt
        })

        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=self.history
        )

        self.history.append(
            completion['choices'][0]['message']
        )
        
        if self.log_prcess:
            print('\n --------- \nAI response: ', completion['choices'][0]['message'])

        response = completion['choices'][0]['message']['content']
        
        choice = self.detect_choice(response)

        self.choice_log.append(choice)

        return choice

    def prompt(self, query):
        # ask llm to return a string output given a specific query

        self.history.append({
            'role': 'user', 
            'content': query + 'For this query only, your answer could be a word or a sentence. '
        })

        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=self.history
        )

        self.history.append(
            completion['choices'][0]['message']
        )

        return completion['choices'][0]['message']

    def detect_choice(self, text):
        # assuming model return something like 'Option (1)', this function extract the integer '1' from the text
        return int(re.search(r'\d+', text).group())

    def classification(self, text, choices):
        # perform zero shot text classification using embedding similarity
        # TODO

        return 0