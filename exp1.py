# coding=utf8
import re
import copy
simplify_pattern = re.compile(
    r'(?P<var_name>[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]+)\s*=\s*(?P<var_value>\d+)')


class Term(object):
    def __init__(self,num,dic):
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

    def tostr(self):
        st = str(self.Num)
        for k in self.Dict:
            if self.Dict[k] == 0:
                continue
            else:
                st = st + '*' + k + '**' + str(self.Dict[k])
        return st


class Expression(object):
    def __init__(self,sum,tup):
        self.Sum = sum
        self.Tup = tup
    def eva(self, known):
        res = ''
        for i in self.Tup:
            term = Term(i[0],i[1])
            term.eva(known)
            st = term.tostr()
            try:
                self.Sum += float(st)
            except:
                res = res + st + '+'

        res += str(self.Sum)
        return res

    def diff(self, var):
        res = ''
        for i in self.Tup:
            term = Term(i[0],i[1])
            if var in term.Dict:
                term.diff(var)
                st = term.tostr()
                res = res + st + '+'
            else:
                pass

        return res[:-1]


def command_or_expression(user):
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

def command_exam(command, user, varlis):
   """
   :param command:用户输入的命令
   :param user:用户输入的原始表达式
   :return:
   """
   # 赋值过程
   count = 0
   Dic = {}
   simplify_match = simplify_pattern.finditer(command)
   if simplify_match:
       for match in simplify_match:
           if match.group('var_name') not in varlis:
               raise_error("No such variable")
           else:
               try:
                   Dic[match.group('var_name')] = float(match.group('var_value'))
               except:
                   raise_error('Invalid value')
           count += 1
   if not count:
       print user
       raise_error('Nothing variable')
       return False
   else:
       return Dic
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
#
# def expression_exam(user_input):
#     index = 0
#
#     while index < len(user_input) - 1:
#
#         if user_input[index].isdigit() and user_input[index + 1].isalpha():
#             user_input = user_input[:index + 1] + '*' + user_input[index + 1:]
#         if not (is_valid(user_input[index]) and is_valid(user_input[index + 1])):
#             raise_error("Invalid Input")
#             return False
#         index = index + 1
#    
#     return final_expression


def varlis_exam(corret_expression):
    index = 1
    name = ''
    lis = []
    while index < len(corret_expression):
        if corret_expression[index - 1].isalpha():
            name += corret_expression[index - 1]
            if not corret_expression[index].isalpha():
                if name in lis:
                    pass
                else:
                    lis.append(name)
                name = ''
        if index == len(corret_expression) - 1 and corret_expression[index].isalpha():
            name += corret_expression[index]
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
    addlis = final_expression.split('+')
    sum = 0
    datalist = []
    for i in addlis:
        try:
            sum += eval(i)
        except:
            multilis = i.split('*')
            num = 1
            dic = {}
            j = 0
            while j < (len(multilis)) - 1:
                if multilis[j].isalpha() and multilis[j] not in dic:
                    if multilis[j + 1] == '':
                        dic[multilis[j]] = int(multilis[j + 2])
                        j = j + 2
                    else:
                        dic[multilis[j]] = 1

                elif multilis[j].isalpha() and multilis[j] in dic:
                    if multilis[j + 1] == '':
                        dic[multilis[j]] += int(multilis[j + 2])
                        j = j + 2
                    else:
                        dic[multilis[j]] += 1
                else:
                    try:
                        num *= float(multilis[j])
                    except:
                        pass
                j += 1
            if multilis[-1].isalpha():

                if multilis[-1] not in dic:
                    dic[multilis[-1]] = 1
                else:
                    dic[multilis[-1]] += 1
            elif multilis[-1].isdigit() and j < len(multilis):
                num *= multilis[-1]

            datalist.append((int(num), dic))

    return (sum, tuple(datalist))


def diff_exam(diff_expression, varlis):
    try:
        var = diff_expression.split(' ')[1]
    except:
        raise_error("No such variable")
        return False
    if var in varlis:
        return var
    else:
        raise_error("No such variable")
        return False


def main():
    main_expression = ''
    main_data = ()
    main_data_final=()
    varlis = []
    while True:
        main_user_input = raw_input('>')
        if command_or_expression(main_user_input) == 3:
            main_expression = expression_exam(main_user_input)
            if main_expression:
                print main_expression
                varlis = varlis_exam(main_expression)
                # print varlis
                if varlis == []:
                    print eval(main_expression)
                    main_expression = ''
                    continue
                else:
                    main_data = data_exam(main_expression)
                    main_data_final = copy.deepcopy(main_data)
            else:

                main_expression = ''

        elif command_or_expression(main_user_input) == 2:
            var = diff_exam(main_user_input, varlis)
            if var:
                main_data = copy.deepcopy(main_data_final)
                #print  main_data
                e = Expression(main_data[0],main_data[1])
                print e.diff(var).replace("**", "^")
            else:
                pass
        elif command_or_expression(main_user_input) == 1:
            dic = command_exam(main_user_input, main_expression, varlis)
            if dic:
                main_data = copy.deepcopy(main_data_final)
                #print main_data
                e = Expression(main_data[0],main_data[1])
                res=e.eva(dic).replace("**", "^")
                try:
                    print eval(res)
                except:
                    print res

            else:
                pass
    return 0


if __name__ == "__main__":
    main()

