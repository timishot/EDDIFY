#!/usr/bin/python3
"""Console"""

import cmd
from datetime import datetime
import models
from models.base_model import BaseModel
from models.course import Course
from models.user import User
from models.review import Review
from models.lesson import Lesson
from models.enrollment import Enrollment
from models.category import Category
from models.quiz import Quiz
import shlex


import shlex  # for splitting the line along spaces except in double quotes

classes = {"BaseModel": BaseModel, "User": User, "Lesson": Lesson, "Course": Course, "Quiz": Quiz, "Enrollment": Enrollment, "Review": Review, "Category": Category}

class EDDIFYCommand(cmd.Cmd):
    """ Eddify console """
    prompt = '(eddify) '


    def do_EOF(self, arg):
        """Exists console"""
        return True
	
    def emptyline(self):
        """ overwriting the emptyline method """
        return False
    
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    
    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        new_dict = {}
        argu = ' '.join(args)
        arguments = shlex.split(argu)
        print(arguments)
        for arg in arguments:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if not value.isdigit():
                    value = value
                else:

                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict
    
    def do_create(self, arg):
        """Creates  a new instances of a class"""
        args = arg.split(" ", 1)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](**new_dict)
        else:
            print("** class doesn't exit **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        print(len(args))
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")
    
    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representation of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

if __name__ == '__main__':
    EDDIFYCommand().cmdloop()