import base64
import zlib
import inspect

def encode_string_to_base64(input_string):
    """
    Encodes a string to base64 format.

    Args:
        input_string (str): The string to be encoded.

    Returns:
        str: The base64 encoded string.
    """
    if not input_string.endswith('\n'):
        input_string += '\n'
    input_bytes = zlib.compress(
        input_string.encode('utf-8'), level=9, wbits=16 + 15)
    base64_bytes = base64.b64encode(input_bytes)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string


def generate_function_code(func):
    source_code = inspect.getsource(func)
    func_name = func.__name__
    output = f"""
{source_code}
{func_name}()
    """
    return output

def get_caller_filename():
    return inspect.stack()[-1].filename