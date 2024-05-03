from typing import Union, Callable
import ast


SafeType = Union[str, int, float, complex, list, tuple, set, dict, bool, bytes, None]


def safe_eval(
    expression: ast.expr, /,
    variables: dict[str, SafeType] = None,
    functions: dict[str, Callable] = None,
) -> SafeType:
    """Recursively evaluate expressions."""

    match expression:
        # Constant
        case ast.Constant():
            if type(expression.value) not in SafeType.__args__:
                raise TypeError(f'Unsafe value type: {type(expression.value).__name__}')
            return expression.value

        # Variable
        case ast.Name():
            try:
                value = variables[expression.id]
                if type(value) not in SafeType.__args__:
                    raise TypeError(f'Unsafe value type: {type(value).__name__}')
                return value
            except KeyError:
                raise NameError(f'Name {expression.id!r} cannot be found in variables.')

        # Collections
        case ast.List():
            return list(safe_eval(e, variables, functions) for e in expression.elts)
        case ast.Tuple():
            return tuple(safe_eval(e, variables, functions) for e in expression.elts)
        case ast.Set():
            return set(safe_eval(e, variables, functions) for e in expression.elts)
        case ast.Dict():
            return dict({
                safe_eval(key, variables, functions): safe_eval(value, variables, functions)
                for key, value in zip(expression.keys, expression.values)
            })

        case ast.UnaryOp():
            operand = safe_eval(expression.operand, variables, functions)

            match expression.op:
                case ast.UAdd():
                    return +operand
                case ast.USub():
                    return -operand
                case ast.Invert():
                    return ~operand
                case ast.Not():
                    return not operand
                case _:
                    raise TypeError(f'Unsupported operator type: {type(expression.op).__name__}')

        case ast.BinOp():
            left = safe_eval(expression.left, variables, functions)
            right = safe_eval(expression.right, variables, functions)

            match expression.op:
                # Arithmetic
                case ast.Add():
                    return left + right
                case ast.Sub():
                    return left - right
                case ast.Mult():
                    return left * right
                case ast.MatMult():
                    return left @ right
                case ast.Div():
                    return left / right
                case ast.FloorDiv():
                    return left // right
                case ast.Mod():
                    return left % right
                case ast.Pow():
                    return left ** right
                    
                # Bit operations
                case ast.BitAnd():
                    return left & right
                case ast.BitOr():
                    return left | right
                case ast.BitXor():
                    return left ^ right
                case ast.LShift():
                    return left << right
                case ast.RShift():
                    return left >> right

                case _:
                    raise TypeError(f'Unsupported operator type: {type(expression.op).__name__}')

        case ast.Compare():
            left = safe_eval(expression.left, variables, functions)
            comparators = [left, *expression.comparators]

            for i, (operator, left) in enumerate(zip(expression.ops, comparators)):
                right = safe_eval(comparators[i + 1], variables, functions)
                comparators[i + 1] = right

                match operator:
                    # Comparison
                    case ast.Eq():
                        if left == right:
                            continue
                        return False
                    case ast.NotEq():
                        if left != right:
                            continue
                        return False
                    case ast.Gt():
                        if left > right:
                            continue
                        return False
                    case ast.Lt():
                        if left < right:
                            continue
                        return False
                    case ast.GtE():
                        if left >= right:
                            continue
                        return False
                    case ast.LtE():
                        if left <= right:
                            continue
                        return False

                    # Identity
                    case ast.Is():
                        if left is right:
                            continue
                        return False
                    case ast.IsNot():
                        if left is not right:
                            continue
                        return False

                    # Membership
                    case ast.In():
                        if left in right:
                            continue
                        return False
                    case ast.NotIn():
                        if left not in right:
                            continue
                        return False

                    case _:
                        raise TypeError(f'Unsupported operator type: {type(operator).__name__}')
            else:
                return True

        case ast.BoolOp():
            match expression.op:
                # Logical
                case ast.And():
                    return all(safe_eval(value, variables, functions) for value in expression.values)
                case ast.Or():
                    return any(safe_eval(value, variables, functions) for value in expression.values)
                case _:
                    raise TypeError(f'Unsupported operator type: {type(expression.op).__name__}')

        # Function
        case ast.Call():
            try:
                function = functions[expression.func.id]
            except KeyError:
                raise NameError(f'Name {expression.func.id!r} cannot be found in functions.')

            args = [safe_eval(x, variables, functions) for x in expression.args]
            kwargs = {
                keyword.arg: safe_eval(keyword.value, variables, functions)
                for keyword in expression.keywords
            }

            return function(*args, **kwargs)
            
        case _:
            raise TypeError(f'Unsupported expression type: {type(expression).__name__}')



def sheval(
    expression: str, /,
    variables: dict[str, SafeType] = None,
    functions: dict[str, Callable] = None,
) -> SafeType:
    """Safely evaluate expression. Only evaluate whitelisted types."""

    tree = ast.parse(expression, mode='eval')
    
    if not isinstance(tree, ast.Expression):
        raise TypeError('Something went wrong. Expected an `ast.Expression`.')
    return safe_eval(tree.body, variables or {}, functions or {})
