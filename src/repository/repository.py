from typing import Type

from src.domain.validator import Validator, ValidationError


class RepositoryError(BaseException):
    pass

class Repository:
    """ Handles operations on a collection of items. """
    def __init__(self, id_getter, validator):
        self.__collection = {}
        self.__id_get = id_getter
        self.__validator = validator

    def insert_all(self, entities):
        """ Inserts all the elements. If any one of the elements results in an id collision,
            or any one of them fails validation, the collection is not
            modified and an RepositoryError is raised.
        """
        valid = True
        for ent in entities:
            if self.__id_get(ent) in self.__collection:
                raise RepositoryError("One of the bulk-added entities resulted in an id collision")
            try:
                self.__validator.validate(ent)
            except ValidationError:
                raise RepositoryError("One of the bulk-added entities did not pass validation")
        for ent in entities:
            self.insert_or_update(ent)

    def insert_or_update(self, entity):
        """ Inserts a new element, or updates it, if it exists. """
        self.__validator.validate(entity)
        self.__collection[self.__id_get(entity)] = entity

    def id_exists(self, id):
        """ Returns True if an entity with the given id exists. """
        return id in self.__collection

    def find_id(self, id):
        """ Finds and returns the element with the given id, or None. """
        if self.id_exists(id):
            return self.__collection[id]
        return None

    def find_all_by_predicate(self, predicate):
        """ Finds and returns all elements that satisfy the given predicate, in a list. """
        return [x for x in self.__collection.values() if predicate(x)]

    def remove_id(self, id):
        """ Removes the given id. """
        if self.id_exists(id):
            return self.__collection.pop(id)
        return None

    def get_all(self):
        """ Returns all the values of the repo, in a list. """
        return self.__collection.values()
