class Job:
    def __init__(self):
        self.job_workflow_invocation = None
        # Initialize other job properties

class JobStep:
    def __init__(self, number, name=None, state=None, output=None):
        self.number = number
        self.name = name
        self.state = state
        self.output = output or []
