#!/usr/bin/python3
""" Defines the HBnB console"""

import re
import cmd
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(argument):
    curly_braces = re.search(r"\{(.*?)\}", argument)
    brackets = re.search(r"\[(.*?)\]", argument)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(argument)]
        else:
            lexer = split(argument[:brackets.span()[0]])
            token_list = [i.strip(",") for i in lexer]
            token_list.append(brackets.group())
            return token_list
    else:
        lexer = split(argument[:curly_braces.span()[0]])
        token_lst = [i.strip(",") for i in lexer]
        token_list.append(curly_braces.group())
        return token_list


class HBNBCommand(cmd.Cmd):
    """HBNB command interpreter class."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def do_quit(self, arg):
        """Quit the command interpreter."""
        exit()

    def do_EOF(self, arg):
        """EOF"""
        exit()

    def emptyline(self):
        """Handle empty lines by passing."""
        pass

    def do_help(self, arg):
        """Get help on commands."""
        help(self)

    def do_create(self, argument):
        """
        Creates a new class instance of BaseModel and prints its id.
        """
        cli_args = parse(argument)
        if len(cli_args) == 0:
            print("** class name missing **")
        elif cli_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(cli_args[0])().id)
            storage.save()

    def do_show(self, argument):
        """
        Outputs string representation of a class instance
        based on the class name and of id.
        """
        cli_args = parse(argument)
        objdict = storage.all()
        if len(cli_args) == 0:
            print("** class name missing **")
        elif cli_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(cli_args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(cli_args[0], cli_args[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(cli_args[0], cli_args[1])])

    def do_destroy(self, argument):
        """ Deletes an instance based on the class name and id """
        cli_args = parse(argument)
        objdict = storage.all()
        if len(cli_args) == 0:
            print("** class name missing **")
        elif cli_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(cli_args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(cli_arg[0], cli_args[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(cli_args[0], cli_args[1])]
            storage.save()

    def do_all(self, argument):
        """
        Outputs the string representation of all instances
        based or not on the class name
        """
        cli_args = parse(argument)
        if len(cli_args) > 0 and cli_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(cli_args) > 0 and cli_args[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(cli_args) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, argument):
        """
        Gets the number of instances of a given class.
        """
        cli_args = parse(argument)
        count = 0
        for obj in storage.all().values():
            if cli_args[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, argument):
        """ Updates an instance based on the class name and id by adding or updating attribute"""
        cli_args = parse(arg)
        objdict = storage.all()

        if len(cli_arg) == 0:
            print("** class name missing **")
            return False
        if cli_args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(cli_args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(cli_args[0], cli_args[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(cli_args) == 2:
            print("** attribute name missing **")
            return False
        if len(cli_args) == 3:
            try:
                type(eval (cli_args[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(cli_args) == 4:
            obj = objdict["{}.{}".format(cli_args[0], cli_args[1])]
            if cli_args[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__ [cli_args[2]])
                obj.__dict__ [cli_args[2]] = valtype (cli_args[3])
            else:
                obj.__dict__ [cli_args[2]] = cli_args[3]
        elif type(eval (cli_arg[2])) == dict:
            obj = objdict["{}.{}".format(cli_args[0], cli_args[1])]
            for k, v in eval (cli_args[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

if __name__ == "__main__":
    HBNBCommand().cmdloop()
