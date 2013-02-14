#!/bin/evn python
# -*- coding: utf-8 -*-
# vim: set et ai sta sw=2 ts=2 tw=0:
"""
assert functions:
 - assertTrue(expression)
 - assertFalse(expression)
 - assertEquals(expected, expression)
 - assertNotEquals(expected, expression)
 - assertException(exceptionType, function)
 - assertNoException(function)

to pass a function, you can use lambda expression like:
  assertException(lambda: myfunction())
"""
def assertTrue(expression):
  "Expect the expression to be true"
  assert expression, "'{0}' was expected to be true".format(expression)
def assertFalse(expression):
  "Expect the expression to be false"
  assert (not expression), "'{0}' was expected to be false".format(expression)
def assertEquals(expected, expression):
  "Expect that the expression equals to the expected value"
  assert expression == expected, "'{0}' expected, got '{1}'".format(expected, expression)
def assertNotEquals(expected, expression):
  "Expect that the expression does not equals to the expected value"
  assert expression != expected, "'{0}' not expected, got '{1}'".format(expected, expression)
def assertException(exceptionType, function):
  "Expect that the function trigger an exception of type exceptionType"
  triggered = False
  try:
    function()
  except BaseException as e:
    if isinstance(e, exceptionType):
      triggered = True
  assert triggered, "Exception '{0}' expected with '{1}'".format(exceptionType, function.__doc__)
def assertNoException(function):
  "Expect that the function does not trigger any exception"
  triggered = False
  unExpectedE = None
  try:
    function()
  except BaseException as e:
    unExpectedE = e
    triggered = True
  assert (not triggered), "Exception '{0}' was not expected with '{1}'".format(unExpected, function.__doc__)

# Unit test
if __name__ == '__main__':
  assertTrue(True)
  assertFalse(False)
  assertEquals(0, 2 - 2)
  assertNotEquals(1, 2 - 2)
  assertException(ZeroDivisionError, lambda: 1 / 0)
  assertNoException(lambda: 1)