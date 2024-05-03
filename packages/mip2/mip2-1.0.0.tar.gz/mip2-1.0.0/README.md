# mip2

mip2 is a mip modeling tool that imitates gurobi's api syntax, making mip modeling easier.

The mip2 backend supports cbc, gurobi, scip, and copt solvers, and will support highspy. if there you have other solver requirements, please let me know.

mip2 is not a re implemented modeling tool, but is integrated based on py-mip, pyscipopt, coptpy and other tools. Therefore, when you need to use a specific solver, you need to install the corresponding tool package.

**Importance**: mip2 not support all features but have the most common features that you need. if you have any requirements, please let me know.

**CBC,GUROBI** 

mip2 use mip package as modeling tool in backend, so you need to install mip package.
```sh
pip install mip
```

**SCIP** 

like cbc, gurobi, mip2 use pyscipopt as modeling tool in backend, so you need to install pyscipopt package.
```sh
conda install --channel conda-forge pyscipopt
```

**COPT** 

mip2 use coptpy as modeling tool in backend.
```sh
pip install coptpy
```

**HIGHS**

highspy now if not easy to using, so mip2 using pyscipopt to modeling and then using highspy to solve the model. so you need to install pyscipopt and highspy.
```sh
conda install --channel conda-forge pyscipopt
pip install highspy
```

## examples
Here is a simple example.

```python

from mip2.api import Model, Param

m = Model(solver_name="CBC")
x = m.addVars([1,2,3], vtype="I", name="x")

m.addConstr(x[1] == 10)
m.addConstr(x.sum() <= 20)
m.addConstr(x.sum() >= 15)

m.setObjective(x.sum())
m.setParam(Param.MIPGap, 0.01)
m.setParam(Param.TimeLimit, 10)
status = m.optimize()

print("x value is:", [x[i].x for i in [1,2,3]])
print("obj value is:", m.objVal)
print("model status is:", status)
```



## api
Here is the api list, like gurobi api, you can read gurobi document to know how to using mip2.

### Model
- Model(name: str = "", solver_name: str = "SCIP")
    - solver_name: str, default is "SCIP", solver name, support "CBC", "GUROBI", "SCIP", "COPT"
    - name: str, default is "mip2", model name

#### addVar
```
addVar(self, vtype: str = "C", lb: float = 0, ub: float = INF, name: str = "") -> Var
```

#### addVars
```
addVars(self, indexs, vtype: str = "C", lb: float = 0.0, ub: float = INF, name: str = "") -> TupleDict[int, Var]
```

#### addConstr
```
addConstr(self, expr, name: str = "")
```

#### addGenConstrIndicator
use big m method to add indicator constraint, that if x>0 then y=1 else y=0. so y is a binary variable.
```
addGenConstrIndicator(self, x, y, big_m: float, tiny_b: float = 0.00001, name: str = "")
```

#### addGenConstrAnd
same as addGenConstrIndicator, but x is a list of binary variables. if all x is 1 then y=1 else y=0. all x is binary variables and y is a binary variable.

Use the big m method to implement this logic.
```
addGenConstrAnd(self, xlist, y, name: str = "")
```

#### addGenConstrAbs
add absolute value constraint, that y = |x|, y is a continuous variable.

Use the big m method to implement this logic.
```
addGenConstrAbs(self, x, y, big_m: float = INF, name: str = "")
```

#### addGenConstRelu
add relu constraint, that y = max(0, x), y is a continuous variable.

Use the big m method to implement this logic.
```
addGenConstRelu(self, x, y, big_m: float = INF, name: str = "")
```

#### setMipStart
set mip start value, that you can set variable value before optimize.
```
setMipStart(self, start: Dict[str, float])
```

#### setObjective
set objective function, that you can set objective function before optimize.
```
setObjective(self, lin_expr, sense: str = "MIN")
```

#### setObjectiveN
Multi-objective solving using hierarchical optimization. This means solving the first objective first, then adding the first objective value as a constraint to the model, solving the second objective, and so on.


```
setObjectiveN(self, lin_expr, index: int, weight: float, mip_gap: float = 100.0, time_limit: int = 90000_0000)
```

#### optimize
optimize and return status. all status is OPTIMIZE, FEASIBLE, INFEASIBLE, TIMEOUT, OTHER.
```
optimize(self) -> str

```

#### optimizeN(self)
optimize multi objective problem.
```
optimizeN(self)
```

#### read
read model from file.
```
read(self, file: str)
```


#### write
write model to file.
```
write(self, file: str)
```

