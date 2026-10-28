solver = 1

while (solver >= 1) and (solver <= 3):
    print("Welcome to mod-systems solver.\nSelect an option:\n1 - Linear"
          "\n2 - x^a = b (mod n)\n3 - a^x = b (mod n)\n4 - exit")
    solver = int(input())
    if solver == 1:
        print("This program solves linear congruence equations")
        print("of the form ax + b = c (mod n)")
        a = int(input("Enter a:"))
        b = int(input("Enter b:"))
        c = int(input("Enter c:"))
        n = int(input("Enter n:"))
        print("The smallest solution is ...")
        for i in range(n):
            if (a * i + b) % n == c:
                print(i)
                break
    if solver == 2:
        print("This program solves exponential congruence equations")
        print("of the form x^a = b (mod n)")
        a = int(input("Enter a:"))
        b = int(input("Enter b:"))
        n = int(input("Enter n:"))
        print("The smallest solution is ...")
        for i in range(n):
            if ((i ** a - b) % n) == 0:
                print(i)
                break
    if solver == 3:
        print("This program solves exponential congruence equations")
        print("of the form a^x = b (mod n)")
        a = int(input("Enter a:"))
        b = int(input("Enter b:"))
        n = int(input("Enter n:"))
        print("The smallest solution is ...")
        for i in range(n):
            if ((a ** i - b) % n) == 0:
                print(i)
                break
print("Cya!")