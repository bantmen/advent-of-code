s = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""

s = open("day4.txt").read()

l = s.split("\n")

required = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

num_valid = 0

import re


def valid_value(field, val):
    if field == "byr":
        return "1920" <= val <= "2002"
    if field == "iyr":
        return "2010" <= val <= "2020"
    if field == "eyr":
        return "2020" <= val <= "2030"
    if field == "hgt":
        if val.endswith("cm"):
            return "150" <= val.split("cm")[0] <= "193"
        if val.endswith("in"):
            return "59" <= val.split("in")[0] <= "76"
        return False
    if field == "hcl":
        return re.search("#[0-9a-f]{6}", val) is not None
    if field == "ecl":
        return val in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
    if field == "pid":
        return len(val) == 9 and re.search("[0-9]{9}", val) is not None
    if field == "cid":
        return True
    return False


def valid(cur):
    req = set(required)
    for line in cur:
        for x in line.split(" "):
            field, val = x.split(":")
            if field not in req:
                if field == "cid":
                    continue
                else:
                    assert False
            if valid_value(field, val):
                req.remove(field)
    return len(req) == 0


cur = []
for line in l:
    if line != "":
        cur.append(line)
    else:
        if valid(cur):
            num_valid += 1
        cur = []

if valid(cur):
    num_valid += 1

print(num_valid)
