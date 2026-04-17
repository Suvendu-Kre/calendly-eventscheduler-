def validate_input(input_text: str) -> str:
    """
    Validates the input to ensure it's not malicious or harmful.
    For now, just checks for empty input.
    """
    return input_text.strip() if input_text and input_text.strip() else "Error: Input cannot be empty."

def validate_output(output: str) -> str:
    """
    Validates the output to ensure it meets certain criteria.
    For now, just checks that the output is non-empty.
    """
    return output.strip() if output and output.strip() else "Error: Empty response."