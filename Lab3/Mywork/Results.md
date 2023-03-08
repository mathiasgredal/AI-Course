| Algorithm                   | Goal   | Path    | Cost | Number of explored nodes |
|-----------------------------|--------|---------|------|--------------------------|
| A-Star                      | (K)    | A-D-H-K | 11   | 14                       |
| A-Star                      | (L)    | A-D-H-L | 10   | 12                       |
| A-Star                      | (K, L) | A-D-H-L | 10   | 12                       |
| Greedy (GBFS) (Alpha 1000)  | (K, L) | A-D-H-L | 10   | 3                        |
| Weighted A-Star (Alpha 1.2) | (K, L) | A-D-H-L | 10   | 11                       |
| Weighted A-Star (Alpha 1.5) | (K, L) | A-D-H-L | 10   | 8                        |
| Weighted A-Star (Alpha 2.5) | (K, L) | A-D-H-L | 10   | 4                        |
| Greedy (GBFS) (Alpha 1000)  | (K)    | A-D-H-K | 10   | 4                        |
| Weighted A-Star (Alpha 1.2) | (K)    | A-D-H-K | 10   | 13                       |
| Weighted A-Star (Alpha 1.5) | (K)    | A-D-H-K | 10   | 10                       |
| Weighted A-Star (Alpha 2.5) | (K)    | A-D-H-K | 10   | 5                        |

## Conclusion
For this tree, Greedy best first provides an optimal cost path in the fewest number of fringes possible.

However we would not have known that this path was optimal without running A-star.

The weighted A-star reduces the number of nodes explored, but compromises on the promise of the optimal path.
However the closer the heuristic functon is to the true cost from that node to the goal, the more confident we can be in the optimality of the weighted A-star.