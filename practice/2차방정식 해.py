import cmath

a = int(input("Enter a : "))
b = int(input("Enter b : "))
c = int(input("Enter c : "))

d = (b**2) - (4*a*c)

sol1 = (-b-cmath.sqrt(d))/(2*a)
sol2 = (-b+cmath.sqrt(d))/(2*a)

if cmath.sqrt(d) == 0j:
    sol1 = (-b)/(2*a)
    sol2 = (-b)/(2*a)
    print('The solution are ', sol1,' and ', sol2)

else:
    sol1 = (-b-cmath.sqrt(d))/(2*a)
    sol2 = (-b+cmath.sqrt(d))/(2*a)
    print('The solution are {0} and {1}'.format(sol1, sol2))