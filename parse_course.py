class Course():
    __init__():
        self.modules = [] # List of Module objects
    
class Module():
    __init__():
        self.name = 'module name'
        self.patth = 'path'
        self.lessons = [] # list of Lesson object
        self.isChoose = True

class Lesson():
    __init__(module):
        self.name = 'lesson name'
        self.path = '<module path>/path'
        self.lessons = [] # list of Step object

        # True if module parent is choosen
        if module.isChoose:
            self.isChoose = True 
        else:
            self.isChoose = False

class Step():
    __init__(lesson):
        self.name = 'step name'
        self.path = '<lesson path>/path'
        self.type = 'number' # string, choise, ...

        # True if module parent is choosen
        if lesson.isChoose:
            self.isChoose = True 
        else:
            self.isChoose = False