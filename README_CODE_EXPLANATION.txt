Start with the initial setup. start_nodes, end_nodes, capacities, true_time are the parameters that define your city. They need to have the same length. For example the first position in the array shows that node 0 is connected to node 1 with a vehicle that holds at most 2 passengers and requires 2 time intervals for this travel. You can change this how you want, just make sure that each node has at least one way to connect with each other node (not neccessarily directly). Just like in a real life scenario.

We differentiate between cases where one passenger is the only one to make a certain travel inquiry and cases where two or more people share at least some part of their way. It does not have to be the exact same way it suffices if some part of it overlaps. Then their inquiry is optimized to find the most efficient way of travel.
In the non-unique case where at least two people share some part of the way, we introduced a non-linear time punishment. This way we could still optimize over one single variable. 

Our initial setup is based on random itinerary inquiries. You are free to play around with those parameters or choose fixed ones to represent a specific scenario.

Example of how to call the script:

python safestroute.py --start_nodes=[0, 1, 2, 3, 4] --end_nodes=[1, 2, 3, 4, 0] --capacities=[5, 5, 5, 2, 2] --true_time=[4, 6, 7, 10, 5]