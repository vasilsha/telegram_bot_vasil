import random
import secrets


class SettingsPG:
    def __init__(self, length=None, low_c_latin=None, up_c_latin=None, digit=None, low_c_no_latin=None,
                 up_c_no_latin=None, special_char=None):
        self.length = length
        self.low_c_latin = low_c_latin
        self.up_c_latin = up_c_latin
        self.digit = digit
        self.low_c_no_latin = low_c_no_latin
        self.up_c_no_latin = up_c_no_latin
        self.special_char = special_char
        if length is None:
            self.length = 6
        if low_c_latin is None:
            self.low_c_latin = True
        if up_c_latin is None:
            self.up_c_latin = True
        if digit is None:
            self.digit = True
        if low_c_no_latin is None:
            self.low_c_no_latin = False
        if up_c_no_latin is None:
            self.up_c_no_latin = False
        if special_char is None:
            self.special_char = False

    def set_length(self, length):
        self.length = length

    def set_low_c_latin(self, low_c_latin):
        self.low_c_latin = low_c_latin

    def set_up_c_latin(self, up_c_latin):
        self.up_c_latin = up_c_latin

    def set_digit(self, digit):
        self.digit = digit

    def set_low_c_no_latin(self, low_c_no_latin):
        self.low_c_no_latin = low_c_no_latin

    def set_up_c_no_latin(self, up_c_no_latin):
        self.up_c_no_latin = up_c_no_latin

    def set_special_char(self, special_char):
        self.special_char = special_char

    def get_length(self):
        return self.length

    def get_low_c_latin(self):
        return self.low_c_latin

    def get_up_c_latin(self):
        return self.up_c_latin

    def get_digit(self):
        return self.digit

    def get_low_c_no_latin(self):
        return self.low_c_no_latin

    def get_up_c_no_latin(self):
        return self.up_c_no_latin

    def get_special_char(self):
        return self.special_char

    def check_pass_empty(self):
        if self.digit or self.low_c_latin or self.up_c_no_latin or self.up_c_latin or self.low_c_no_latin or self.special_char:
            return False
        return True

    def print_settings(self):
        """ debug """
        print(self.get_length(), self.get_low_c_latin(), self.get_up_c_latin(), self.get_digit(),
              self.get_low_c_no_latin(), self.get_up_c_no_latin(), self.get_special_char())


settings_list = SettingsPG()


def pass_gen(settings_list):
    latin_low_chars = 'qwertyuiopasdfghjklzxcvbnm'
    numbers = '0123456789'
    non_latin_low_chars = 'ёйцукенгшщзхъфывапролджэячсмитьбю'
    special_chars = "`~!@#$%^&*()_-+=[{]}\\\"/|;:'/? "
    pass_chars = ""
    if settings_list.get_low_c_latin():
        pass_chars = pass_chars + latin_low_chars
    if settings_list.get_up_c_latin():
        pass_chars = pass_chars + latin_low_chars.upper()
    if settings_list.get_digit():
        pass_chars = pass_chars + numbers
    if settings_list.get_low_c_no_latin():
        pass_chars = pass_chars + non_latin_low_chars
    if settings_list.get_up_c_no_latin():
        pass_chars = pass_chars + non_latin_low_chars.upper()
    if settings_list.get_special_char():
        pass_chars = pass_chars + special_chars
    if len(pass_chars) < 1:
        pass_chars = '!'
    pass_list = []
    for i in range(settings_list.get_length()):
        pass_list.append(secrets.choice(pass_chars))
    random.shuffle(pass_list)
    password = "".join(pass_list)
    return password

# settings_list.set_length(55)
# settings_list.set_special_char(True)
# settings_list.print_settings()
# print(pass_gen(settings_list))
