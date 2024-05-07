from pydantic import BaseModel

class AgentBaseModel(BaseModel):
    pass

    
def agent(cls):
    # Check if the class already inherits from AgentBaseModel
    if not issubclass(cls, AgentBaseModel):
        # If not, create a new class that is the same as cls but also inherits from AgentBaseModel
        class NewClass(cls, AgentBaseModel):
            pass
        
        # Update the class dictionary to include all attributes from cls
        NewClass.__module__ = cls.__module__
        NewClass.__name__ = cls.__name__
        NewClass.__qualname__ = cls.__qualname__
        NewClass.__annotations__ = cls.__annotations__.copy()
        
        # Enhance the __init__ method to add logging
        original_init = cls.__init__
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            print(f"{self.__class__.__name__} initialized with {self.dict()}")
        NewClass.__init__ = new_init

        return NewClass
    
    else:
        # If cls already inherits from AgentBaseModel, just add logging
        original_init = cls.__init__
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            print(f"{self.__class__.__name__} initialized with {self.dict()}")
        cls.__init__ = new_init
        return cls

# Example usage
@agent
class User(AgentBaseModel):
    name: str
    age: int

user = User(name="Alice", age=20)
