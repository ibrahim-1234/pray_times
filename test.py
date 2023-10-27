def longestAlternatingSubstring(digits: str) -> str:
    res = [digits[0]]
    a = ''

    for i in digits:
        if int(res[len(res)-1]) % 2 == 0:
            if int(i) % 2 != 0:
                res.append(i)
            else:
                if len(a) < len(res):
                    a = ''.join(res)
                res = [i]

        else:
            if int(i) % 2 == 0:
                res.append(i)
            else:
                if len(a) < len(res):
                    a = ''.join(res)
                res = [i]
    return a


print(longestAlternatingSubstring('1263654081858902'))