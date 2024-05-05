import argparse
import sympy
from sympy import Not, simplify, symbols
from sympy.abc import A, B, C, D
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy.logic.boolalg import Or, And
from itertools import product
from quine_mccluskey.qm import QuineMcCluskey
import re

def parse_expression(expression:str):
    '''
    Parse a boolean expression string into a symbolic form
    '''