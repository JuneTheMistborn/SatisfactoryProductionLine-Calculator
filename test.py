string = "19.9679534"

verify = lambda s: False if s.islower() or s.isupper()\
    else f"{(round(float(s), 4)):.4f}" + "%" if 250 >= float(s) >= 0 else False

print(verify(string))

