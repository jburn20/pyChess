import math, tkinter as tk
class doubleAngles:
    def doublesin(numer: float, denom: float):
        numerans = (numer * 2) * adjacent
        denomerans = denom ** 2
        return numerans, denomerans

    def doublecos(numer: float, denom: float):
        numerans = (denom ** 2) - 2 * (numer ** 2)
        denomerans = denom ** 2
        return numerans, denomerans

    def doubletan(numer: float, denom: float):
        numerans = (numer * 2) * adjacent
        denomerans = (denom ** 2) - 2 * (numer ** 2)
        return numerans, denomerans
if __name__ == "__main__":
    given = input("Enter given trig ratio\n")
    numer: float = float(input("Enter numerator\n"))
    denom: float = float(input("Enter denominator\n"))
    theta = "\u03B8"
    quadrant = input("Enter quadrant: ")
    if given == "sin":
        opposite = numer
        hypotenuse = denom
        adjacent = math.sqrt((hypotenuse ** 2) - (opposite ** 2))
    elif given == "cos":
        adjacent = numer
        hypotenuse = denom
        opposite = math.sqrt((hypotenuse ** 2) - (adjacent ** 2))
    elif given == "tan":
        opposite = numer
        adjacent = denom
        hypotenuse = math.sqrt((adjacent ** 2) + (opposite ** 2))
    print(f"opposite: {opposite}, hypotenuse: {hypotenuse} and adjacent: {adjacent}")
    doublesin = doubleAngles.doublesin(numer, denom)
    doublecos = doubleAngles.doublecos(numer, denom)
    doubletan = doubleAngles.doubletan(numer, denom)
    print(
        f"The double sin angle is: {doublesin}\nThe double cos angle is {doublecos}\nThe double tan angle is: {doubletan}\nRemember the numerator comes first!"
    )