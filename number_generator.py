
# -*- coding: utf-8 -*-

# mukera 1 2 3
# mukera 1 2 3

ByOne = [
"ዜሮ",
"አንድ",
"ሁለት",
"ሶስት",
"አራት",
"አምስት",
"ስድስት",
"ሰባት",
"ስምንት",
"ዘጠኝ",
"አስር",
"አስራ አንድ",
"አስራ ሁለት",
"አስራ ሶስት",
"አስራ አራት",
"አስራ አምስት",
"አስራ ስድስት",
"አስራ ሰባት",
"አስራ ስምንት",
"አስራ ዘጠኝ"
]

ByTen = [
"ዜሮ",
"አስር",
"ሃያ",
"ሰላሳ",
"አርባ",
"ሃምሳ",
"ስልሳ",
"ሰባ",
"ሰማንያ",
"ዘጠና"
]

zGroup = [
"",
"ሺህ",
"ሚሊዮን",
"ቢሊዮን",
"ትሪሊዮን",
"ኳድሪሊዮን"
]


def subThousand(n):
    assert(isinstance(n,(int, int)))
    assert(0 <= n <= 999)
    if n <= 19:
        return ByOne[n]
    elif n <= 99:
        q, r = divmod(n, 10)
        return ByTen[q] + (" " + subThousand(r) if r else "")
    else:
        q, r = divmod(n, 100)
        return ByOne[q] + " መቶ" + (" " + subThousand(r) if r else "")


def thousandUp(n):
    assert(isinstance(n,(int, int)))
    assert(0 <= n)
    return ", ".join(reversed([subThousand(z) + (" " + zGroup[i] if i else "") if z else "" for i,z in enumerate(splitByThousands(n))]))


def splitByThousands(n):
    assert(isinstance(n,(int, int)))
    assert(0 <= n)
    res = []
    while n:
        n, r = divmod(n, 1000)
        res.append(r)
    return res


def get_number_as_words(n):
  assert(isinstance(n,(int, int)))
  if n==0:
    return "ዜሮ"
  return ("Minus " if n < 0 else "") + thousandUp(abs(n))


# def main():
#   pass
#   # n = int(raw_input("Please enter an integer:\n>> "))
#   # print(get_number_as_words(n))
#   # assert(get_number_as_words(n))


if __name__ == "__main__":
  pass
