def pythonExam():
    print('''# %% [markdown]
# # Practical 1
# 
# ## Name:XYZ
# ## Roll no:123
# 

# %% [markdown]
# Q1 What is the result of the following operation in Python?
#    3+2*2**2//3
# 

# %%
   3+2*2**2//3

# %% [markdown]
# P/B: Parentheses/Brackets:
# 
# Solve expressions inside parentheses or brackets first.
# E/O: Exponents/Orders (i.e., powers and square roots, etc.):
# MD: Multiplication and Division (from left to right):
# 
# Perform multiplication and division operations from left to right.
# AS: Addition and Subtraction (from left to right):
# 
# Finally, perform addition and subtraction operations from left to right.

# %% [markdown]
# Q2 The variables A= ‘1’ and B = ’2’, What is the result of A+B? 
# a) You can’t add two strings 
# b) ‘3’
# c) 12
# d) 3
# 
# 

# %%
A='1'
B='2'
A+B

# %% [markdown]
# Q3 Construct a simple calculator using arithmetic operations

# %%
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print("Choose operation:")
print("1. Add")
print("2. Subtract")
print("3. Multiply")
print("4. Divide")

choice = input("Enter choice (1/2/3/4): ")

if choice in ('1', '2', '3', '4'):
    if choice == '1':
        z= num1 + num2
        print(z)
    elif choice == '2':
        z= num1 - num2
        print(z)
    elif choice == '3':
        z= num1 * num2
        print(z)
    elif choice == '4':
        z= num1/num2
        print(z)
else:
    print("Invalid input. Please choose a valid operation (1/2/3/4).")



# %%
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Error: Cannot divide by zero."
    
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print("Choose operation:")
print("1. Add")
print("2. Subtract")
print("3. Multiply")
print("4. Divide")

choice = input("Enter choice (1/2/3/4): ")

if choice in ('1', '2', '3', '4'):
    if choice == '1':
        result = add(num1, num2)
        print(f"{num1} + {num2} = {result}")
    elif choice == '2':
        result = subtract(num1, num2)
        print(f"{num1} - {num2} = {result}")
    elif choice == '3':
        result = multiply(num1, num2)
        print(f"{num1} * {num2} = {result}")
    elif choice == '4':
        result = divide(num1, num2)
        print(f"{num1} / {num2} = {result}")
else:
    print("Invalid input. Please choose a valid operation (1/2/3/4).")


# %% [markdown]
# Q4 Develop a program to check if two numbers are equal, less than or greater than.

# %%
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

if num1 == num2:
    print(f"{num1} is equal to {num2}")
elif num1 > num2:
    print(f"{num1} is greater than {num2}")
else:
    print(f"{num1} is less than {num2}")


# %% [markdown]
# Q5 What is the output of the following lines of code? 
# x=1 
# if(x!=1): 
#     print('Hello') 
# else: print('Hi')
# print('Mike')

# %%
x=1
if(x!=1):
    print('Hello')
else:
    print('Hi')
    print('Mike')

# %% [markdown]
# Q6. How many iterations are performed in the following loop and what is the output 
# for n in range(3): 
#     print(n+1)
# 
# 

# %%
for n in range(3): 
    print(n+1)

# %% [markdown]
# Explanation
# First iteration (n = 0):
# 
# print(0 + 1) prints 1.
# Second iteration (n = 1):
# 
# print(1 + 1) prints 2.
# Third iteration (n = 2):
# 
# print(2 + 1) prints 3.

# %% [markdown]
# Q7.
# What is g(25) – g(24), given the definition of g below?
# def g(n): 
#     s=0
#     for i in range(1, n+1):
#         if n%i == 0:
#            s = s+1
#     return(s)
# 
# 

# %%
def g(n): 
    s=0
    for i in range(1, n+1):
        if n%i == 0:
           s = s+1
    return(s)
result_g_25 = g(25)
result_g_24 = g(24)

final_result = result_g_25 - result_g_24

print(f"g(25) - g(24) = {final_result}")

# %% [markdown]
# Q 8
#  Write a python program to reverse a given number 
# Sample Input: 783 
# Output: 387 
# Sample Input: 242789 
# Output: 987242 
# Sample Input: 3 
# Output: 3

# %%
def reverse_number(num):
    reversed_num = 0
    while num > 0:
        digit = num % 10
        reversed_num = (reversed_num * 10) + digit
        num = num // 10
    return reversed_num

print(f"Reverse Number = {reverse_number(387)}")
print(f"Reverse Number = {reverse_number(242789)}")   
print(f"Reverse Number = {reverse_number(3)}")

# %% [markdown]
# Q9: Write a program to print Fibonacci series of a number entered by user 
# Sample Input and output
# How many terms? 7 
# Fibonacci sequence: 
# 0 
# 1 
# 1 
# 2 
# 3 
# 5 
# 8 
# Sample Input and output
# How many terms? -1 
# Enter a positive integer 
# Sample Input and output 
# How many terms? 1 
# Fibonacci sequence: 
# 0

# %%
num_terms = int(input("How many terms? "))
if num_terms <= 0:
    print("Enter a positive integer.")
elif num_terms == 1:
    print("Fibonacci sequence:\n0")
else:
    fib_series = [0, 1]
    a, b = 0, 1

    for _ in range(2, num_terms):
        next_term = a + b
        fib_series.append(next_term)
        a, b = b, next_term

    print("Fibonacci sequence:")
    for term in fib_series:
        print(term)


# %% [markdown]
# Q10 Write a python program to read a number n and print the sum of odd natural numbers between the range of 1 to n both inclusive 
# Sample Input and output 
# Enter a number 10 
# Sum = 25

# %%
n = int(input("Enter a number: "))

if n < 1:
    print("Please enter a positive integer.")
else:

    oddsum = 0
    for num in range(1, n + 1,2):
        oddsum += num

    print(f"Sum of odd natural numbers between 1 and {n}: {oddsum}")


# %% [markdown]
# Q11 Write a Program to find whether a given number is Strong Numbers Sample Input and output Q5.Enter a number:145 The number is a strong number. Enter a number:234 The number is not a strong number.

# %%
num = int(input("Enter a number: "))

if num < 0:
    print("Please enter a non-negative integer.")
else:
    original_num = num
    sum_factorials = 0

    while num > 0:
        digit = num % 10
        factorial = 1
        for i in range(1, digit + 1):
            factorial *= i

        sum_factorials += factorial
        num //= 10
    if sum_factorials == original_num:
        print("The number is a strong number.")
    else:
        print("The number is not a strong number.")


# %% [markdown]
# Q12 Write a python Program to compute the roots of the equation ax2 + bx + c = 0 and print using three-decimal places.
# 
# The roots are real if the discriminant D = b2 − 4ac is non-negative. If the discriminant is negative, then the roots are complex conjugate
# The program proceeds in the following steps. 
# (a) It accepts the values of a, b and c from the keyboard.
# (b) No solution if both a and b are zero. The program finishes with appropriate message.
# (c) Linear equation if a = 0 but and the root is −c/b. The program prints out the root with appropriate message and the program finishes. 
# (d) Calculates the discriminant D and determines the corresponding roots. 
# (e) Prints out the roots with appropriate message and the program finishes.
# 
# Test data and expected output: 
# Enter a,b,c: 0 2 3 Linear equation: root=-1.500 
# Enter a,b,c: 1 3 2 The roots are real: -1.000 and -2.000 
# Enter a,b,c: 2 6 9 The roots are complex: -1.500+1.500 i and -1.500-1.500 i 
# Enter a,b,c: 0 0 4 No solution: a & b both zero

# %%
import math

a, b, c = map(float, input("Enter a, b, c (separated by space): ").split())

if a == 0:
    if b == 0:
        print("No solution: a and b both zero.")
    else:
        root_linear = -c / b
        print(f"Linear equation: root = {root_linear:.3f}")
else:
    discriminant = b**2 - 4*a*c

    if discriminant >= 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        print(f"The roots are real: {root1:.3f} and {root2:.3f}")
    else:
        real_part = -b / (2*a)
        imaginary_part = math.sqrt(abs(discriminant)) / (2*a)
        root1_complex = f"{real_part:.3f}+{imaginary_part:.3f}i"
        root2_complex = f"{real_part:.3f}-{imaginary_part:.3f}i"
        print(f"The roots are complex: {root1_complex} and {root2_complex}")


# %% [markdown]
# Q13 Accept the marks for the number of subjects studying in this semester. While accepting marks check the constraints that entered marks should not be negative as well as should not be more than 100 (if entered terminate the code). If the constraint is satisfied calculate the total & percentage. If % is greater than equal to 92 display “Merit” if % is between 75 and 91 display “Distinction” if % is between 60 and 74 “First class” if % is between 45 to 59 display “Second class” else display “Fail”

# %%
def is_valid_marks(marks):
    return 0 <= marks <= 100
def calculate_grade(percentage):
    if percentage >= 92:
        return "Merit"
    elif 75 <= percentage <= 91:
        return "Distinction"
    elif 60 <= percentage <= 74:
        return "First class"
    elif 45 <= percentage <= 59:
        return "Second class"
    else:
        return "Fail"

num_subjects = int(input("Enter the number of subjects: "))

total_marks = 0
for i in range(1, num_subjects + 1):
    marks = float(input(f"Enter marks for subject {i}: "))

    if not is_valid_marks(marks):
        print("Invalid marks entered. Exiting program.")
        exit()

    total_marks += marks

percentage = (total_marks / (num_subjects * 100)) * 100

print(f"\nTotal Marks: {total_marks}")
print(f"Percentage: {percentage:.2f}%")

grade = calculate_grade(percentage)
print(f"Grade: {grade}")


# %% [markdown]
# Q 14 Write a program to implement logic gates (AND, OR, NOT) gates

# %%
def and_gate(input1, input2):
    return input1 and input2

def or_gate(input1, input2):
    return input1 or input2

def not_gate(input1):
    return not input1

input1 = bool(int(input("Enter input 1 (0 or 1): ")))
input2 = bool(int(input("Enter input 2 (0 or 1): ")))

result_and = and_gate(input1, input2)
print(f"AND Gate: {input1} AND {input2} = {int(result_and)}")

result_or = or_gate(input1, input2)
print(f"OR Gate: {input1} OR {input2} = {int(result_or)}")

result_not = not_gate(input1)
print(f"NOT Gate for input {input1}: NOT {input1} = {int(result_not)}")


# %% [markdown]
# Q 15
# Write a Python program to print the following pattern. Take number of lines as input from user.
#  5 4 3 2 1                    
#    4 3 2 1
#      3 2 1
#        2 1
# 	     1
# 

# %%
num_lines = int(input("Enter the number of lines: "))

for i in range(num_lines):
    for j in range(i):
        print("  ", end="")

    for k in range(num_lines - i, 0, -1):
        print(f"{k} ", end="")

    print()
# %% [markdown]
# # Experiment_2

# %% [markdown]
# Write a Python program to calculate the length of a string

# %%
def string_length(string):  
  return len(string)
string = "Hello, world!"
length = string_length(string)
print(f"The length of the string '{string}' is {length}")


# %% [markdown]
# Write a Python program to count the number of characters (character frequency) in a string

# %%
def char_frequency(string):
  char_counts = {}
  for char in string:
    if char in char_counts:
      char_counts[char] += 1
    else:
      char_counts[char] = 1
  return char_counts

string = "Hello, world! I love data analysis with python"
char_counts = char_frequency(string)
print("Character frequencies:")
for char, count in char_counts.items():
  print(f"'{char}': {count}")


# %%
# Write a Python program to get a string made of the first 2 and last 2 characters of a given string. If the string length is less than 2, return the empty string instead.

# Sample String : 'resource'
# Expected Result : 'rece'
# Sample String : 'co'
# Expected Result : 'coco'
# Sample String : ' w'
# Expected Result : Empty String

# %%
def first_last_two(string):
  if len(string) < 2:
    return ""
  else:    
    return string[:min(2, len(string))] + string[-min(2, len(string)):]


string1 = "resource"
string2 = "co"
string3 = "w"

result1 = first_last_two(string1)
result2 = first_last_two(string2)
result3 = first_last_two(string3)

print(f"String: '{string1}', Result: '{result1}'")
print(f"String: '{string2}', Result: '{result2}'")
print(f"String: '{string3}', Result: '{result3}'")


# %% [markdown]
# Write a Python program to get a string from a given string where all occurrences of its first char have been changed to '$', except the first char itself.
# Sample String : 'restart'
# Expected Result : 'resta$t'

# %%
user_input=input("Enter a string")
if user_input:
    first_char=user_input[0]
    modified_string=first_char + user_input[1:].replace(first_char,'$')
    print(f"The modified string is {modified_string}")
else:
    print("Cannot Modify")

# %% [markdown]
# Write a Python program to remove characters that have odd index values in a given string.

# %%
def remove_odd_index_chars(input_string):
    result_string = input_string[::2]
    return result_string

given_string = input("Enter a string: ")
result = remove_odd_index_chars(given_string)
print('String: ', given_string)
print("Result:", result)


# %% [markdown]
# 
# Write a python program to Check if a Substring is Present in a Given String.

# %%
def check_substring(text, substring):
  return substring in text

text = input("Enter the main text: ")
substring = input("Enter the substring to search for: ")

if check_substring(text, substring):
  print("The substring is present in the text.")
else:
  print("The substring is not present in the text.")


# %% [markdown]
#  
# Write a Python Program to Form a New String where the First Character and the Last Character have been Exchanged. 

# %%
def exchange_first_last_chars(string):
  if len(string) >= 2:
    return string[-1:] + string[1:-1] + string[:1]
  else:
    return string  


original_string = input("Enter a string: ")


modified_string = exchange_first_last_chars(original_string)
print("Original string:", original_string)
print("Modified string:", modified_string)


# %% [markdown]
# 
# Accept a string as an input from the user. Check if the accepted string is palindrome or not.
# If the string is Palindrome, print “String is palindrome”, otherwise print “String is not palindrome”.
# Also print the actual and reversed strings.
# Note – Ignore the case of characters.
# 

# %%
def is_palindrome(text):

  lower_text = text.lower()

  reversed_text = lower_text[::-1]

  return lower_text == reversed_text

text = input("Enter a string: ")

is_palindrome_result = is_palindrome(text)


print(f"String: {text}")
print(f"Is palindrome: {is_palindrome_result}")
print(f"Original string: {text}")
print(f"Reversed string: {text[::-1]}")


# %% [markdown]
#  
# Accept two strings ‘string1’ and ‘string2’ as an input from the user. Generate a resultant string, such that it is a concatenated string of all upper case alphabets from both the strings in order they appear. Print the actual and the resultant strings.
# Sample Input:
#            string1:       I Like C
#            string2:       Mary Likes Python
#           Output:        ILCMLP
# 
# 

# %%
def concatenate_uppercase(string1, string2):
  uppercase_letters = "".join(
      c for c in string1 + string2 if c.isupper()
  )
  return uppercase_letters


string1 = input("Enter the first string: ")
string2 = input("Enter the second string: ")
resultant_string = concatenate_uppercase(string1, string2)
print(f"Actual strings:\nstring1: {string1}\nstring2: {string2}")
print(f"Resultant string: {resultant_string}")


# %% [markdown]
# 
# Write a python program to check if two strings have the same characters (in case insensitive with the same character count) example [“roha”,”roaah”]=False [“aabc”,”abca”]=True

# %%
def have_same_chars(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    if len(str1) != len(str2):
        return False
    char_counts = {}
    for char in str1:
        char_counts[char] = char_counts.get(char, 0) + 1
    for char in str2:
        char_counts[char] = char_counts.get(char, 0) - 1
    return all(count == 0 for count in char_counts.values())
 
print(have_same_chars("roha", "roaah"))
print(have_same_chars("aabc", "abca"))
print(have_same_chars("Hello", "hello"))
print(have_same_chars("Python", "Pyhton")) 
print(have_same_chars("abc", "abbc"))

# %% [markdown]
# 
#  Input will consist of the number of words separated by spaces and possibly commas. There will be a full stop to determine (and print) what percentage the words are more than 6 letters long. 

# %%
words=input("Enter words seperated by spaces and/or commas:\n")
word_list=words.split()
long_words=0
total_words=0
for word in word_list:
    if len(word)>6:
        long_words+=1
    total_words+=1
percentage=(long_words/total_words)*100
print(f"{percentage:2f}% of words are more than 6 letters long")

# %% [markdown]
# 
# Read in a sentence composed of words separated by at least one space, and print them out again with only one space between each word and every second word reversed. The sentence on input and output is to be concluded with full stop. Thus sample output might be: This si an elpmaxe of tahw is tnaem.

# %%
def reverse_every_second_word(sentence):
  words = sentence.strip().split()
  for i in range(1, len(words), 2):
    words[i] = words[i][::-1]
  return ' '.join(words) + '.'

# Get user input for the sentence
sentence = input("Enter a sentence: ")

# Reverse every second word and print the result
result = reverse_every_second_word(sentence)
print(result)


# %% [markdown]
# 
# Trimming can be described as a process of removing from the end of a string of characters some selection of characters. Input a string and write a program to trim all the occurrence of multiple spaces from the string. 

# %% [markdown]
# Python Split String – How to Split a String into a List or Array in Python
# 
# split a string using built-in Python methods such as split(), splitlines(), and partition().
# 
# Since strings are immutable, they cannot be changed once they have been created. Any action that seems to modify a string actually produces a new string.
# 
# Concatenation, slicing, and formatting are just a few of the many operations that you can perform on strings in Python. You can also use strings with a number of built-in modules and functions, including re, str(), and len().
# 
# There's also a wide range of string operations, including split(), replace(), and strip(), that are available in Python. You can use them to manipulate strings in different ways.
# 
# myString = "Hello world"
# 
# How to Split a String into a List Using the split() Method
# The split() method is the most common way to split a string into a list in Python. This method splits a string into substrings based on a delimiter and returns a list of these substrings.
# ![image.png](attachment:image.png)
# 
# How to Split a String into a List Using the splitlines() Method
# 
# The splitlines() method is used to split a string into a list of lines, based on the newline character (\n).
# 
# ![image-2.png](attachment:image-2.png)
# 
# In this example, we split the string "hello\nworld" into a list of two elements, "hello" and "world", using the splitlines() method
# 
# How to Split a String into a List Using Regular Expressions with the re Module
# 
# The re module in Python provides a powerful way to split strings based on regular expressions.
# 
# ![image-3.png](attachment:image-3.png)
# In this example, we split the string "hello world" into a list of two elements, "hello" and "world", using a regular expression that matches any whitespace character (\s).
# 
# How to Split a String into a List Using the partition() Method
# 
# The partition() method splits a string into three parts based on a separator and returns a tuple containing these parts. The separator itself is also included in the tuple.
# 
# ![image-4.png](attachment:image-4.png)
# 
# When to Use Each Method
# So here's an overview of these methods and when to use each one for quick reference:
# 
# split(): This is the most common method for splitting a text into a list. You can use this method when you want to split the text into words or substrings based on a specific delimiter, such as a space, comma, or tab.
# 
# partition(): This method splits a text into three parts based on the first occurrence of a delimiter. You can use this method when you want to split the text into two parts and keep the delimiter. For example, you might use partition() to split a URL into its protocol, domain, and path components. The partition() method returns a tuple of three strings.
# 
# splitlines(): This method splits a text into a list of strings based on the newline characters (\n). You can use this method when you want to split a text into lines of text. For example, you might use splitlines() to split a multiline string into individual lines.
# 
# 
# Regular expressions: This is a more powerful method for splitting text into a list, as it allows you to split the text based on more complex patterns. For example, you might use regular expressions to split a text into sentences, based on the presence of punctuation marks. The re module in Python provides a range of functions for working with regular expressions.

# %%
def trim_multiple_spaces(string):

 return " ".join(string.split())


string = input("Enter a string: ")


trimmed_string = trim_multiple_spaces(string)


print("Trimmed string:", trimmed_string)


# %% [markdown]
# 
# Write a program to print a histogram of the frequencies (number of occurrence of each individual letter in the sentence) in form of asterisk for different characters in its input. (input would be string).

# %%


# %%



# %% [markdown]
# # 1.	Give new name to the user by exchanging first and last characters of his/her name.

# %%
def exchange_name(name):
    if len(name) < 2:
        return "Name should have at least two characters"
    else:
        new_name = name[-1] + name[1:-1] + name[0]
        return new_name
    
exchange_name("XYZ")

# %% [markdown]
# # Teacher has entered math marks for all the students in a list. Help her to print the second highest and second lowest marks. Use list data structure.

# %%
def find_second_highest_lowest(marks):
    if len(marks) < 2:
        return "Insufficient data"
    else:
        sorted_marks = sorted(marks)
        second_lowest = sorted_marks[1]
        second_highest = sorted_marks[-2]
        return second_lowest, second_highest
    
    
find_second_highest_lowest([80,78,55,67,23,98,68,55,34,78,90,66,33])

# %% [markdown]
# # 3.	Teacher has to select all the students having roll numbers, that are multiple of 5. Help the teacher. Use list data structure

# %%
def select_students_by_roll_number(roll_numbers):
    multiple_of_5_students = [student for student in roll_numbers if student % 5 == 0]
    return multiple_of_5_students

select_students_by_roll_number([7,8,40,10,4,3,55,63,68,34,54,5,10,50,30])

# %% [markdown]
# # 4. For a given number A which contains only digits 0's and 1's, if it is possible to make all digits same by flipping only one digit, print YES, else print NO

# %%
def is_possible_to_make_same(number):
    digit_count = {'0': 0, '1': 0}
    for digit in str(number):
        digit_count[digit] += 1

    if digit_count['0'] == 1 or digit_count['1'] == 1:
        return "YES"
    else:
        return "NO"
    

is_possible_to_make_same(1100001)

# %% [markdown]
# # 5.	Student names are saved in a tuple. Find the length of each student name.

# %%
# Task 5: Find the length of each student name in a tuple
def length_of_each_student_name(names_tuple):
    return [len(name) for name in names_tuple]

# Task 5: Take user input for student names
students_tuple = tuple(input("Task 5: Enter student names separated by spaces: ").split())
length_of_names = length_of_each_student_name(students_tuple)
print("Task 5: Length of Each Student Name -", length_of_names)


# %% [markdown]
# # 6.	Take a paragraph from some book. Create a dictionary consisting of all the words and its frequency in the given text.
# paragraph = """In a hole in the ground there lived a hobbit. 
# Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, 
# sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort."""
# 

# %%

paragraph = """In a hole in the ground there lived a hobbit. 
Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy smell, nor yet a dry, bare, 
sandy hole with nothing in it to sit down on or to eat: it was a hobbit-hole, and that means comfort."""

words = paragraph.lower().split()
word_frequency_dict = {}

for word in words:
    word = word.strip('.,:')
    if word not in word_frequency_dict:
        word_frequency_dict[word] = 1
    else:
        word_frequency_dict[word] += 1

print("Task 6: Word Frequency Dictionary -", word_frequency_dict)


# %% [markdown]
# # 7.	Create a dictionary from following two lists. The first list will have name of the students and second list will have their corresponding marks.

# %%

names = ["Alice", "Bob", "Charlie", "David"]
marks = [85, 92, 78, 88]

students_dict = dict(zip(names, marks))
print("Task 7: Students Dictionary -", students_dict)


# %% [markdown]
# # 8.	Implement Caesar Cipher using Python Dictionary: Caesar Cipher shift =3 means each letter will be replace by 3 letters a->d, e->h, b->e

# %%

def caesar_cipher(text, shift):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    cipher_dict = {letter: alphabet[(index + shift) % 26] for index, letter in enumerate(alphabet)}
    
    encrypted_text = ''.join([cipher_dict.get(char, char) for char in text.lower()])
    return encrypted_text

plain_text = "hello"
shift = 3
cipher_text = caesar_cipher(plain_text, shift)
print(f"Task 8: Caesar Cipher - Plain Text: {plain_text}, Cipher Text: {cipher_text}")


# %% [markdown]
# # 9.	Create set S1 will all even numbers from 1 to 100. Create set S2 with all squares of numbers 1 to 10. Create the following sets from these two sets i . Union of S1 and S2 ii. Intersection of S1 and S2.

# %%
# Task 9: Create sets and perform operations
S1 = set(range(2, 101, 2))
S2 = {x**2 for x in range(1, 11)}

# i. Union of S1 and S2
union_set = S1.union(S2)

# ii. Intersection of S1 and S2
intersection_set = S1.intersection(S2)

print("Task 9: Union of S1 and S2 -", union_set)
print("Task 9: Intersection of S1 and S2 -", intersection_set)


# %% [markdown]
# # 10.	Create a list in python for storing supermarket bill details and perform the following operations on it:
# ● Add an item to the end of the list 
# ● Insert an item at a given position 
# ● Modify an element by using the index of the element 
# ● Remove an item from the list 
# ● Remove all items from the list 
# ● Slice Elements from a List 
# ● Remove the item at the given position in the list, and return it 
# ● Return the number of times 'x' appear in the list 
# ● Sort the items of the list in place 
# ● Reverse the elements of the list in place

# %%
supermarket_bill = []

supermarket_bill.append("Milk")
supermarket_bill.append("Bread")
supermarket_bill.append("Eggs")

print("Supermarket Bill:", supermarket_bill)

supermarket_bill.insert(1, "Cheese")
print("After Inserting 'Cheese' at Position 1:", supermarket_bill)

supermarket_bill[2] = "Juice"
print("After Modifying Element at Index 2:", supermarket_bill)

# Check if "Bread" is in the list before attempting to remove it
if "Bread" in supermarket_bill:
    supermarket_bill.remove("Bread")
    print("After Removing 'Bread':", supermarket_bill)
else:
    print("'Bread' not found in the list.")

supermarket_bill.clear()
print("After Clearing the List:", supermarket_bill)

supermarket_bill.extend(["Chips", "Soda", "Chocolate"])
print("Updated Supermarket Bill:", supermarket_bill)

sliced_items = supermarket_bill[1:3]
print("Sliced Items:", sliced_items)

# Check if index 1 is within the range before attempting to pop
if 1 < len(supermarket_bill):
    removed_item = supermarket_bill.pop(1)
    print(f"Removed Item at Position 1: {removed_item}")
    print("Updated Supermarket Bill:", supermarket_bill)
else:
    print("Index 1 is out of range.")

item_count = supermarket_bill.count("Chips")
print(f"Count of 'Chips' in the Supermarket Bill: {item_count}")

supermarket_bill.sort()
print("Sorted Supermarket Bill:", supermarket_bill)

supermarket_bill.reverse()
print("Reversed Supermarket Bill:", supermarket_bill)


# %% [markdown]
# # 11.	Write a python program to count positive and negative numbers in a list.

# %%
def count_positive_negative(numbers):
    positive_count = sum(1 for num in numbers if num > 0)
    negative_count = sum(1 for num in numbers if num < 0)
    return positive_count, negative_count

# Example Usage:
numbers_list = [-2, -1, 0, 1, 2]
positive_count, negative_count = count_positive_negative(numbers_list)
print("Positive Count:", positive_count)
print("Negative Count:", negative_count)


# %% [markdown]
# # 12.	Write a python program to sum all the elements in a list.

# %%
def sum_of_elements(numbers):
    return sum(numbers)

# Example Usage:
numbers_list = [1, 2, 3, 4, 5]
total_sum = sum_of_elements(numbers_list)
print("Sum of Elements:", total_sum)


# %% [markdown]
# # 13.	Write a Python program to find the list of words that are longer than n from a given list of words.

# %%
def longer_than_n(words, n):
    return [word for word in words if len(word) > n]


words_list = ["apple", "banana", "grape", "kiwi", "orange"]
n = 4
longer_words = longer_than_n(words_list, n)
print(f"Words Longer than {n} characters:", longer_words)


# %% [markdown]
# # 14.	Write a Python program to find the list in a list of lists whose sum of elements is the highest. Sample lists: [1,2,3], [4,5,6], [10,11,12], [7,8,9] Expected Output: [10, 11, 12]
# 

# %%
def list_with_highest_sum(list_of_lists):
    return max(list_of_lists, key=sum)


lists_of_lists = [[1, 2, 3], [4, 5, 6], [10, 11, 12], [7, 8, 9]]
result_list = list_with_highest_sum(lists_of_lists)
print("List with Highest Sum:", result_list)


# %%



# %% [markdown]
# # XYZ - 123

# %% [markdown]
# # a.	Calculate the Greatest Common Divisor with gcd() function and by writing your own function

# %%
def gcd(a, b):
    
    while b:
        a, b = b, a % b
    return a

gcd_value = gcd(60, 24)  
print(gcd_value) 


# %% [markdown]
# # b.	Write two functions sub  and mul. 
# 
# 1. 	mul function will take any number,multiply it by 3 and return.
# 2.	sub function will take an integer as an input, multiply that number by 3 by calling mul function, subtract 2 from it and return the value
# 

# %%
def mul(num):
 
  return num * 3

def sub(num):
 
  return mul(num) - 2

number = 5


product = mul(number)
print(f"Number multiplied by 3: {product}")


result = sub(number)
print(f"Number multiplied by 3 and then subtracted by 2: {result}")


# %% [markdown]
# # c.	Create a function name student with his default information as his standard and school name with provision that if student wants can change default information

# %%
class Student:
 

  def __init__(self, name="XYZ", standard=16, school_name="MPSTME"):
    self.name = name
    self.standard = standard
    self.school_name = school_name

  def change_name(self, new_name):
    self.name = new_name

  def change_standard(self, new_standard):
    self.standard = new_standard

  def change_school_name(self, new_school_name):
    self.school_name = new_school_name

  def get_info(self):
    return {
      "Name": self.name,
      "Standard": self.standard,
      "School Name": self.school_name,
    }


student1 = Student() 
print(f"Student 1 information: {student1.get_info()}")

student1.change_name("XYZ")  
student1.change_standard(17) 

print(f"Student 1 information after changes: {student1.get_info()}")

student2 = Student("ABC ", 15, "NL COllege")  
print(f"Student 2 information: {student2.get_info()}")

student2.change_school_name("NMIMS")  
print(f"Student 2 information after changes: {student2.get_info()}")


# %% [markdown]
# # d.	Create a lamda function to generate square roots for the numbers given in the list
# 
# 

# %%
numbers = [1, 2, 4, 5, 7, 8, 4]

square_root_lambda = lambda x: x ** 0.5


square_roots = list(map(square_root_lambda, numbers))

print(f"Square roots of the numbers: {square_roots}")


# %% [markdown]
# # e.

# %%
def calculate_bill_amount(furniture_list, cost_list, required_furniture, quantity):
   

    if required_furniture in furniture_list and quantity > 0:
        furniture_index = furniture_list.index(required_furniture)
        cost = cost_list[furniture_index]
        bill_amount = cost * quantity
        return bill_amount
    else:
        print("Invalid furniture or quantity. Bill amount set to 0.")
        return 0

furniture_list = ["Sofa set", "Dining table", "T.V. Stand", "Cupboard"]
cost_list = [20000, 8500, 4599, 13920]


required_furniture = input("Enter the required furniture: ")
quantity = int(input("Enter the quantity: "))


bill_amount = calculate_bill_amount(furniture_list, cost_list, required_furniture, quantity)
print("Bill amount: Rs.", bill_amount)


# %% [markdown]
# # f. Consider the list of courses opted by a Student "John" and available electives at ABC Training Institute:
# courses = ("Python Programming", "RDBMS", "Web Technology", "Software Engg.")
# electives = ("Business Intelligence", "Big Data Analytics")
# Write a Python Program to satisfy business requirements mentioned below:
# 1 List the number of courses opted by John.
# 2 List all the courses opted by John.
# 3 John is also interested in elective courses mentioned above. Print the updated tuple including electives.
# 

# %%
def count_courses(course_list):

  return len(course_list)

def list_courses(course_list):
  
  print(f"Courses: {', '.join(course_list)}")

def update_courses_with_electives(courses, electives):
  
  if input("Is John interested in electives (y/n)? ").lower() == "y":
    return courses + electives
  else:
    print("John remains with his current course list.")
    return courses


courses = ("Python Programming", "RDBMS", "Web Technology", "Software Engg.")
electives = ("Business Intelligence", "Big Data Analytics")

print(f"John has opted for {count_courses(courses)} courses.")
list_courses(courses)

updated_courses = update_courses_with_electives(courses, electives)
if updated_courses is not courses:
  list_courses(updated_courses)


# %% [markdown]
# # g. Consider a scenario from ABC Training Institute.
# The given table shows the marks scored by students of grade XI in Python Programming course.
# Write a Python program to meet the requirements mentioned below:
# a. Display the name and marks for every student.
# b. Display the top two scorers for the course.
# c. Display class average of this course.
# Hint- Implement the solution using a dictionary.
# 

# %%
data = {
    "John": 86.5,
    "Jack": 91.2,
    "Jill": 84.5,
    "Harry": 72.1,
    "Joe": 80.5,
}

for name, marks in data.items():
    print(f"{name:<10} scored {marks:.2f}")


top_two_scores = sorted(data.values(), reverse=True)[:2]
top_two_students = [name for name, marks in data.items() if marks in top_two_scores]
print(f"\nTop two scorers:")

for name, score in zip(top_two_students, top_two_scores):
    print(f"{name:<10} scored {score:.2f}")


class_average = sum(data.values()) / len(data)
print(f"\nClass average: {class_average:.2f}")


# %% [markdown]
# # h. Consider a scenario from ABC Training Institute. Given below are two Sets representing the names of students enrolled for particular course:
# java_course = {"John", "Jack", "Jill", "Joe"}
# python_course = {"Jake", "John", "Eric", "Jill"}
# Write a Python program to list the number of students enrolled for:
# 1)Python course
# 2)Java course only
# 3)Python course only
# 4)Both Java and Python courses
# 5)Either Java or Python courses but not both
# 6)Either Java or Python courses
# 

# %%

java_course = {"John", "Jack", "Jill", "Joe"}
python_course = {"Jake", "John", "Eric", "Jill"}


num_python_students = len(python_course)
print(f"Number of students enrolled in Python course: {num_python_students}")


num_java_only_students = len(java_course) - len(java_course.intersection(python_course))
print(f"Number of students enrolled in Java course only: {num_java_only_students}")

num_python_only_students = len(python_course) - len(python_course.intersection(java_course))
print(f"Number of students enrolled in Python course only: {num_python_only_students}")

num_both_courses_students = len(java_course.intersection(python_course))
print(f"Number of students enrolled in both Java and Python courses: {num_both_courses_students}")


num_either_course_students = len(java_course.union(python_course)) - num_both_courses_students
print(f"Number of students enrolled in either Java or Python courses but not both: {num_either_course_students}")


num_either_course_alt = len(java_course) + len(python_course) - num_both_courses_students
print(f"Number of students enrolled in either Java or Python courses (alternative): {num_either_course_alt}")


# %% [markdown]
# # i. Given a Number in the form of a List of digits , return all possible permutations. For example given [1,2,3] return [1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]
# 

# %%
def permutations(digits):

  if len(digits) == 1:
    yield digits
  else:
    for i, digit in enumerate(digits):
      remaining_digits = digits[:i] + digits[i+1:]
      for permutation in permutations(remaining_digits):
        yield [digit] + permutation

digits = [1, 2, 3]
for permutation in permutations(digits):
  print(permutation)


# %% [markdown]
# # J.Given an unsorted array of integers find the length of the longest consecutive sequence of elements. For example given [100,4,200,1,3,2]. The  Longest consecutive sequence is [1,2,3,4] return the length as 4.

# %%
def longest_consecutive_sequence(nums):

  seen = set(nums)

  longest_sequence = 0

  for num in nums:
  
    if num - 1 not in seen:
   
      current_sequence = 1

      
      while num + current_sequence in seen:
        current_sequence += 1

      longest_sequence = max(longest_sequence, current_sequence)

  return longest_sequence


nums = [100, 4, 200, 1, 3, 2]
longest_sequence = longest_consecutive_sequence(nums)
print(f"Length of longest consecutive sequence: {longest_sequence}")


# %%


# %%


# %% [markdown]
# # XYZ - 123

# %%
import pandas as pd
import numpy as np

# %%
df=pd.read_csv("Titanic.csv")

# %%
df2=pd.read_excel("Gapminder.xlsx")

# %%
dict={
    "1":"Thor",
    "2":"Iron man",
    "3":"Captain America",
    "4":"Loki",
    "5":"Scarlett Witch"
    
    
}

# %%
d=pd.Series(dict)
d

# %%
data={"apples":[3,4,5,6,7], "Oranges":[8,63,2,4,7]}

# %%
d1=pd.DataFrame(data)
d2=pd.DataFrame(data, index=["June","July","August","September","October"])
d2

# %%
df2.columns

# %%
df2.describe()

# %%
df2.index

# %%
df2.shape

# %%
df2.count()

# %%
len(df2)

# %%
df2.set_index("index", inplace=True)

# %%
df2

# %%
df2["country"].unique()

# %%
selected_columns = df2[['country', 'gdp_cap']]
selected_columns

# %%
value_at_2701 = df2.loc[1009:3006, 'country']
print(value_at_2701)

# %%
df2.iloc[3:9,0:2]

# %%
df2.iloc[:,0:3]

# %%
df2.loc[:,[True,False,True,False,True]]

# %%
df.head()

# %%
df.shape

# %%
df["Age"].isnull().count()

# %%
df["Fare"].isnull().count()

# %%
cat_col = [col for col in df.columns if df[col].dtype=='object']
print("Categorical columns: ",cat_col)

# %%
num_col = [col for col in df.columns if df[col].dtype!='object']
print("Numerical columns: ",num_col)

# %%
df[cat_col].nunique()

# %%
df["Pclass"].unique()

# %%
ddf=df.drop(columns=["Name","Ticket"])

# %%
ddf

# %%
df.dropna()

# %%
df.dropna(axis=1)

# %%
dic={
    "Fist":[np.nan,2,5,6,8],
    "Two":[6,3,6,np.nan,np.nan]
}

# %%
dt=pd.Series(dic)
dt

# %%
for i in range(len(df.index)):
    print("Total Nan in row", i+1,":", df.iloc[i].isnull().sum())

# %%
df=pd.read_excel("data.xlsx")

# %%
df

# %%
print(df.to_string())

# %%
new_df=df.dropna()
new_df

# %%
df

# %%
df.fillna(130, inplace=True)
df

# %%
df["calories"].fillna(130, inplace=True)
print(df.to_string())

# %%
y=np.round_(x)
y

# %%
df["calories"].fillna(x,inplace=True)
df

# %%
x1=df["calories"][0]
x1

# %%
print(df["calories"].fillna(x1))

# %%
df["date"]=pd.to_datetime(df['date'])
print(df.to_string())

# %%
for x in df.index:
    if df.loc[x,"Duration"] > 120:
        df.loc[x,"Duration"] = 120

# %%
print(df)

# %%
print(df.duplicated())

# %%



# %% [markdown]
# # XYZ - 123

# %%
import pandas as pd
import numpy as np

# %%
pulse=pd.read_csv("pulse.csv")
churn=pd.read_csv("churn.csv")

# %%
pulse.head()


# %% [markdown]
# # 1.	Select dataset with (.csv file) of sufficiently large size (>300 rows). It should contain columns with different data types.(churnt data set)

# %%
churn.head()

# %%
print("Pulse: ", pulse.shape)
print("Churn: ", churn.shape)

# %%
print("Pulse columns: ", pulse.columns)
print("Churn columns: ", churn.columns)

# %%


# %% [markdown]
# # 2.	Create data frames from data structures (dictionary, list, tuple)

# %%
dict_data=churn.to_dict()
dict_data

# %%
dict_df=pd.DataFrame.from_dict(dict_data)
dict_df

# %%
list_values=churn.values.tolist()
list_cols=churn.columns.tolist()
print(list_cols)
list_df=pd.DataFrame(list_values,columns=list_cols)

# %%
tuple_data=tuple(churn.itertuples(index=False))
print(tuple_data)


# %%
tuple_df=pd.DataFrame(tuple_data)
print(tuple_df)

# %%
my_list=["Nisha","Rewa","Tanmay","Virat","Ananya","Leena","Raj","Kartik"]
df_list=pd.DataFrame(my_list,index=[1,2,3,4,5,6,7,8], columns=["Names"])
print("\n DataFrame using List\n",df_list,'\n')

# %%
my_dict={'Name':["Pooja","Omkar","Nysha","Rupin"],"Age":[24,3,35,22]}
df_dict=pd.DataFrame(my_dict,index=[1,2,3,4])
print("\n DataFrame using dictionary\n", df_dict,'\n')

# %% [markdown]
# # 3.	Create data frames from unformatted text file.

# %%
file1=open(r"C:/Users/mpstme.student/Downloads/exp7/faculty_data.txt","r")
data=file1.readlines()
data2=[]
for i in data:
  
    new=i.replace("\n","")
    data2.append(new)

# %%
data2

# %%
chunks=[data2[x:x+6]for x in range(0,len(data2),6)]
print(chunks)
list_df=pd.DataFrame(chunks)
list_df.head()

# %%
file1=open(r"C:/Users/mpstme.student/Downloads/exp7/faculty_data.txt","r")
df_faculty_data=pd.DataFrame()
name=[]
position=[]
dept=[]
degree=[]
exp=[]
address=[]
i=0
for line in file1:
    if i==0 or i%6==0:
        name.append(line.replace("\n",""))
    elif i%6==1:
        position.append(line.replace("\n",""))
    elif i%6==2:
        dept.append(line.replace("\n",""))
    elif i%6==3:
        degree.append(line.replace("\n",""))
    elif i%6==4:
        exp.append(line.replace("\n",""))
    elif i%6==5:
        address.append(line.replace("\n",""))
    i=i+1

df_faculty_data.insert(0,"Name",name)
df_faculty_data.insert(1,"Position",position)
df_faculty_data.insert(2,"Department",dept)
df_faculty_data.insert(3,"Degree",degree)
df_faculty_data.insert(4,"Experience",exp)
df_faculty_data.insert(5,"Address",address)
df_faculty_data

# %% [markdown]
# # 4.	Obtain metadata of given dataset

# %%
churn.info()

# %% [markdown]
# # 5.	Explore size, shape, data types of each column in the dataset.

# %%
print("Shape",churn.shape)
print("Size", churn.size)
print("Datatype", churn.dtypes)

# %% [markdown]
# # 6.	Perform statistical analysis with min, max, average, standard deviation, percentile etc.

# %%
churn.describe()

# %% [markdown]
# # 7.	Identify null values, missing values in dataset(pulse rate data)

# %%
pulse.head()
pulse.isnull().sum()

# %% [markdown]
# # 8.	Replace missing values by appropriate values.

# %%
df_formatted=pulse.copy()
df_formatted["Date"].fillna("No data", inplace=True)
df_formatted["Pulse"].fillna(df_formatted["Pulse"].mean(), inplace=True)
df_formatted["Maxpulse"].fillna(df_formatted["Maxpulse"].mean(), inplace=True)
df_formatted["Calories"].fillna(df_formatted["Calories"].mean(), inplace=True)
df_formatted

# %% [markdown]
# # 9.	Remove null values from the dataset.

# %%
pulse.dropna()
pulse

# %% [markdown]
# # 10.	Display first 10 rows of dataset.
# 
# 

# %%
pulse.head(10)

# %% [markdown]
# # 11.	Display last 5 rows of dataset.

# %%
pulse.tail()

# %%


# %%



# %% [markdown]
# ### Name: XYZ
# ### Roll No: 123

# %%
import numpy as np
import pandas as pd
import matplotlib

diamonds =pd.read_csv("diamonds.csv")

# %%
diamonds.head()

# %%
diamonds = diamonds.drop("Unnamed: 0",axis=1)

# %%
diamonds.head()

# %%
print(diamonds.shape)

# %%
diamonds.hist(column="carat",color="red")

# %%
diamonds.hist(column="carat",figsize=(8,8),color="blue",bins=50,range=(0,3.5))

# %%
diamonds[diamonds["carat"] > 3.5]

# %%
diamonds["carat"].plot(kind="density",figsize=(8,8),xlim=(0,5));

# %%
carat_table = pd.crosstab(index=diamonds["clarity"],columns="count")
carat_table

# %%
carat_table.plot(kind="bar",figsize=(8,8));

# %%
carat_table = pd.crosstab(index=diamonds["clarity"],columns=diamonds["color"])
carat_table

# %%
carat_table.plot(kind="bar",figsize=(8,8),stacked=True);

# %%
carat_table.plot(kind="bar",figsize=(8,8),stacked=False);

# %%
import pandas as pd
df = pd.read_csv("titanic_clean.csv")

# %%
df.head()

# %% [markdown]
# ## CROSSTABULATION

# %%
df['survived'].value_counts()

# %%
df['survived'].value_counts(normalize=True)

# %% [markdown]
# ## Two Way Tables

# %%
pd.crosstab(df['gender'],df['survived'])

# %%
pd.crosstab(df['gender'],df['survived'],normalize='index')

# %%
pd.crosstab(df['gender'],df['survived'],normalize='columns')

# %%
mwc =df['gender'].copy()
mwc[df['age']<=16]='child'
pd.crosstab(mwc,df['survived'],normalize='index')

# %% [markdown]
# ## Three-way tables

# %%
categories = [df['class'],mwc]
pd.crosstab(categories,df['survived'])

# %%
pd.crosstab(df['survived'],categories,normalize='columns')

# %%
by_class = df.groupby('class')
by_class

# %%
len(by_class)

# %%
first_class_passengers = by_class.get_group('1st')
first_class_passengers.head()

# %%
first_again = df[df['class']=='1st']
first_again.head()

# %% [markdown]
# ## Aggregating

# %%
import numpy as np
class_means = df.groupby('class').aggregate(np.mean)
class_means

# %%
import numpy as np
class_means = by_class.aggregate(np.mean)
class_means

# %%
class_means = by_class.mean()
class_means





# %% [markdown]
# # XYZ - 123

# %%
import pandas as pd

# %%
df1=pd.read_excel("Masterdata.xlsx")

# %%
df1

# %% [markdown]
# # 1.	What is the maximum score of an employee in each of the department?

# %%
max_score_per_dept = df1.groupby('dept')['sport score'].max()
print(max_score_per_dept)


# %% [markdown]
# # 2.	What is name of the employee who's age is minimum in each of the cities?

# %%
min_age_per_city = df1.groupby('city')['age'].idxmin()
employee_names_min_age = df1.loc[min_age_per_city, ['name', 'city']]
print(employee_names_min_age)


# %% [markdown]
# # 3.	Does all the departments have participation from employee age group between 20 to 30?

# %%
age_range_participation = df1.groupby('dept')['age'].apply(lambda x: all((x >= 20) & (x <= 30)))
print(age_range_participation)


# %% [markdown]
# # 4.	What is the average score of an employee in each department and city?

# %%
average_score_per_dept_city = df1.groupby(['dept', 'city'])['sport score'].mean()
print(average_score_per_dept_city)


# %% [markdown]
# # 5.	What is the designation of the youngest player who score highest in cricket? 

# %%
cricket_players = df1[df1['sport'] == 'cricket']
highest_score_cricket = cricket_players['sport score'].max()
youngest_highest_scorer = cricket_players[cricket_players['sport score'] == highest_score_cricket]['age'].idxmin()
youngest_highest_scorer_name = df1.loc[youngest_highest_scorer, 'name']
youngest_highest_scorer_designation = df1.loc[youngest_highest_scorer, 'designation']
print("Name of the youngest player who scored highest in cricket:", youngest_highest_scorer_name)
print("Designation of the youngest player who scored highest in cricket:", youngest_highest_scorer_designation)


# %% [markdown]
# # 6.	What is the city and department of the eldest player who score highest in any of the sport?

# %%
highest_scorer = df1.loc[df1['sport score'].idxmax()]
eldest_highest_scorer_city_dept = (highest_scorer['city'], highest_scorer['dept'])
print("City and department of the eldest player who scored highest:", eldest_highest_scorer_city_dept)


# %% [markdown]
# # 7.	Which department performed best on the basis of average score city wise

# %%
avg_score_city_dept = df1.groupby(['dept', 'city'])['sport score'].mean()
best_performing_dept_citywise = avg_score_city_dept.groupby(level='dept').agg(['idxmax', 'max'])
print("Department performed best on the basis of average score city-wise:")
for dept, (city, max_avg_score) in best_performing_dept_citywise.iterrows():
    print(f"Department: {dept}, City: {city}, Max Average Score: {max_avg_score:.2f}")


# %% [markdown]
# # Task 2: Perform following normalization on datasets mentioned in folder of this experiment. (Emp_info)
# 
# 

# %% [markdown]
# # 1.	Maximum absolute scaling technique 
# 
# 

# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MaxAbsScaler

emp_info = pd.read_excel('Emp.xlsx')


max_abs_scaler = MaxAbsScaler()
emp_info_max_abs_scaled = emp_info.copy()
emp_info_max_abs_scaled[['age', 'salary', 'performance score']] = max_abs_scaler.fit_transform(emp_info[['age', 'salary', 'performance score']])

print("Normalized Data (Maximum Absolute Scaling):")
print(emp_info_max_abs_scaled)
print()

emp_info_max_abs_scaled[['age', 'salary', 'performance score']].plot(kind='bar')
plt.title('Maximum Absolute Scaling')
plt.xlabel('Index')
plt.ylabel('Scaled Value')
plt.show()


# %% [markdown]
# # 2.	The min-max feature scaling technique
# 

# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

emp_info = pd.read_excel('Emp.xlsx')

min_max_scaler = MinMaxScaler()
emp_info_min_max_scaled = emp_info.copy()
emp_info_min_max_scaled[['age', 'salary', 'performance score']] = min_max_scaler.fit_transform(emp_info[['age', 'salary', 'performance score']])

print("Normalized Data (Min-Max Feature Scaling):")
print(emp_info_min_max_scaled)
print()

emp_info_min_max_scaled[['age', 'salary', 'performance score']].plot(kind='bar')
plt.title('Min-Max Feature Scaling')
plt.xlabel('Index')
plt.ylabel('Scaled Value')
plt.show()


# %% [markdown]
# # 3.	The z-score method
# 

# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


emp_info = pd.read_excel('Emp.xlsx')

z_score_scaler = StandardScaler()
emp_info_z_score_scaled = emp_info.copy()
emp_info_z_score_scaled[['age', 'salary', 'performance score']] = z_score_scaler.fit_transform(emp_info[['age', 'salary', 'performance score']])


print("Normalized Data (Z-Score Method):")
print(emp_info_z_score_scaled)
print()


emp_info_z_score_scaled[['age', 'salary', 'performance score']].plot(kind='bar')
plt.title('Z-Score Method')
plt.xlabel('Index')
plt.ylabel('Scaled Value')
plt.show()



# %% [markdown]
# ### Name: XYZ
# ### Roll no: 123

# %% [markdown]
# # Task 1

# %% [markdown]
# ## 1. Read different data files as NumPy array (text, csv, tsv, excel file etc.)

# %% [markdown]
# ### a. Read tumor_data file and perform following operations

# %%
import numpy as np
import pandas as pd
tumor_data = pd.read_csv('Tumor_data.csv')

# %% [markdown]
# ### i. Find the mean of all the parameters and display

# %%
mean_values = tumor_data.mean()
print("Mean of all Parameters:")
print(mean_values)

# %% [markdown]
# ### ii. Display all the tumors greater than mean radius

# %%
mean_radius = mean_values['radius']
tumor_greater_than_mean_radius = tumor_data[tumor_data['radius']> mean_radius]
print("\n Tumors with radius greater than mean radius:")
print(tumor_greater_than_mean_radius)

# %% [markdown]
# ### iii. Display tumor data where radius is less then its mean  but the perimeter is high compared to its mean.

# %%
mean_perimeter = tumor_data['perimeter'].mean()

high_perimeter_low_radius = tumor_data[(tumor_data['radius'] < mean_radius) & (tumor_data['perimeter'] > mean_perimeter)]
print("\n Tumors with radius is less then its mean but the perimeter is high compared to its mean.")
print(high_perimeter_low_radius)

# %% [markdown]
# ## b. Read Wine_data file and perform following operations

# %%
import numpy as np
import pandas as pd
wine_data = pd.read_excel('Wine_data.xlsx')

# %% [markdown]
# ### i. Display the wine where alcohol contain is high but magnesium content is low.

# %%
high_alcohol_low_magnesium = wine_data[(wine_data['Alcohol'] > wine_data['Alcohol'].mean()) & (wine_data['Magnesium'] < wine_data['Magnesium'].mean())]

print(high_alcohol_low_magnesium)
print(high_alcohol_low_magnesium.shape)

# %% [markdown]
# ### ii. Find out the range of Hue in wine

# %%
Hue_range = wine_data['Hue'].max() - wine_data['Hue'].min()
print('\nRange of Hue in wine:',Hue_range)

# %% [markdown]
# ### iii. Is there correlation exist between alcohol percentage and color intensity ? if not then display the odd ones.

# %%
wine_data[" Colour Intensity"].corr(wine_data["Alcohol"])

# %%
import seaborn as sns
corr_matrix=wine_data.corr()
print(corr_matrix)
sns.heatmap(corr_matrix, annot=True)

# %% [markdown]
# ## Task 2

# %% [markdown]
# ### Practice Code

# %%
from PIL import Image
image = Image.open('Image.png')
print(image.format)
print(image.size)
print(image)

# %%
from numpy import asarray
img_data = asarray(image)
print(type(img_data))
print(img_data.shape)
print(img_data)

# %%
import matplotlib.pyplot as plt
plt.hist(img_data)

# %%
from PIL import Image
from numpy import asarray
import matplotlib.pyplot as plt
image2 = Image.open('Image.png')
imgray = image2.convert(mode = 'L')
img_data2 = asarray(imgray)

print(img_data2.shape)
print(img_data2)
plt.hist(img_data2)


# %%
import pandas as pd
df= pd.read_csv("used_cars_data.csv")
df

# %%
df.head()

# %%
df.tail()

# %%
df.columns

# %%
df.info()

# %%
df.describe

# %%
df.drop(columns=["S.No."],inplace=True)

# %%
df.head()

# %%
#separating categorical and numerical variables
#HISTOGRAM IS FOR NUMERICAL DATA WHILE COUNT PLOT IS FOR CATEGORICAL DATA
num_column=[]
cat_column=[]

for i in df.columns: 
    if df[i].dtype=="object":
        cat_column.append(i)
    else:
        num_column.append(i)

print("Numerical Variables: ",num_column)
print("Categorical Variables: ",cat_column)

# %%
df.isnull().sum()

# %%
#changed the columns to numerical values
df['Engine'] = df['Engine'].str.extract('(\d+)').astype(float)
df['Mileage'] = df['Mileage'].str.extract('(\d+)').astype(float)
df['Power'] = df['Power'].str.extract('(\d+)').astype(float)

# %%
df.head()

# %%
#introducing new column car age to know the age of the car

from datetime import date
date.today().year
df['Car_Age'] = date.today().year-df['Year']
df.head()

# %%
#creating features
#retreiving brand name, model create new columnsdf['Brand']= df.Name.str.split().str.get(0)
df['Model']= df.Name.str.split().str.get(1) + ' ' + df.Name.str.split().str.get(2)
df[['Name', 'Brand','Model']]

# %%
df.head()

# %% [markdown]
# # Data Cleaning/Wrangling

# %%
print(df.Brand.unique())
print(df.Brand.nunique())

# %%
df['Brand'].replace({"ISUZU": "Isuzu","Mini": "Mini Cooper","Land" : "Land Rover"},inplace=True)
print(df['Brand'])
df.head()

# %%
print(df.Brand.unique())

# %% [markdown]
# # eda univariate analysis

# %%
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# %%
for col in num_column:
    print(col)
    print('Skew: ', round(df[col].skew(),2))
    plt.figure(figsize = (15,4))
    plt.subplot(1,2,1)
    df[col].hist(grid=False)
    plt.ylabel('count')
    plt.subplot(1,2,2)
    sns.boxplot(x=df[col])
    plt.show()

# %%
# log or normalisation
def log_transform(data, cols):
    for colname in cols:
        if (df[colname] == 0).any():
            df[colname + '_log'] = np.log(df[colname] + 1)
        else:
            df[colname + '_log'] = np.log(df[colname])
    df.info()
log_transform(df, ['Kilometers_Driven', "Price"])

# %%
fig, axes = plt.subplots(3,2, figsize = (18,18))
fig.suptitle('Bar plot for all categorical variables in the dataset')
sns.countplot(ax = axes[0, 0], x = "Fuel_Type", data = df, color = 'blue', order = df['Fuel_Type'].value_counts().index);
sns.countplot(ax = axes[0, 1], x = "Transmission", data = df, color = 'blue', order = df['Transmission'].value_counts().index);
sns.countplot(ax = axes[1, 0], x = "Owner_Type", data = df, color = 'blue', order = df['Owner_Type'].value_counts().index);
sns.countplot(ax = axes[1, 1], x = "Location", data = df, color = 'blue', order = df['Location'].value_counts().index);
sns.countplot(ax = axes[2, 0], x = "Brand", data = df, color = 'blue', order = df['Brand'].head(20).value_counts().index);
sns.countplot(ax = axes[2, 1], x = "Model", data = df, color = 'blue', order = df['Model'].head(20).value_counts().index);
 
axes[1][1].tick_params(labelrotation=45);
axes[2][0].tick_params(labelrotation=90);
axes[2][1].tick_params(labelrotation=90);

# %%

 ''')
    

   