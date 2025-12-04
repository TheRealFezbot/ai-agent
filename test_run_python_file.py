from functions.run_python_file import run_python_file

def main():

    # Should print calculator's usage instructions
    result = run_python_file("calculator", "main.py")
    print("Result:\n" + result + "\n")

    # Should run the calculator.. which gives a kindof nasty result
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result:\n" + result + "\n")

    # Should run the calculator's tests successfully
    result = run_python_file("calculator", "tests.py")
    print("Result:\n" + result + "\n")

    # Should return a work directory error
    result = run_python_file("calculator", "../main.py")
    print("Result:\n" + result + "\n")

    # Should return a nonexistent file error
    result = run_python_file("calculator", "nonexistent.py")
    print("Result:\n" + result + "\n")

    # Should return a 'not a python file' error
    result = run_python_file("calculator", "lorem.txt")
    print("Result:\n" + result + "\n")

if __name__ == "__main__":
    main()