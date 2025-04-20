"""
Mathematical utilities
"""

from typing import Callable, Tuple

class RootFinder:
    """Class for numerical root-finding methods"""
    
    @staticmethod
    def bisection(func: Callable[[float], float], a: float, b: float, tol: float = 1e-8, max_iter: int = 100) -> Tuple[float, int]:
        """
        Bisection method for finding roots
        
        Args:
            func: Function for which to find roots where func(x) = 0
            a: Lower bound of interval
            b: Upper bound of interval
            tol: Tolerance for convergence
            max_iter: Maximum number of iterations
            
        Returns:
            Tuple of (root, iterations)
        """
        fa = func(a)
        fb = func(b)
        
        # Check if the root is in the interval
        if fa * fb > 0:
            raise ValueError("Function must have opposite signs at interval endpoints")
            
        iterations = 0
        
        while (b - a) > tol and iterations < max_iter:
            # Bisect the interval
            c = (a + b) / 2
            fc = func(c)
            
            if abs(fc) < tol:
                return c, iterations
                
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
                
            iterations += 1
            
        # Return midpoint as the root
        return (a + b) / 2, iterations
    
    @staticmethod
    def newton_raphson(func: Callable[[float], float], derivative: Callable[[float], float], x0: float, 
                       tol: float = 1e-8, max_iter: int = 100) -> Tuple[float, int]:
        """
        Newton-Raphson method for finding roots
        
        Args:
            func: Function for which to find roots where func(x) = 0
            derivative: Derivative of the function
            x0: Initial guess
            tol: Tolerance for convergence
            max_iter: Maximum number of iterations
            
        Returns:
            Tuple of (root, iterations)
        """
        x = x0
        iterations = 0
        
        while iterations < max_iter:
            f_x = func(x)
            
            if abs(f_x) < tol:
                return x, iterations
                
            df_x = derivative(x)
            
            # Avoid division by zero
            if abs(df_x) < 1e-10:
                raise ValueError("Derivative too small, possible stationary point")
                
            # Update x
            x_new = x - f_x / df_x
            
            # Check for convergence
            if abs(x_new - x) < tol:
                return x_new, iterations
                
            x = x_new
            iterations += 1
            
        # Return the last approximation
        return x, iterations
    