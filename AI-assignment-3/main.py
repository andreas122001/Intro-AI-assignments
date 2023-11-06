from Assignment import CSP, create_sudoku_csp, create_map_coloring_csp, print_sudoku_solution

csp = create_sudoku_csp("./medium.txt")

solution = csp.backtracking_search()

if solution:
    print_sudoku_solution(solution)
else:
    print("No solution")
