# Desired Coding Style

I'm thinking I want to figure out how to extend the `Continue` tool with tools of my own. I will have the AI build the tools for me. However, I'm learning that it's very easy for machines to lose context of what's happened within the past. They can hallucinate heavily, and can miss a lot of important context for which causes a burn of energy. They can also code almost entirely outside of my desired standards. Therefore, I want to have a document that has my desired coding style so I can feed the document to a LLM and have it enforce the style. This will be a growing document. I'll likely start placing it inside of my notion or something of the like.

## Final Coding Style - Before AI Takes Over!

The rules can mostly follow black and ruff in terms of linting anf formatting. However, I want to add a few rules of my own. That's primarily regarding the order of imports, class definitions, and function definitions. I want to have the imports at the top of the file, followed by the class definitions. 

1. Before running code, I setup a `main` function that runs the code. This is the entry point of the code. Might have them throughout a project to run different parts of the code before writting tests.
2. I've come to realize that it helps to write down what you aim to achieve and a series of steps to get there. This is the `TODO` list. I want to have a `TODO` list at the top of the file that describes what the code is supposed to do.
   1. I want to have a `TODO` list at the top of the file that describes what the code is supposed to do.
   2. I also want to have todo items throughout the code that describe what the code is supposed to eventually do. This will be done using comments. It's also transferrable to jupyter notebooks, as you could use markdown cells to describe what the code is supposed to do.
3. Once the first few tasks are determined, I'm learning it's better to write classes that will contain most of the work contain then slowly fill the code in. The first steps of the `TODO` list will likely go into the same class. As we fill in the code we can refactor the code to make it more modular, and easier to read. We would incorporate encapsulation, inheritance, and polymorphism as needed. We can also use OOP principles to make the code more readable and maintainable like SOLID principles or design patterns. I'm not forgetting functional patterns. Will need to get more into that.


## Project Planning

1. Think of input
2. Think of output
3. Create a few samples between the inputs and outputs
   1. Think of it like crossing a bridge. When you cross the bridge you have some sort of benefit that you didn't have before. You can think of the bridge as the code you're writing. The inputs are the things you have before you cross the bridge. The outputs are the things you have after you cross the bridge. The samples are the things you can do with the outputs that you couldn't do with the inputs.
4. Think of a few steps/plan to get from the inputs to the outputs
5. Design beginning systems
6. Design your data
7. Define your metrics for success
8. Collect preliminaty data and systems
9. Compile by writing code and using agents (Like Devika or Devin)
10. Test and refine
11. Repeat steps 9 and 10 until you have a working system

If I have an agent, I would ensure they agent knew how to help me remain clear about this. Over time, it should be clear which bridges I'm attempting to cross when doing almost any action.

## Code Organization

I have a particular way I like to organize my code. I like to have the imports at the top of the file, followed by the class definitions, then the function definitions. I like to have the `main` function at the bottom of the file to adhoc run code within that file. Tests are hard to put into place, though they might help one become certain about the desired outcome.


### Sorting

**Snippet from [`ssort`](https://github.com/bwhmather/ssort) documentation:**

Sorts the contents of python modules so that statements are placed after the things they depend on, but leaves grouping to the programmer. Groups class members by type and enforces topological sorting of methods.

Makes old fashioned code navigation easier, you can always scroll up to see where something is defined, and reduces bikeshedding.

Compatible with and intended to complement isort and black.


**Before:**
    
```python
from module import BaseClass

def function():
    return _dependency()

def _decorator(fn):
    return fn

@_decorator
def _dependency():
    return Class()

class Class(BaseClass):
    def public_method(self):
        return self

    def __init__(self):
        pass
```

**After:**

```python
from module import BaseClass

class Class(BaseClass):
    def __init__(self):
        pass

    def public_method(self):
        return self

def _decorator(fn):
    return fn

@_decorator
def _dependency():
    return Class()

def function():
    return _dependency()
```


Now the order of the code. It's the result of the `ssort` tool. I like the way it's organized. It's easier to read and understand. I can see the class definition, then the function definitions. I can see the dependencies of the functions. It's a good way to organize code. I like it.


## Python Code Style

I have things that I like to do in Python. 

### Classes

1. I like to use classes to store data and methods that operate on that data together.
2. I mostly like to use BaseModel from pydantic to define the data that goes into the class. It forces me to think about constraints and validation.
3. I also like making modifier classes that return modifiers using the `@staticmethod` decorator. This is a way to make the class more modular and easier to test.
4. I prefer dependency injection, though it's difficult to pull off in real life.
   1. It's possible to use callables as dependency injection. It doesn't need to be an entire class.
   2. Actually, I liked the `torch` way of doing dependency injection. It held a registry of all Modules and could call them by name. This is a good way to do dependency injection.


### Example


![Dependency Injection With DsPy](./imgs/good-oop.png)

The class that the developer creates has very clear steps that are being followed through the entire codebase. There are a few cases of dependency injections here. The first is with the `__init__` method. The developer adds a function for grounding the code samples he's generating. He's also injecting the `resolve_function` and `resolve_reactions`. The resolve_function is going into the resolve_reactions function. 

This injection allows the developer to change the functionality dynamically, and run experiments with the code by going through a list of possible functions.


Most of all, I like that the logic is within a contained space. **You know what the code is supposed to do within a small numbers of lines**, even if the rest of the code is verbose.


### Folders & File Structure

1. Keep the code flat for as long as possible.
2. Only when the code gets too big, split it into folders.
3. Keep utilities in a `utils.py` file. Keep it organized as one file for as long as possible.
4. Have an abstracts file that has all of the interfaces for the classes within the projects. This is a good way to keep track of what the classes are supposed to do.
5. There should be a core file that has the main classes that are used throughout the project. Put all data classes (objects that primarily hold data) into one folder. The data classes should be minimally divided up. 
6. Have a **`config.py`** file that has all of the configurations for the project. It should be responsible for dictating file paths, passwords, default user names, passwords, etc. This is a good way to keep track of what the configurations are supposed to do. I like to use **`pydantic-settings`** for this. I break-up configuration into multiple parts while keeping them within the same file.
   1. The files themselves are amended able to things like environment variables and command line arguments. This is a good way to keep track of what the configurations are supposed to do.

**AVOID!!! What to avoid in the codebase:**

1. Having multiple locations for a given task (i.e, config, database, `__main__`, 'errors', utils, etc.)
2. Comment out too much code.
   1. It start's to build up over time.
   2. It's possible to have config options and feature flags as a way to keep track of what the code is supposed to do.
3. Having too many classes in a single file.
4. Having too many functions in a single class.
5. Having too many dependencies in a single class.
6. Getting code disorganized.