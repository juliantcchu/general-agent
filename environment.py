

class NaiveEnvironment:

    choices = []

    def __init__(self, options):
        self.options = options

        

    def act(self, decision):

        if decision == None:
            return 'What would be your first step? ', self.options # started

        
        self.choices.append(decision)

        # returns new state description and new possible actions
        # in the naive environment, new state description is the action perforemed at last step
        # and the possible actions are the same at each step
        return 'You decided to ' + self.options[decision] + '. What do you wwant to do next?', self.options


class UserDeterminedEnvironment:

    choices = []

    def __init__(self):
        self.options = input('what are the choices? seperate using ";" : ').split(';')

        

    def act(self, decision):

        if decision == None:
            return 'What would be your first step? ', self.options # started

        
        self.choices.append(decision)

        self.state = input('new state description: ')
        _options = input('what are the new options? seperate using ";" : ').split(';')

        if _options[:7] == 'prompt:'
            return 'prompt', _options[7:]

        self.options = _options.split(';')
        # returns new state description and new possible actions
        # in the naive environment, new state description is the action perforemed at last step
        # and the possible actions are the same at each step
        return 'You decided to ' + self.options[decision] + '. ' + self.state + ' What do you wwant to do next?', self.options