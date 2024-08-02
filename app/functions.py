def number_to_text_uzbek(n):
    units = ["", "bir", "ikki", "uch", "to'rt", "besh", "olti", "yetti", "sakkiz", "to'qqiz"]
    tens = ["", "o'n", "yigirma", "o'ttiz", "qirq", "ellik", "oltmish", "yetmish", "sakson", "to'qson"]
    thousands = ["", "ming", "million", "milliard"]

    if n == 0:
        return "nol"

    text_representation = []
    group_index = 0

    while n > 0:
        group = n % 1000
        n //= 1000

        if group != 0:
            group_text = []
            hundreds = group // 100
            remainder = group % 100

            if hundreds != 0:
                group_text.append(units[hundreds] + " yuz")

            if remainder >= 10 and remainder < 20:
                group_text.append(tens[1] + " " + units[remainder % 10])
            elif remainder >= 20:
                group_text.append(tens[remainder // 10])
                if remainder % 10 != 0:
                    group_text.append(units[remainder % 10])
            elif remainder != 0:
                group_text.append(units[remainder])

            if group_index < len(thousands) and thousands[group_index]:
                group_text.append(thousands[group_index])

            text_representation.append(" ".join(group_text).strip())

        group_index += 1

    return " ".join(reversed(text_representation)).strip()
