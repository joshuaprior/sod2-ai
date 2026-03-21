class classproperty:
    '''Creates a class-level property that can be accessed without instantiating the class.'''
    def __init__(self, fget):
          self.fget = fget

    def __get__(self, owner_instance, owner_cls):
        return self.fget(owner_cls)