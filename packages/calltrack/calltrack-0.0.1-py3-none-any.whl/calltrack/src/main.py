from decorators import jsonlog
from log_writer import JSONLogWriter, LogQueue

queue = LogQueue(name="main")
writer = JSONLogWriter(log_queue=queue, save_dir="logit/logs/", autoflush=True)


@jsonlog(writer=writer)
def add(a, b):
    """Add two numbers."""
    return a + b


@jsonlog(writer=writer)
def subtract(a, b):
    """Subtract two numbers."""
    return a - b


@jsonlog(writer=writer)
def multiply(a, b):
    """Multiply two numbers."""
    return a * b


@jsonlog(writer=writer)
def divide(a, b):
    """Divide two numbers."""
    if b != 0:
        return a / b
    else:
        return "Error: Division by zero is not allowed."


@jsonlog(writer=writer)
def calculate_area(length, width):
    """Calculate the area of a rectangle."""
    return multiply(length, width)


def main():
    # Example usage of the functions
    print("Addition:", add(5, 3))
    print("Subtraction:", subtract(10, 4))
    print("Multiplication:", multiply(2, 7))
    print("Division:", divide(20, 5))

    # Calculate the area of a rectangle
    length = 5
    width = 4
    area = calculate_area(length, width)
    print(f"The area of a rectangle with length {length} and width {width} is {area}.")

    writer.flush()


if __name__ == "__main__":
    main()
