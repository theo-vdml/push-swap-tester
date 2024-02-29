import os
import random
import itertools

tester_name = "./checker_linux"

def n_random(length, minimum, maximum):
    # Vérifier que la plage est valide
    if maximum - minimum + 1 < length:
        raise ValueError("La plage spécifiée ne peut pas générer suffisamment de nombres uniques.")

    # Générer la liste de nombres aléatoires uniques
    random_numbers = random.sample(range(minimum, maximum + 1), length)

    # Convertir la liste de nombres en une chaîne de caractères
    result_string = ' '.join(map(str, random_numbers))

    return result_string


def swap(stack):
    if len(stack) >= 2:
        stack[0], stack[1] = stack[1], stack[0]

def push(source_stack, dest_stack):
    if source_stack:
        dest_stack.append(source_stack.pop(0))
        reverse_rotate(dest_stack)
def rotate(stack):
    if stack:
        element = stack.pop(0)
        stack.append(element)

def reverse_rotate(stack):
    if stack:
        element = stack.pop()
        stack.insert(0, element)

def ss(stack_a, stack_b):
    swap(stack_a)
    swap(stack_b)

def rr(stack_a, stack_b):
    rotate(stack_a)
    rotate(stack_b)

def rrr(stack_a, stack_b):
    reverse_rotate(stack_a)
    reverse_rotate(stack_b)

def print_stacks(stack_a, stack_b):
    def get_size(stack):
        return len(stack)

    size_a = get_size(stack_a)
    size_b = get_size(stack_b)
    offset_a = size_b - size_a
    offset_b = size_a - size_b
    offset_a = 0 if offset_a < 0 else offset_a
    offset_b = 0 if offset_b < 0 else offset_b
    i = 0
    print()
    while i < max(size_a, size_b):
        if i >= offset_a:
            content_a = stack_a[i - offset_a]
            print(f"    {content_a}\t\t    ", end="")
        else:
            print("\t \t\t\t\t", end="")

        if i >= offset_b:
            content_b = stack_b[i - offset_b]
            print(f"{content_b}")
        else:
            print("")

        i += 1

    print("(a) ------\t\t(b) ------\n")

def print_red(skk): print("\033[91m {}\033[00m" .format(skk))
 
 
def print_orange(skk): print("\033[33m {}\033[00m" .format(skk))

def print_green(skk): print("\033[92m {}\033[00m" .format(skk))

def check_rules(size, actions):
    rules_dict = {
        3: 3,          # Sorting 3 values: no more than 3 actions
        5: 12,         # Sorting 5 values: no more than 12 actions
        100: {         # Sorting 100 values
            True: 700,
            '4/5': 900,
            '3/5': 1100,
            '2/5': 1300,
            '1/5': 1500
        },
        500: {         # Sorting 500 values
            True: 5500,
            '4/5': 7000,
            '3/5': 8500,
            '2/5': 10000,
            '1/5': 11500
        }
    }

    if size in rules_dict:
        rules = rules_dict[size]
        if isinstance(rules, int):
            return actions <= rules
        elif isinstance(rules, dict):
            for points, limit in rules.items():
                if actions <= limit:
                    return points
            return False
    return True


def main(n_test, sizes, logtype):

    output = ""

    for size in sizes:

        print("=====================")
        print("Tests for size : " + str(size))
        print("=====================")
        print()
        av = 0
        min = -1
        maximum = -1
        perms_count = 0
        if(size in [0]):
            perms = itertools.permutations(range(size))
            for perm in perms:
                args = " "
                args = args + ' '.join(map(str, perm)) + " "
                fail = False
                steps = os.popen("./push_swap " + args).read().strip()
                count = os.popen("./push_swap " + args + " | wc -l").read().strip()
                av = av + int(count)
                checker = os.popen("./push_swap " + args + " | " + tester_name + " " + args).read().strip()
                if (int(count) > maximum):
                    maximum = int(count)
                if (int(count) < min or min == -1):
                    min = int(count)
                if(checker == "KO"):
                    fail = True
                    print_red("Permutation " + str(perms_count + 1) + ": " + count + " actions, result = " + checker)
                else:
                    if(check_rules(size, int(count)) == False):
                        print_red("Permutation " + str(perms_count + 1) + ": " + count + " actions (TOO MANY), result = " + checker)
                        fail = True
                    elif(check_rules(size, int(count)) == True):
                        print_green("Permutation " + str(perms_count + 1) + ": " + count + " actions, result = " + checker)
                    else:
                        print_orange("Permutation " + str(perms_count + 1) + ": " + count + " actions ("+check_rules(size, int(count))+"), result = " + checker)
                if ((fail and logtype == "fails") or logtype == "all"):
                        print("\033[91m###########################[ARGS]#########################")
                        print(args)
                        print("###########################[STEPS]#########################\033[00m")
                        steps = steps.split("\n")
                        stack_a = args.split()
                        stack_b = []
                        print_orange("--[INIT]--")
                        print_stacks(stack_a, stack_b)
                        for step in steps:
                            if (step == "pa"):
                                push(stack_b, stack_a)
                            if (step == "pb"):
                                push(stack_a, stack_b)
                            if (step == "sa"):
                                swap(stack_a)
                            if (step == "sb"):
                                swap(stack_b)
                            if (step == "ss"):
                                ss(stack_a, stack_b)
                            if (step == "ra"):
                                rotate(stack_a)
                            if (step == "rb"):
                                rotate(stack_b)
                            if (step == "rr"):
                                rr(stack_a, stack_b)
                            if (step == "rra"):
                                reverse_rotate(stack_a)
                            if (step == "rrb"):
                                reverse_rotate(stack_b)
                            if (step == "rrr"):
                                rrr(stack_a, stack_b)
                            print_orange("--[" + step + "]--")
                            print_stacks(stack_a, stack_b)
                        print("###########################[END]#########################\033[00m")
                perms_count = perms_count + 1
        for test in range(n_test):
            args = n_random(size, -99999, 99999)
            fail = False
            steps = os.popen("./push_swap " + args).read().strip()
            count = os.popen("./push_swap " + args + " | wc -l").read().strip()
            checker = os.popen("./push_swap " + args + " | " + tester_name + " " + args).read().strip()
            av = av + int(count)
            if (int(count) > maximum):
                maximum = int(count)
            if (int(count) < min or min == -1):
                min = int(count)
            if(checker == "KO"):
                fail = True
                print_red("Test " + str(test + 1) + ": " + count + " actions, result = " + checker)
            else:
                if(check_rules(size, int(count)) == False):
                    print_red("Test " + str(test + 1) + ": " + count + " actions (TOO MANY), result = " + checker)
                    fail = True
                elif(check_rules(size, int(count)) == True):
                    print_green("Test " + str(test + 1) + ": " + count + " actions, result = " + checker)
                else:
                    print_orange("Test " + str(test + 1) + ": " + count + " actions ("+check_rules(size, int(count))+"), result = " + checker)
            if ((fail and logtype == "fails") or logtype == "all"):
                    print("\033[91m###########################[ARGS]#########################")
                    print(args)
                    print("###########################[STEPS]#########################\033[00m")
                    steps = steps.split("\n")
                    stack_a = args.split()
                    stack_b = []
                    print_orange("--[INIT]--")
                    print_stacks(stack_a, stack_b)
                    for step in steps:
                        if (step == "pa"):
                            push(stack_b, stack_a)
                        if (step == "pb"):
                            push(stack_a, stack_b)
                        if (step == "sa"):
                            swap(stack_a)
                        if (step == "sb"):
                            swap(stack_b)
                        if (step == "ss"):
                            ss(stack_a, stack_b)
                        if (step == "ra"):
                            rotate(stack_a)
                        if (step == "rb"):
                            rotate(stack_b)
                        if (step == "rr"):
                            rr(stack_a, stack_b)
                        if (step == "rra"):
                            reverse_rotate(stack_a)
                        if (step == "rrb"):
                            reverse_rotate(stack_b)
                        if (step == "rrr"):
                            rrr(stack_a, stack_b)
                        print_orange("--[" + step + "]--")
                        print_stacks(stack_a, stack_b)
                    print("###########################[END]#########################\033[00m")
        av = int(av / (n_test + perms_count))
        
        # print()
        # print("-> Average for " + str(size) + " numbers is " + str(av) + " actions")
        # print("-> Your maximum for " + str(size) + " numbers is " + str(maximum) + " actions")
        # print("-> Your min for " + str(size) + " numbers is " + str(min) + " actions")
        output = output + "\n\n==== [ Results for " + str(size) + "] ====\n"
        output = output + "-> Average: " + str(av) + " actions" + "\n"
        output = output + "-> Min: " + str(min) + " actions" + "\n"
        output = output + "-> Max: " + str(maximum) + " actions" + "\n"
        if(check_rules(size, int(av)) == False):
            output = output + "-> Score (average): \033[91m0/5 TOO MANY ACTIONS\n\033[00m"
        elif(check_rules(size, int(av)) == True):
            output = output + "-> Score (average): \033[92m5/5\n\033[00m"
        else:
            output = output + "-> Score (average): \033[33m" + check_rules(size, int(av)) + " TOO MANY ACTIONS\n\033[00m"
        if(check_rules(size, int(maximum)) == False):
            output = output + "-> Score (maximum): \033[91m0/5 TOO MANY ACTIONS\n\033[00m"
        elif(check_rules(size, int(maximum)) == True):
            output = output + "-> Score (maximum): \033[92m5/5\n\033[00m"
        else:
            output = output + "-> Score (maximum): \033[33m" + check_rules(size, int(maximum)) + " TOO MANY ACTIONS\n\033[00m"
        
        print()

    print(output)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        n_test = int(sys.argv[1])
    else:
        n_test = 1
    
    if len(sys.argv) > 2:
        sizes = [int(sys.argv[2])]
    else:
        sizes = [2, 3, 5, 100, 500]

    if len(sys.argv) > 3:
        logtype = sys.argv[3]
    else:
        logtype = ""

    main(n_test, sizes, logtype)


