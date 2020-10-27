#!/usr/bin/env python3

class EvaluationItem():
    '''
    class to hold information about each part of the blueprint
    as it is evaluated
    '''

    def __init__(self, eval_criteria: dict):
        '''
        class constructor
        here we are setting up the evaluation criteria object
        '''
        self.eval_type = eval_criteria["eval_type"]
        self.match_type = eval_criteria["match_type"]
        self.description = eval_criteria["description"]
        self.criteria = eval_criteria["criteria"]
        self.expected = eval_criteria["expected"]

    def __repr__(self):
        '''
        decent __repr__ for debuggability
        this is something recommended by Raymond Hettinger
        '''
        return (f'{self.__class__.__name__}(eval_type={self.eval_type},'
                f'match_type={self.match_type},'
                f'description={self.description},'
                f'criteria={self.criteria},'
                f'expected={self.expected}')
