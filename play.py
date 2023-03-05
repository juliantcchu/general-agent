from general_agent import Agent
from environment import NaiveEnvironment, UserDeterminedEnvironment
import time

# user defined environment at each step
def main1():
    
    history = ['start']
    task = input('what is the task? ')
    Tommy = Agent(task)
    env = UserDeterminedEnvironment()
    currDecision = None

    print('\n --------- \n starting execution loop')
    while history[-1] != 'I am done. ':
        state, action_space = env.act(currDecision)
        if state == 'prompt':
            currDecision = Tommy.prompt(action_space)
        else:
            currDecision = Tommy.decide(action_space, state = state)
        history.append(currDecision )
        print('in play, option picked is', currDecision)

    print('\n --------- \n session ended. the choices made are ', history)


# choosing from NaiveEnvironment
def main2():
    options = [
        'load housing data. ', 
        'get data from yahoo finance. ', 
        'get twitter data. ', 
        'preprocess data. ', 
        'train a decision tree on the data. ',
        'train a linear regression model on the data. ', 
        'train a time-series LSTM on the data. ', 
        'I am done. '
    ]
    print('\n --------- \n options', options)

    history = ['start']

    Tommy = Agent('predict housing prices. ')
    env = NaiveEnvironment(options)
    currDecision = None

    print('\n --------- \n starting execution loop')
    
    while history[-1] != 'I am done. ':
        time.sleep(10)
        state, action_space = env.act(currDecision)
        currDecision = Tommy.decide(action_space, state = state)
        history.append(options[currDecision])
        print('in play, option picked is', options[currDecision])

    print('\n --------- \n session ended. the choices made are ', history)

if __name__ == '__main__':
    main1()