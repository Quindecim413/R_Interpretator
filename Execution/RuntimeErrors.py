class RuntimeError(Exception):
    def __init__(self, message):
        super(RuntimeError, self).__init__(message)
        self.message = message


class ObjectNotFound(RuntimeError):
    def __init__(self, obj_name):
        super(ObjectNotFound, self).__init__('Error: object \'{}\' not found'.format(obj_name))


class ObjectNotSubSettable(RuntimeError):
    def __init__(self, obj_name):
        super(ObjectNotSubSettable, self).__init__('Error: object \'{}\' not subsettable'.format(obj_name))


class NoLoop(RuntimeError):
    def __init__(self):
        super(NoLoop, self).__init__('Error: no loop for break/next, jumping to top level')


class FailedToFindFunction(RuntimeError):
    def __init__(self, func_name):
        super(FailedToFindFunction, self).__init__('could not find function "{}"'.format(func_name))


class DLRAppliedNotToSubsettable(RuntimeError):
    def __init__(self, name):
        super(DLRAppliedNotToSubsettable, self).__init__('Error in ${} : object of type "closure" is not subsettable'
                                                         .format(name))


class ArgNotInterpretableAsLogical(RuntimeError):
    def __init__(self):
        super(ArgNotInterpretableAsLogical, self).__init__("Error: argument is not interpretable as logical")


class UnexpectedPlainAssignment(RuntimeError):
    def __init__(self):
        super(UnexpectedPlainAssignment, self).__init__("Error : unexpected = assignment")


class UnexpectedSimpleAssignment(RuntimeError):
    def __init__(self):
        super(UnexpectedSimpleAssignment, self).__init__("Error : unexpected <- assignment")


class UnexpectedSuperAssignment(RuntimeError):
    def __init__(self):
        super(UnexpectedSuperAssignment, self).__init__("Error : unexpected <<- assignment")


class UnusedArguments(RuntimeError):
    def __init__(self, args_count):
        super(UnusedArguments, self).__init__("Error : unused arguments - {}".format(args_count))
