# use bfs to find the shortest path between two nodes of a graph
def shortest_path(graph, start, goal):
	explored = set()

    # queue holds all paths found so far
	queue = [[start]]
	
	# If the desired node is
	# reached
	if start == goal:
		return [goal]
	
	# Loop to traverse the graph
	# with the help of the queue
	while queue:
		path = queue.pop(0)
		node = path[-1]

		#  not visited?
		if node not in explored:
			neighbours = graph[node]
			
			# grow paths to include each neighbor
			for neighbour in neighbours:
				new_path = list(path)
				new_path.append(neighbour)
				queue.append(new_path)
				
				# check if neighbur is the goal
				if neighbour == goal:
					return new_path
			explored.add(node)
	return []

