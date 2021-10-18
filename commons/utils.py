from typing import List


class ClassUtils:
    """
    Utilities for classes. Red the docs of each method.
    """

    @staticmethod
    def get_class_instance_properties_as_dict(class_instance: object = None,
                                              return_properties: List = None) -> dict:
        """
        This method give you a class properties using their dict representation

        :param class_instance: a class instance, for example a queryset
        :param return_properties: the properties to find in the class
        :return: a dict
        """
        try:
            class_instance.__dict__
        except:
            return {}
        return {key: value for key, value in class_instance.__dict__.items()
                if key in return_properties and value is not None}
