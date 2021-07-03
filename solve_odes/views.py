from django.shortcuts import render
from django.http import HttpResponse
from .models import FormData, Method, Result

from sympy import var
from sympy import sympify, pprint
from sympy.utilities.lambdify import lambdify
# Create your views here.

name = "Solve Ordinary Differential Equations"


def index(request):
    method1 = Method("Euler Method")
    method2 = Method("Huen Method")
    method3 = Method("Runge-Kutta Method")
    methods = [method1, method2, method3]
    field1 = FormData("fdash_str", "y'")
    field2 = FormData("f_str", "y")
    field3 = FormData("x0", "x₀")
    field4 = FormData("y0", "y₀")
    field5 = FormData("h", "h")
    field6 = FormData("x_reqd", "the value of x at which to approximate y")
    fields = [field1, field2, field3, field4, field5, field6]
    return render(request, 'input_form.html', {'name': name, 'methods': methods, 'fields': fields})


def euler(fdash, f, x0, y0, h, x_reqd):
    # data is a list of lists that will store all the table entries
    data = []
    # this_row is a list that will store the entries for the current iteration
    this_row = []
    # the initial value of x will be x0
    x_curr = x0
    # the initial value of y_prev will be y0
    y_prev = y0
    # i is used to keep track of the number of iterations (it is used to populate the 'n' column)
    i = 0
    while (x_curr <= x_reqd):
        true_val = f(x_curr)
        # if this is the first value of x, the true error will be zero (no true error)
        # otherwise, true error = true value - previous value of y'
        if (x_curr == x0):
            this_row = [i, x_curr, y_prev, true_val, 0]
        else:
            this_row = [i, x_curr, y_prev, true_val, abs(true_val-y_prev)]
        # append this row to the data list (a list of lists)
        data.append(this_row)
        # Euler Method's calculation of y_approx begins here
        y_curr = y_prev + h*fdash(x_curr, y_prev)
        y_prev = y_curr
        # update x for the next iteration by adding the common difference to it
        x_curr = x_curr+h
        i += 1
    return data


def huen(fdash, f, x0, y0, h, x_reqd):
    # data is a list of lists that will store all the table entries
    data = []
    # this_row is a list that will store the entries for the current iteration
    this_row = []
    # the initial value of x will be x0
    x_curr = x0
    # the initial value of y_prev will be y0
    y_prev = y0
    # i is used to keep track of the number of iterations (it is used to populate the 'n' column)
    i = 0
    while (x_curr <= x_reqd):
        true_val = f(x_curr)
        # if this is the first value of x, the true error will be zero (no true error)
        # otherwise, true error = true value - previous value of y'
        if (x_curr == x0):
            this_row = [i, x_curr, y_prev, true_val, 0]
        else:
            this_row = [i, x_curr, y_prev, true_val, abs(true_val-y_prev)]
        # append this row to the data list (a list of lists)
        data.append(this_row)
        # Huen Method's calculation of k1,k2,k3 and y_approx begins here
        k1 = fdash(x_curr, y_prev)
        k2 = fdash(x_curr+((1/3)*h), y_prev+((1/3)*k1*h))
        k3 = fdash(x_curr+((2/3)*h), y_prev+((2/3)*k2*h))
        y_curr = y_prev + (1/4)*(k1+3*k3)*h
        y_prev = y_curr
        # update x for the next iteration by adding the common difference to it
        x_curr = x_curr+h
        i += 1
    return data


def runge_kutta(fdash, f, x0, y0, h, x_reqd):
    # data is a list of lists that will store all the table entries
    data = []
    # this_row is a list that will store the entries for the current iteration
    this_row = []
    # the initial value of x will be x0
    x_curr = x0
    # the initial value of y_prev will be y0
    y_prev = y0
    # i is used to keep track of the number of iterations (it is used to populate the 'n' column)
    i = 0
    while (x_curr <= x_reqd):
        true_val = f(x_curr)
        # if this is the first value of x, the true error will be zero (no true error)
        # otherwise, true error = true value - previous value of y'
        if (x_curr == x0):
            this_row = [i, x_curr, y_prev, true_val, 0]
        else:
            this_row = [i, x_curr, y_prev, true_val, abs(true_val-y_prev)]
        # append this row to the data list (a list of lists)
        data.append(this_row)
        # Runge Kutta's calculation (k1, k2, k3, k4 and y_approx) begins here
        k1 = h*fdash(x_curr, y_prev)
        k2 = h*fdash(x_curr+(h/2), y_prev+((1/2)*k1))
        k3 = h*fdash(x_curr+(h/2), y_prev+((1/2)*k2))
        k4 = h*fdash(x_curr+h, y_prev+k3)
        y_curr = y_prev + (1/6)*(k1+(2*k2)+(2*k3)+k4)
        y_prev = y_curr
        # update x for the next iteration by adding the common difference to it
        x_curr = x_curr+h
        i += 1
    return data


def result(request):
    if request.method == 'POST':
        x = var('x')
        y = var('y')
        method = request.POST['method']
        f_str = request.POST['f_str']
        fdash_str = request.POST['fdash_str']
        expr = sympify(fdash_str)
        fdash = lambdify([x, y], expr)
        expr = sympify(f_str)
        f = lambdify(x, expr)
        x0 = float(request.POST['x0'])
        y0 = float(request.POST['y0'])
        h = float(request.POST['h'])
        x_reqd = float(request.POST['x_reqd'])
        if (method == "Euler Method"):
            data = euler(fdash, f, x0, y0, h, x_reqd)
        elif (method == "Huen Method"):
            data = huen(fdash, f, x0, y0, h, x_reqd)
        elif (method == "Runge-Kutta Method"):
            data = runge_kutta(fdash, f, x0, y0, h, x_reqd)
        headings = ["n", "x", "w", "y", "|Yn-Wn|"]
        return render(request, 'result_table.html', {'name': name, 'headings': headings, 'data': data})
    else:
        return render(request, 'input_form.html', {'name': name, 'methods': methods, 'fields': fields})
