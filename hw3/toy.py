from scipy.optimize import rosen, differential_evolution
bounds = [(0,2), (0, 2), (0, 2), (0, 2), (0, 2)]
result = differential_evolution(rosen, bounds)
# result = differential_evolution(rosen, bounds, updating='deferred', workers=2)
print(result.x, result.fun)
print('haha')