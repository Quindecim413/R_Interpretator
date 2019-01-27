class R_RuntimeError(Exception):
    def __init__(self, message, args=list()):
        super(R_RuntimeError, self).__init__(message)
        self.message = message
        self.args = args




class ObjectNotFound(R_RuntimeError):
    def __init__(self, obj_name):
        super(ObjectNotFound, self).__init__('Error: object \'{}\' not found'.format(obj_name))


class ObjectNotSubSettable(R_RuntimeError):
    def __init__(self, obj):
        super(ObjectNotSubSettable, self).__init__('object of type {} not subsettable'.format(obj.get_type()))


class ClosureNotSubSettable(R_RuntimeError):
    def __init__(self):
        super(ClosureNotSubSettable, self).__init__('object of type closure not subsettable')


class InvalidLeftHandAssignment(R_RuntimeError):
    def __init__(self):
        super(InvalidLeftHandAssignment, self).__init__('invalid (do_set) left-hand side to assignment')


class InvalidRightHandAssignment(R_RuntimeError):
    def __init__(self):
        super(InvalidRightHandAssignment, self).__init__('invalid (do_set) right-hand side to assignment')


class ApplyToNonFunction(R_RuntimeError):
    def __init__(self):
        super(ApplyToNonFunction, self).__init__('attempt to apply non-function')


class NoLoop(R_RuntimeError):
    def __init__(self):
        super(NoLoop, self).__init__('no loop for break/next, jumping to top level')


class FailedToFindFunction(R_RuntimeError):
    def __init__(self, func_name):
        super(FailedToFindFunction, self).__init__('could not find function "{}"'.format(func_name))


class DLRAppliedNotToSubsettable(R_RuntimeError):
    def __init__(self, name):
        super(DLRAppliedNotToSubsettable, self).__init__('Error in ${} : object of type "closure" is not subsettable'
                                                         .format(name))


class ArgNotInterpretableAsLogical(R_RuntimeError):
    def __init__(self):
        super(ArgNotInterpretableAsLogical, self).__init__("Error: argument is not interpretable as logical")


class UnexpectedPlainAssignment(R_RuntimeError):
    def __init__(self):
        super(UnexpectedPlainAssignment, self).__init__("Error : unexpected = assignment")


class UnexpectedSimpleAssignment(R_RuntimeError):
    def __init__(self):
        super(UnexpectedSimpleAssignment, self).__init__("Error : unexpected <- assignment")


class UnexpectedSuperAssignment(R_RuntimeError):
    def __init__(self):
        super(UnexpectedSuperAssignment, self).__init__("Error : unexpected <<- assignment")


class UnusedArguments(R_RuntimeError):
    def __init__(self, arg):
        super(UnusedArguments, self).__init__("Error : unused argument - {}".format(arg.show_self()))


class ArgumentMissingWithNoDefualt(R_RuntimeError):
    def __init__(self, arg_name):
        super(ArgumentMissingWithNoDefualt, self).__init__("argument \"{}\" is missing with no default".format(arg_name))


class InvalidArgTypeInArgs(R_RuntimeError):
    def __init__(self, invalid_arg_name, where_repr):
        super(InvalidArgTypeInArgs, self).__init__('invalid \'{}\' type in \'{}\''.format(invalid_arg_name, where_repr))


class InvalidArgType(R_RuntimeError):
    def __init__(self):
        super(InvalidArgType, self).__init__('invalid argument type')


class NonNumericToBinary(R_RuntimeError):
    def __init__(self):
        super(NonNumericToBinary, self).__init__('non-numeric argument to binary operator')


class ArgumentCannotBeHandledByFun(R_RuntimeError):
    def __init__(self, arg_pos, arg_type, fun_name):
        super(ArgumentCannotBeHandledByFun, self).__init__('argument {} (type \'{}\') cannot be handled by \'{}\''
                                                         .format(arg_pos, arg_type, fun_name))

class InvalidArg(R_RuntimeError):
    def __init__(self, arg_name):
        super(InvalidArg, self).__init__("invalid '{}' argument".format(arg_name))
