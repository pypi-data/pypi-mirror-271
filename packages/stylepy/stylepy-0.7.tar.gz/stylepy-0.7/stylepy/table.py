
def tabular_list(data, col_widths = [15, 45], returnValue = False):
    """
    Print data in a tabular format with horizontal lines, differentiating the header.

    :param data: List of tuples, where each tuple represents a row.
    :param col_widths: List of integers representing the width of each column.
    """
    def divider():
        # Create and print a divider line with '+'
        line = "+" + "+".join("-" * width for width in col_widths) + "+"
        print(line)

    def header_divider():
        # Create and print a simple divider line without '+' for the header
        line = "-" * (sum(col_widths) + len(col_widths) - 1)
        print(line)

    # Print the header row
    divider()
    header = data[0]
    formatted_header = "|".join(
        f"{item:<{col_widths[i]}}" for i, item in enumerate(header))
    print("|" + formatted_header + "|")
    header_divider()

    # Print the rest of the rows
    for row in data[1:]:
        formatted_row = "|".join(
            f"{item:<{col_widths[i]}}" for i, item in enumerate(row))
        print("|" + formatted_row + "|")
        header_divider()
