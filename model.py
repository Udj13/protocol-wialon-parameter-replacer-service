"""Copyright 2021 Eugeny Shlyagin (shlyagin@gmail.com)

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""


def packets_bodies_process(s, parameters):
    packets = s.split('|')
    for i in range(len(packets)):
        for can_name_parameter in parameters:
            packets[i] = rearrange_data(packets[i], can_name_parameter)
    return '|'.join(packets)


def rearrange_data(s, parameter_name):
    if s.find(parameter_name) == -1:
        return s
    position = s.find(parameter_name) + len(parameter_name) - 1
    is_value_found = True
    value = ''
    while is_value_found:
        position += 1
        try:
            next_char = s[position]
            if next_char.isdigit() or next_char == '.':
                value += next_char
            else:
                is_value_found = False
        except IndexError:
            is_value_found = False

    splitted_data = s.split(';')
    if splitted_data[13] == '':
        splitted_data[13] = value
    else:
        splitted_data[13] += "," + value
    s = ';'.join(splitted_data)

    return s
