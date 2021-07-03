from django.shortcuts import render
from django.http import HttpResponse
from .models import FormData, Method, Result

from sympy import var
from sympy import sympify
from sympy.utilities.lambdify import lambdify
from sympy import diff
# Create your views here.

name = "Solve Non-Linear Equations"


def index(request):
    method1 = Method("Bisection")
    method2 = Method("Regula-Falsi")
    method3 = Method("Secant")
    method4 = Method("Newton-Raphson")
    methods = [method1, method2, method3, method4]
    field1 = FormData("f_str", "f(x)")
    field2 = FormData("a", "lower endpoint of interval (a)")
    field3 = FormData("b", "upper endpoint of interval (b)")
    field4 = FormData("tol", "tolerance value")
    field5 = FormData("n", "the maximum number of iterations")
    fields = [field1, field2, field3, field4, field5]
    return render(request, 'input_form.html', {'name': name, 'methods': methods, 'fields': fields})


def bisection(f, a, b, f_a, f_b, tol, n):
    # data is a list of lists that will store all the table entries
    data = []
    # this_row is a list that will store the entries for the current iteration
    this_row = []

    # if the signs of f(a) and f(b) are opposite, then the Intermediate Value Theorem has been violated
    # the process must be exited in this case
    if ((f_a) < 0 and (f_b) < 0) or ((f_a) >= 0 and (f_b) >= 0):
        print("f(a) and f(b) must have opposite signs")
        exit()
    # if update_flag = True -> a was updated in the last iteration
    # if update_flag = False -> b was updated in the last iteration
    update_flag = True
    success_flag = False
    for i in range(0, n):
        f_a = f(a)
        f_b = f(b)
        c = (a+b)/2
        f_c = f(c)
        # est_error -> estimated error (| c[i] - c[i-1] |)
        if (i == 0):
            # no estimated error for the first iteration
            est_error = 0
        else:
            if (update_flag):
                est_error = abs(c-a)
            else:
                est_error = abs(c-b)
        this_row = [i, a, b, c, f_c, est_error]
        data.append(this_row)
        if ((f_c == 0) or (i != 0 and est_error < tol)):
            # display the table of results if either f(c)=0 or the estimated error is within the tolerance value
            return data
            success_flag = True
            break
        if (((f_a)*(f_c)) < 0):
            b = c
            update_flag = False
        else:
            a = c
            update_flag = True
    # if we could not determine an approximate value accurate to the tolerance value, or we have exceeded the maximum number
    # of iterations, then the method has failed
    if (success_flag == False):
        print("The method failed after {0} iterations.".format(i+1))
    return data


def regula_falsi(f, a, b, f_a, f_b, tol, n):
    # data is a list of lists that will store all the table entries
    data = []
    # this_row is a list that will store the entries for the current iteration
    this_row = []

    # if the signs of f(a) and f(b) are opposite, then the Intermediate Value Theorem has been violated
    # the process must be exited in this case
    if ((f_a) < 0 and (f_b) < 0) or ((f_a) >= 0 and (f_b) >= 0):
        print("f(a) and f(b) must have opposite signs")
        exit()
    # if update_flag = True -> a was updated in the last iteration
    # if update_flag = False -> b was updated in the last iteration
    update_flag = True
    success_flag = False
    for i in range(0, n):
        f_a = f(a)
        f_b = f(b)
        c = ((a*f_b)-(b*f_a))/(f_b - f_a)
        f_c = f(c)
        # est_error -> estimated error (| c[i] - c[i-1] |)
        if (i == 0):
            # no estimated error for the first iteration
            est_error = 0
        else:
            if (update_flag):
                est_error = abs(c-a)
            else:
                est_error = abs(c-b)
        this_row = [i, a, b, c, f_c, est_error]
        data.append(this_row)
        if ((f_c == 0) or (i != 0 and est_error < tol)):
            # display the table of results if either f(c)=0 or the estimated error is within the tolerance value
            return data
            success_flag = True
            break
        if (((f_a)*(f_c)) < 0):
            b = c
            update_flag = False
        else:
            a = c
            update_flag = True
    # if we could not determine an approximate value accurate to the tolerance value, or we have exceeded the maximum number
    # of iterations, then the method has failed
    if (success_flag == False):
        print("The method failed after {0} iterations.".format(i+1))
    return data


def secant(f, a, b, f_a, f_b, tol, n):
    # data is a list of lists that will store all the table entries
    data = []
    # this_row is a list that will store the entries for the current iteration
    this_row = []

    # if the signs of f(a) and f(b) are opposite, then the Intermediate Value Theorem has been violated
    # the process must be exited in this case
    if ((f_a) < 0 and (f_b) < 0) or ((f_a) >= 0 and (f_b) >= 0):
        print("f(a) and f(b) must have opposite signs")
        exit()
    success_flag = False
    for i in range(0, n):
        f_a = f(a)
        f_b = f(b)
        c = ((a*f_b)-(b*f_a))/(f_b - f_a)
        f_c = f(c)
        # est_error -> estimated error (| c[i] - c[i-1] |)
        if (i == 0):
            # no estimated error for the first iteration
            est_error = 0
        else:
            est_error = abs(c-b)
        this_row = [i, a, b, c, f_c, est_error]
        data.append(this_row)
        if ((f_c == 0) or (i != 0 and est_error < tol)):
            # display the table of results if either f(c)=0 or the estimated error is within the tolerance value
            return data
            success_flag = True
            break
        # For the next iteration, the current b becomes a, and the current c becomes b
        a = b
        b = c
    # if we could not determine an approximate value accurate to the tolerance value, or we have exceeded the maximum number
    # of iterations, then the method has failed
    if (success_flag == False):
        print("The method failed after {0} iterations.".format(i+1))
    return data


def newton_raphson(f, f_str, a, b, f_a, f_b, tol, n):
    # data is a list of lists that will store all the table entries
    data = []
    # this_row is a list that will store the entries for the current iteration
    this_row = []

    # if the signs of f(a) and f(b) are opposite, then the Intermediate Value Theorem has been violated
    # the process must be exited in this case
    if ((f_a) < 0 and (f_b) < 0) or ((f_a) >= 0 and (f_b) >= 0):
        print("f(a) and f(b) must have opposite signs")
        exit()
    success_flag = False
    c = (a+b)/2
    c_prev = c
    for i in range(0, n):
        c = float(c)
        c_prev = float(c_prev)
        f_c = f(c_prev)
        derivativeF = diff(f_str, x)
        true_value = derivativeF.subs(x, c_prev)
        c = c_prev - (f(c_prev)/true_value)
        # est_error -> estimated error (| c[i] - c[i-1] |)
        if (i == 0):
            # no estimated error for the first iteration
            est_error = 0
        else:
            est_error = abs(c-c_prev)
        this_row = [i, c, f_c, est_error]
        data.append(this_row)
        if ((f_c == 0) or (i != 0 and est_error < tol)):
            # display the table of results if either f(c)=0 or the estimated error is within the tolerance value
            return data
            success_flag = True
            break
        c_prev = c
    # if we could not determine an approximate value accurate to the tolerance value, or we have exceeded the maximum number
    # of iterations, then the method has failed
    if (success_flag == False):
        print("The method failed after {0} iterations.".format(i+1))
    return data


def result(request):
    if request.method == 'POST':
        x = var('x')
        y = var('y')
        method = request.POST['method']
        f_str = request.POST['f_str']
        expr = sympify(f_str)
        f = lambdify(x, expr)
        a = float(request.POST['a'])
        b = float(request.POST['b'])
        tol = float(request.POST['tol'])
        n = int(request.POST['n'])
        f_a = f(a)
        f_b = f(b)
        if (method == "Bisection"):
            data = bisection(f, a, b, f_a, f_b, tol, n)
            headings = ["n", "a", "b", "c", "f(c)", "|Cn-Cn-1|"]
        elif (method == "Regula-Falsi"):
            data = regula_falsi(f, a, b, f_a, f_b, tol, n)
            headings = ["n", "a", "b", "c", "f(c)", "|Cn-Cn-1|"]
        elif (method == "Secant"):
            data = secant(f, a, b, f_a, f_b, tol, n)
            headings = ["n", "Xn-1", "Xn", "Xn+1", "f(Xn+1)", "|Xn-Xn-1|"]
        elif (method == "Newton-Raphson"):
            data = newton_raphson(f, f_str, a, b, f_a, f_b, tol, n)
            headings = ["n", "Xn", "f(Xn)", "|Xn-Xn-1|"]
        return render(request, 'result_table.html', {'name': name, 'headings': headings, 'data': data})
    else:
        return render(request, 'input_form.html', {'name': name, 'methods': methods, 'fields': fields})
