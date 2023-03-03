"""
Function Decorator Module
"""

class DatabaseDecorator:
    """
    Helper decorator class for universal decorators
    """
    # Decorator for validating database insert methods
    @staticmethod
    def validate_insert(required_fields):
        """
        Python decorator function to validate objects before they are inserted
        into the database.

        Usage:
            Before any method that inserts data into the database, you should
            decorate the method as such:

            @validate_insert(required_fields = TABLE_XXXX_FIELDS)

            In the above, `TABLE_XXXX_FIELDS` should be the class constant variable
            containing a list of the required fields for the table to be inserted
            into.

        Note:
            This method does not prevent inserting duplicate values for unique
            fields. The insert method body should still enforce uniqueness
            where appropriate.
        """

        def decorator(func):
            def wrapper(self, *args):
                if (
                    isinstance(args[0], dict)
                    and all(field in args[0].keys() for field in required_fields)
                    and len(args[0].keys()) == len(required_fields)
                ):
                    return func(self, *args)
                return False  # Indicates validation failure

            return wrapper

        return decorator
