# GoSafe---Contact-minimization-in-public-transport

Google Maps / SBB / ZVV etc all propose routes when you have an itinerary inquiry. Their algorithm is based on a metric that minimizes the time required for travel. It simply shows the fastest route.

During these times, social distencing has been shown to be one of the most effective ways to slow down the spread of the virus. The virus spreads from person to person in their close proximity. Self quarantine is one way to combat this, however sometimes people are still required to take public transport. 

Our approach is to distribute the people as much as possible in public transport to avoid clusters and to avoid people getting unnecessarily close to each other. 
For this we created a program that does not only find the fastest connection between two points but also distributes the people. This has the effect that sometimes people might not be able to take the most efficient connection, however it proposes them a route that reduces the contact they have to other commuters. 

This simple code is a proof of concept that one could find very efficient solutions to the travel time optimization problem while reducing the amount of people that share one transportation vehicle. 

The code is is built as follows. 
There is a simulated city, composed of nodes that represent train/bus/tram stations. Each node is connected to at least one other node. Between two nodes at least one transportation vehicle transports passengers. This vehicle has a maximum capacity of people that it can hold. A certain amount of time is required to go from one node to another. This simulates our city. 

A first passenger gets proposed a route, based on pure time optimization metrics. As long as other passengers don't share some part of the way, their optimal travel way is calculated like this as well. However if some share a common path, then their proposed way will not only depend on time considerations but also on how many people are already using this specific connection. The system will then propose a path for them that less people are using. We opted for a non-linear impact, meaning that each additional passenger taking the same route as others will be weighted more heavily.

For this to work in a real life scenario some data about the current position and wanted travel route is required from the passengers. In our simulation we have this knowledge for each passenger, in reality one would have to compose this data from ticket sales and itinerary inquiries in the SBB app and potentially from localisation data given by phone companies. We would then update our simulated city to represent the actual puplic transportation system from the city in question. 



