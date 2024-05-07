from .abstract_logs import AbstractLogger
# Example usage

logger = AbstractLogger('module1', 'module1.log')

def main():
    logger.log("info", "This is an info message")
    try:
        # Your code here
        raise ValueError("This is a test error")
    except Exception as e:
        logger.log("error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
