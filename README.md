## Self-Driving AI Cars Project

This project involves programming the mechanics of a moving car and distance sensors to the limits of the track. The sensor readings are then used as input to a neural network with two output neurons, one responsible for turning and the other for speed control. Cars appear on the track in generations, and when all the cars in a generation have an accident, the one that has travelled the greatest distance is selected and its neural network is mutated (random numbers are added to the weights of the network with a certain probability). The evolution of the cars using the algorithm I programmed (the code can be seen in the 'own-network' branch) can be observed [here](https://www.youtube.com/watch?v=jz81Rb7Ouso). Unfortunately, the car evolution process with the simple mutation algorithm I wrote is not very efficient, it is quite random. I got much better results using the NEAT package. Learning with the NEAT algorithm on a more difficult track can be seen [here](https://www.youtube.com/watch?v=l3oIitRD7Wg).

### Inspiration

This project draws inspiration from the following repositories:

- [NeuralNine/ai-car-simulation](https://github.com/NeuralNine/ai-car-simulation/)
- [gniziemazity/self-driving-car](https://github.com/gniziemazity/self-driving-car/)

