from sympy import mod_inverse
import numpy as np
from datetime import datetime

# 
# tonelli_shanks() :- implementation of Tonelli-Shanks algorithm
# 
# @n : the quadratic residue for which the solution 
# is to be found
# 
# @p : the prime number with respect to which the
# solution has to be found
# 
# finds x : (x*x) ≡ n mod p 
# where p = 4k + 3
# 

def tonelli_shanks(n, p):
  x = p-1
  s = 0
  while(x%2!=1):
    x=x//2
    s+=1
  q = (p-1)//(2**s)
  z = 2
  while(isResidue(z,p)):
    z+=1
  M = s
  c = pow(z,q,p)
  t = pow(n,q,p)
  R = pow(n,(q+1)/2,p)
  while(True):
    if(t==0):
      return 0
    if(t==1):
      return R
    i = 0
    while(pow(t,2**i,p)!=1):
      i+=1
    b = pow(c,2**(M-i-1),p)
    M = i
    c = pow(b,2,p)
    t = (t*c)%p
    R = (R*b)%p

# 
# generatePoints() :- generates points according to the 
# given curve parameters and stores them in file
# 
# @a, @d : parameters of the Short Weiestrass Curve
# 
# @p : the prime number with respect to which the
# points have to be found
# 
# @fname : takes the name of the file to be created
# to store the points (default : points.txt)
# 
# The general equation for Short Weiestrass Curve is :
# 
# y^2 = x^3+ax+d
# 
# 
# 
# opens a new file with given name
# 
# for every x from 0 to p, checks if the corresponding
# value of y^2 is a quadratic residue
# 
# if it is, uses appropriate function to find y
# depending on nature of p
# 
# writes the points into the opened file
# 

def generatePoints(a, d, p, start=0):
  #Creating the output file
  x_array = []
  y_array = []

  # $$$
  if start > p:
    start = 0

  # take at max 1000 points
  for x in range(start, min(start+1000, p)):
      fx = ((x*x*x)+(a*x)+d)%p   #finding values of y^2 mod p for every integer value of x in range
      if(isResidue(fx, p) or fx == 0):
        # 4k+3 form
        if((p-3)%4 == 0):
          y = pow(fx, (p+1)/4, p)   #euler's method
        # 4k+1 form
        else:
          y = tonelli_shanks(fx,p)   #Tonneli-Shank's method

        x_array.append(x)
        y_array.append(y)
        if fx != 0:
          x_array.append(x)
          y_array.append(p-y)
  return (x_array,y_array)

#
# pow() :- helper function to execute
# fast exponentiation with modular operation
# 
# @a, @b : base and index values respectively for
# exponentiation operation
# 
# @m : the value to be used for modular part of
# the operation
# 
# returns a^b mod m
# time complexity : O(logn)
#
 
def pow(a, b, m):   
  if(b == 0):
    return 1%m
  ans = pow(a, b//2, m) 
  if(b%2 == 0):
    return (ans*ans)%m
  else:
    return ((ans*ans)%m*a)%m

# 
# isResidue() :- helper function to check whether a 
# given number is a quadratic residue with respect to 
# a given prime number
# 
# @x : the number to check for quadratic residue
# 
# @p : the prime number with respect to which the
# condition has to be checked
# 
# Euler's criterion for QR:
# 
# if x^((p-1)/2) ≡ 1 mod p, then x is QR
# if x^((p-1)/2) ≡ -1 mod p, then x is QNR
# 

def isResidue(x, p):
  return pow(x,(p-1)/2,p) == 1

# 
# addpoints() :- function to perform addition operation 
# on two points in the curve using the affine addition formula
# 
# @p1, @p2 : two input points to perform addition operation
# 
# formula for affine addition is as follows:-
# 
# gradient = (y2 - y1) / (x2 - x1)
# x3 = (gradient^2) - x2 - x1
# y3 = (gradient*(x2 - x3)) - y2
# 
# this formula is altered for finite field and used here
# final answer is returned as a tuple of (x3,y3)
# 

def addpoints(a,d,p,p1,p2):
  # print(p1)
  # print(p2)   

  try:
    gradient = (p2[1]-p1[1])*mod_inverse((p2[0]-p1[0]),p)
    x = (gradient**2-p2[0]-p1[0])%p
    y = (gradient*(p2[0]-x)-p2[1])%p
  except:
    print("-*-*-*-*-*-*-*Inverse does not exist, please change the point!!*-*-*-*-*-*-*-")
    return (0,-1)
  return (x,y)

# 
# subtractpoints() :- function to subtract one given point from another
# 
# @p1, @p2 : two inputs to perform subtraction operation (p1-p2)
# 
# it can be deduced from original curve equation that the 
# additive inverse of (x,y) is (x,-y)
# 
# ∴ (x1,y1) - (x2,y2) = (x1,y1) + (-x2,y2)
# 
# here we are directly using this fromula and a previously defined 
# function addpoints to perfrom the subtraction operation
# 

def substractpoints(a,d,p,p1,p2):
  p3 = (p2[0],-1*p2[1])
  return addpoints(a,d,p,p1,p3)

# 
# doublepoint() :- function to perform doubling operation 
# on a given point in the curve using the affine addition formula
# 
# @p1 : two input points to perform addition operation
# 
# substituting the value of x2 and y2 with x1 and y1
# respectively and substituting values from original 
# equation of the curve gives us the following formula
# 
# lamda = ((3*x1*x1) + a) / (2*y1)
# x = (lamda^2) - (2*x1)
# y = (lamda*(x1-x)) - y1
# 
# this formula is altered for finite field and used here
# final answer is returned as a tuple of (x,y)
# 

def doublepoint(a,d,p,p1):
  try:                      
    lam = (3*p1[0]*p1[0]+a)*mod_inverse((2*p1[1]),p)                      
    x = (lam**2-2*p1[0])%p
    y = ((lam*(p1[0]-x))-p1[1])%p
  except:
    print("-*-*-*-*-*-*-*Inverse does not exist, please change the point!!*-*-*-*-*-*-*-")
    return (0,-1)
  return (x,y)

# 
# multiplypoint() :- function to perform scalar multiplication
# with a given a point and scalar value
# 
# @p1, @scalar : the input point and scalar value to perform
# saclar multiplication of point
# 
# multiplication is perfromed with repeated addition operations 
# with some optimization using doubling and addition method
# time complexity : O(logn)
# 

def multiplypoint(a,d,p,p1, scalar):
  pt = (0,1)

  if scalar == 1:
    pt = p1
  elif scalar%2 == 1:
    pt = addpoints(a,d,p,p1,multiplypoint(a,d,p,p1,scalar-1))
  else:
    pt = multiplypoint(a,d,p,doublepoint(a,d,p,p1),scalar//2)
  return pt

