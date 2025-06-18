
class ValidationStrategy:
    @abstract
    def validate(self, data: str) -> bool:
        pass


class Validator:
    def __init__(self, strategy: ValidationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ValidationStrategy):
        self._strategy = strategy
    
    def perform_validation(self, data: str) -> bool:
        return self._strategy.validate(data)


class CpfValidation(ValidationStrategy):
    def validate(slef, cpf: str) -> bool:
        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11 or cpf == cpf[0] * 11 or cpf == "12345678909":
            return False

        first_digit = self.calc_digit(cpf[:9], 10)
        second_digit = self.calc_digit(cpf[:9] + str(first_digit), 11)

        return int(cpf[9]) == first_digit and int(cpf[10]) == second_digit

    def calc_digit(self, digs: str, start_weight: int) -> int:
        total = sum(int(d) * w for d, w in zip(digs, range(start_weight, 1, -1)))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder


class PlateValidation(ValidationStrategy):
    def validate(self, plate: str) -> bool:
        plate = plate.upper().strip()

        # Padrão Mercosul: 3 letras, 1 número, 1 letra, 2 números (e.g., ABC4E67)
        padrao_mercosul = re.compile(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$')
        if padrao_mercosul.match(plate):
            return True

        # Padrão Antigo: 3 letras, 4 números (e.g., ABC1234)
        padrao_antigo = re.compile(r'^[A-Z]{3}[0-9]{4}$')
        if padrao_antigo.match(plate):
            return True

        return False