Assignments 3

In this task we were asked to construct a weighted directed graph similar to the previous task 2.
 We were asked to implement two interfaces, using 2 classes we opened and detailed on both

The first class we implemented is 
DiGraph 
	which basically stores all the graph properties within it.
	Within this class we have created two dictioneries: one of nodes and one of edges.
	Nodes- the keys are the keys of the nodes and the values are the nodes themselves(node_data type) - each node includes id ,pos, edges_in(dict) and edges_out(dict). 
	NodeCount- counts the number of vertices in the graph
	EdgeCount- counts the amount of our edges in the graph
	mc- counts the amount of our actions in the graph

	all the usually function: remove node/edge, add node/edge, v size, e size.

GraphAlgo class where it performs some functions:
	
	init- which is the initialization of the graph and whether it exists or not,
	
	get_graph- returns the graph we have
	
	save_ to_json- we were asked to save the graph and upload it to the Json file.All the data we have at the nodes which are themselves, the key and pos and the end and the edges which are src target and weight to the Json file.
	
	load_from_json function- we will do the opposite we did in the save_to_json function just the opposite we will call the string we want to read and load our information.

	the shortest_path function-
		created a dictionry stackmap, and started going over the neighbors of a starting vertex, from the neighbor with the lowest weight to the highest.
		for each of them putting their key and weight in the node_weight dictionry  + the weight of the initial code (equal to 0) . added them to the stackmap and update them in the node_weight.
		In the next iteration we went over the neighbors of each of the nodes in stampmap, and started with the vertex with the lowest tag in the list. And again we passed by his neighbors,
		For each of them - if its tag is greater than the distance (= the weight of the side between the vertex and the neighbor + the tag of the vertex from which we reached the neighbor),
		we will update the weight to be the distance.
		we put each of the neighbors in stackmap.
		And again we will look at the stackmap, and take the vertex with the lowest weight (no matter at what stage I inserted it, unless there are two vertices with the same tag)
		And we will pass on the neighbors of the vertex the same actions we did on the neighbors of the previous vertex.
		Once the vertex with the lowest weight in the stackmap is the target vertex, it means that we have found the shortest route to it and we have already gone through all the ways that there is a starting vertex to it

		we will save in for each node, the previous vertex from which we reached the node in the ShortestPathMap, and thus the route will be saved for us.
		The path is constructed using a list, to which we add the target vertex to the beginning,
		and we will continue each time to add the pre field of the first vertex in the list to the beginning.
		we can be sure route was built that checks the short route following which we reached the destination vertex.
		Then we return its weight and the list and finish using the function. If there is no path to this vertex we will return that the distance is infinite and empty list.
		Complexity: O (| E | + | V | log | V |) Because every time you go through a neighbor you update or add its vertex and tag, it happens | E | Times and complication Add / update is log (| V).
		In addition each vertex is taken out of the queue once, and this happens | V | Expenditure times and complexity is log (| V).


	component_components-
	Use the Tarjan algorithm but in an iterative manner.
	Go through each vertex in the graph, and go to each vertex over its neighbors.
	If we have not yet visited this neighbor, we will put the parent vertex in the work dictionary with the number of neighbors we have already passed +1,
	and then we will also put the neighbor in the work dictionary.
	We will save in the recurse variable we added to a neighbor, and then we will exit the aisle on the neighbors, and re-enter the aisle on the neighbor's neighbors.
	If we have already visited the neighbor (according to its value in the disc dictionary) and it is in the st stack, meaning we have not finished taking care of it,
	So in case the disc value of that neighbor is smaller than the low of the original vertex,
	We will update the original vertex to its low value to be the neighbor's disc.
	This will continue until we reach a state where the disc value of a particular vertex is equal to its low value.
	And it will happen when we reach a leaf or a vertex that we have already passed over all its neighbors.
	We will start to take out what work all the vertices according to FILO.
	 Once we get to the vertex we're working on,
	We will know that we have created a binding element with all the vertices we have taken out up to it.
	We will add each such element to the list of -com elements and return it
	the complexity is O(|E|+|V|) because we pass each neighbor of each node - |E|, and after that we pass each component nodes: total nodes in all component- |V|.
	
	component_component(id1)-
	we doing the same thing we did in component_components, but now we start to pass from the id1 node, and once we create component includes this node,
	we will stop computes another components and return id1 component.
	
	plot_graph- we will create a drawing of all the nodes and edges and tilt them to draw if a particular vertex has no place we will randomly place it for the purpose of positioning in its graph, to connect and use the previous arrow function.
