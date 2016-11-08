# coding=utf8
import re
import copy

simplify_pattern = re.compile(r'(?P<var_name>[a-zA-Z]+)\s*=\s*(?P<var_value>\d+)')


class Term(object):
    def __init__(self, num, dic):
        self.Num = num
        self.Dict = dic

    def eva(self, known):
        for key in known:
            if key in self.Dict:
                self.Num *= known[key] ** self.Dict.pop(key)
            else:
                pass

    def diff(self, var):
        __tmp = self.Dict.get(var)
        if __tmp == 0:
            pass
        else:
            self.Num *= __tmp
            self.Dict[var] = __tmp - 1

    def to_string(self):
        st = str(self.Num)
        for k in self.Dict:
            if self.Dict[k] == 0:
                continue
            else:
                st = st + '*' + k + '**' + str(self.Dict[k])
        return st


class Expression(object):
    def __init__(self, result, tup):
        self.Sum = result
        self.Tup = tup

    def eva(self, known):
        res = ''
        for i in self.Tup:
            term = Term(i[0], i[1])
            term.eva(known)
            st = term.to_string()
            try:
                self.Sum += float(st)
            except ValueError:
                res = res + st + '+'
        res += str(self.Sum)
        return res

    def diff(self, var):
        res = ''
        for i in self.Tup:
            term = Term(i[0], i[1])
            if var in term.Dict:
                term.diff(var)
                st = term.to_string()
                res = res + st + '+'
            else:
                pass
        return res[:-1]


def command_or_expression(user):
    if user == "#####":
        return 4
    # 命令
    if user.startswith('!simplify'):
        return 1
    # 求导
    elif user.startswith('!d/d'):
        return 2
    # 表达式
    else:
        return 3


def is_valid(char):
    if char.isdigit() or char.isalpha() or is_symbol(char):
        return True
    else:
        return False


def is_symbol(char):
    if char in ['+', '*', '-', '*', '^']:
        return True
    else:
        return False


def raise_error(error_message):
    print error_message


def command_exam(command, user, var_list):
    """
    :param command:用户输入的命令
    :param user:用户输入的原始表达式
    :param var_list:变量列表
    :return:
    """
    # 赋值过程
    count = 0
    var_dict = {}
    simplify_match = simplify_pattern.finditer(command)
    if simplify_match:
        for match in simplify_match:
            if match.group('var_name') not in var_list:
                raise_error("No such variable")
            else:
                try:
                    var_dict[match.group('var_name')] = float(match.group('var_value'))
                except ValueError:
                    raise_error('Invalid value')
            count += 1
    if not count:
        print user
        raise_error('Nothing variable')
        return False
    else:
        return var_dict


# def command_exam(command, user, varlis):
#     """
#     :param command:用户输入的命令
#     :param user:用户输入的原始表达式
#     :return:
#     """
#     # 赋值过程
#     Dic = {}
#     simplify_match = simplify_pattern.finditer(command)
#     if simplify_match:
#         for match in simplify_match:
#             if match.group('var_name') not in varlis:
#                 raise_error("No such variable")
#             else:
#                 try:
#                     Dic[match.group('var_name')] = float(match.group('var_value'))
#                 except:
#                     raise_error('Invalid value')
#         return Dic
#     else:
#         print user
#         raise_error('Nothing variable')
#         return False
#


def expression_exam(user_input):
    index = 0
    while index < len(user_input) - 1:
        if user_input[index].isdigit() and user_input[index + 1].isalpha():
            user_input = user_input[:index + 1] + '*' + user_input[index + 1:]

        if not (is_valid(user_input[index]) and is_valid(user_input[index + 1])):
            raise_error("Invalid Input")
            return False
        index += 1
    final_expression = user_input

    # 幂运算运算符替换
    if '^' in user_input:
        final_expression = user_input.replace('^', '**')

    # 减号处理
    if '-' in user_input:
        final_expression = user_input.replace('-', '+-')
    return final_expression


def var_list_exam(correct_expression):
    index = 1
    name = ''
    lis = []
    while index < len(correct_expression):
        if correct_expression[index - 1].isalpha():
            name += correct_expression[index - 1]
            if not correct_expression[index].isalpha():
                if name in lis:
                    pass
                else:

                    lis.append(name)
                name = ''
        if index == len(correct_expression) - 1 and correct_expression[index].isalpha():
            name += correct_expression[index]
            if name in lis:
                pass
            else:
                lis.append(name)
            name = ''
        else:
            pass
        index += 1
    return lis


def data_exam(final_expression):
    add_list = final_expression.split('+')
    result = 0
    data_list = []
    for i in add_list:
        try:
            result += eval(i)
        except NameError:
            multiple_list = i.split('*')
            num = 1
            dic = {}
            j = 0
            while j < (len(multiple_list)) - 1:
                if multiple_list[j].isalpha() and multiple_list[j] not in dic:
                    if multiple_list[j + 1] == '':
                        dic[multiple_list[j]] = int(multiple_list[j + 2])
                        j += 2
                    else:
                        dic[multiple_list[j]] = 1

                elif multiple_list[j].isalpha() and multiple_list[j] in dic:
                    if multiple_list[j + 1] == '':
                        dic[multiple_list[j]] += int(multiple_list[j + 2])
                        j += 2
                    else:
                        dic[multiple_list[j]] += 1
                else:
                    try:
                        num *= float(multiple_list[j])
                    except ValueError:
                        pass
                j += 1

            if multiple_list[-1].isalpha():
                if multiple_list[-1] not in dic:
                    dic[multiple_list[-1]] = 1
                else:
                    dic[multiple_list[-1]] += 1
            elif multiple_list[-1].isdigit() and j < len(multiple_list):
                num *= multiple_list[-1]
            data_list.append((int(num), dic))
    return result, tuple(data_list)


def diff_exam(diff_expression, var_list):
    try:
        var = diff_expression.split(' ')[1]
    except IndexError:
        raise_error("No such variable")
        return False
    if var in var_list:
        return var
    else:
        raise_error("No such variable")
        return False


def main():
    main_expression = ''
    main_data_final = ()
    var_list = []
    while True:
        main_user_input = raw_input('>')
        if command_or_expression(main_user_input) == 3:
            main_expression = expression_exam(main_user_input)
            if main_expression:
                print main_expression
                var_list = var_list_exam(main_expression)
                # print var_list
                if not var_list:
                    print eval(main_expression)
                    main_expression = ''
                    continue
                else:
                    main_data = data_exam(main_expression)
                    main_data_final = copy.deepcopy(main_data)
            else:
                main_expression = ''

        elif command_or_expression(main_user_input) == 2:
            var = diff_exam(main_user_input, var_list)
            if var:
                main_data = copy.deepcopy(main_data_final)
                # print  main_data
                e = Expression(main_data[0], main_data[1])
                print e.diff(var).replace("**", "^")
            else:
                pass
        elif command_or_expression(main_user_input) == 1:
            dic = command_exam(main_user_input, main_expression, var_list)
            if dic:
                main_data = copy.deepcopy(main_data_final)
                # print main_data
                e = Expression(main_data[0], main_data[1])
                res = e.eva(dic).replace("**", "^")
                try:
                    print eval(res)
                except NameError or ValueError:
                    print res
            else:
                pass
        elif command_or_expression(main_user_input) == 4:
            break
    return 0


if __name__ == "__main__":
    main()
