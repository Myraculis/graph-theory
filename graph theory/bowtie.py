import math

def calculate_gamma(x, n):
    # Calculate the exponent values
    exponent1 = (n - 1) / 2
    exponent2 = math.ceil((n - 1) / 4)

    # Calculate the powers of x
    x1 = x ** exponent1
    x2 = x ** exponent2

    # Calculate the combination part
    combination_value = (x1 - x2) / 2

    # Calculate the binomial coefficient
    binomial_coefficient = combination_value * (combination_value - 1) / 2

    # Calculate the gamma value
    gamma_value = x * binomial_coefficient

    return gamma_value

def main():
    # Prompt the user for input
    x = float(input("Enter the value of x: "))
    n = int(input("Enter the value of n (must be odd): "))

    # Ensure n is odd
    if n % 2 == 0:
        print("The value of n must be odd.")
        return

    # Calculate and display the result
    result = calculate_gamma(x, n)
    print(f"The value of gamma(x, B_n) is: {result}")

if __name__ == "__main__":
    main()
