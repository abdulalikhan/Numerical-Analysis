from django.shortcuts import render
from django.http import HttpResponse
from .models import FormData, Method, Result

from sympy import var
from sympy import sympify, pprint
from sympy import Integral
from sympy import integrate
from sympy.utilities.lambdify import lambdify
# Create your views here.

name = "Numerical Integration"


def index(request):
    method1 = Method("Composite Trapezoidal Rule")
    method2 = Method("Composite Simpson Rule")
    methods = [method1, method2]
    field1 = FormData("f_str", "f(x)")
    field2 = FormData("n", "n")
    field3 = FormData("a", "lower limit (a)")
    field4 = FormData("b", "upper limit (b)")
    fields = [field1, field2, field3, field4]
    return render(request, 'input_form.html', {'name': name, 'methods': methods, 'fields': fields})


def comp_trapezoidal(f, n, a, b):
    h = (b-a)/float(n)
    # initializing approx_result with 0, as it will store our final result of approximation
    approx_result = 0.0
    # we are also initializing the summation variable with 0, so that we can use it like a running total
    summation = 0.0
    # the Composite Trapezoidal Rule calculation begins here
    approx_result = f(a)+f(b)
    for i in range(1, n):
        summation += f(a+(i*h))
    approx_result = approx_result + 2*summation
    approx_result = (h/2.0)*approx_result
    return approx_result


def comp_simpson(f, n, a, b):
    # if the number of intervals is odd, we must exit as Composite Simpson Rule cannot be used in this case
    if (n % 2 != 0):
        print("Error: Composite Simpson's rule can only be applied to even values of n")
        exit()
    h = (b-a)/float(n)

    # initializing approx_result with 0, as it will store our final result of approximation
    approx_result = 0.0
    # we are also initializing the summations with 0, so that we can use them as running totals
    summation1 = 0.0
    summation2 = 0.0

    # the Composite Simpson Rule calculation begins here
    approx_result = f(a)+f(b)
    for i in range(1, n//2):
        summation1 += f(a+(2*i*h))
    for i in range(1, (n//2)+1):
        summation2 += f(a+((2*i-1)*h))
    approx_result = approx_result + 2*summation1 + 4*summation2
    approx_result = (h/3.0)*approx_result
    return approx_result


def result(request):
    if request.method == 'POST':
        x = var('x')
        method = request.POST['method']
        f_str = request.POST['f_str']
        expr = sympify(f_str)
        f = lambdify(x, expr)
        n = int(request.POST['n'])
        a = float(request.POST['a'])
        b = float(request.POST['b'])
        h = (b-a)/float(n)
        if (method == "Composite Trapezoidal Rule"):
            approx = comp_trapezoidal(f, n, a, b)
        elif (method == "Composite Simpson Rule"):
            approx = comp_simpson(f, n, a, b)

        true_value = integrate(f_str, (x, a, b))
        true_error = abs(true_value-approx)
        result1 = Result("f'(x₀)", str(approx))
        result2 = Result("True Error", str(true_error))
        results = [result1, result2]
        return render(request, 'result.html', {'name': name, 'results': results})
    else:
        return render(request, 'input_form.html', {'name': name, 'methods': methods, 'fields': fields})
