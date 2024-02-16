## Self-Driving AI Cars Project

This project involves programming the mechanics of a running car and distance sensors to the boundaries of a track. Subsequently, the sensor readings are utilized as input to a neural network featuring two output neurons, where one is responsible for turning and the other for speed control. Cars emerge on the track in populations, and when all the cars in a population have crashed, the one that traveled the greatest distance is selected, and its neural network is mutated (random numbers are added to the weights of the network with a certain probability). The evolutions of the cars on the track can be observed [here](https://www.youtube.com/watch?v=jz81Rb7Ouso). Unfortunately, the process of car evolution is not very efficient, it is quite random. In the future, I intend to use more advanced evolutionary algorithms such as NEAT.

### Inspiration

This project draws inspiration from the following repositories:

- [NeuralNine/ai-car-simulation](https://github.com/NeuralNine/ai-car-simulation/)
- [gniziemazity/self-driving-car](https://github.com/gniziemazity/self-driving-car/)

### Future Plans

In the future, more advanced evolutionary algorithms such as NEAT will be employed to enhance the efficiency and effectiveness of the car evolution process on the track.
