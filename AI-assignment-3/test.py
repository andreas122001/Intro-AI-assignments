from Assignment import CSP

csp = CSP()
csp.add_variable("a", [1,2,3])
csp.add_variable("b", [1,2,3])
csp.add_all_different_constraint(['a', 'b'])

