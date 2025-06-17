def is_valid_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11 or cpf == "12345678909":
        return False

    def calc_digit(digs: str, start_weight: int) -> int:
        total = sum(int(d) * w for d, w in zip(digs, range(start_weight, 1, -1)))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    first_digit = calc_digit(cpf[:9], 10)
    second_digit = calc_digit(cpf[:9] + str(first_digit), 11)

    return int(cpf[9]) == first_digit and int(cpf[10]) == second_digit


