from django.shortcuts import render
from django.http import HttpResponse
from .models import FormData, Method, Result

from sympy import var
from sympy import sympify
from sympy import diff
from sympy.utilities.lambdify import lambdify
# Create your views here.

name = "Numerical Differentiation"


def index(request):
    method1 = Method("Three-point Midpoint Formula")
    methods = [method1]
    field1 = FormData("f_str", "f(x)")
    field2 = FormData("h", "h")
    field3 = FormData("x0", "x₀")
    fields = [field1, field2, field3]
    return render(request, 'input_form.html', {'name': name, 'methods': methods, 'fields': fields})


def three_point_mid(f, x0, h):
    x0 = float(x0)
    h = float(h)
    return (f(x0 + h) - f(x0 - h)) / (2 * h)


def result(request):
    if request.method == 'POST':
        x = var('x')
        f_str = request.POST['f_str']
        expr = sympify(f_str)
        f = lambdify(x, expr)
        h = request.POST['h']
        x0 = request.POST['x0']

        approx = three_point_mid(f, x0, h)

        derivativeF = diff(f_str, x)
        true_value = derivativeF.subs(x, x0)
        true_error = abs(true_value-approx)
        result1 = Result("f'(x₀)", str(approx))
        result2 = Result("True Error", str(true_error))
        results = [result1, result2]
        return render(request, 'result.html', {'name': name, 'results': results})
    else:
        return render(request, 'input_form.html', {'name': 'Numerical Differentiation', 'methods': methods, 'fields': fields})
