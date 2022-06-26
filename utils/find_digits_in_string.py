
def digits_of_string(input_string=None):
    output = ''
    if input_string:
        output = output + ''.join(c for c in input_string if c.isdigit())
    return output
