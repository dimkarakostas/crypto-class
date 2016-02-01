from exercises.registry import register_grader

def validate(metadata, input_pass):
    """
    Check if private-key in metadata matches the user input
    """
    is_solution = True if metadata['private-key'] == input_pass else False
    return (is_solution, None)

register_grader('14.0', validate)
