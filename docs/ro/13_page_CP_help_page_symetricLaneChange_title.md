# Symetric lange change

  
Symmetric lane change is used in multitool courses and tells the driver in which lane he has to drive after the turn.  
This is a bit hard to understand so let's have a look at two examples.  


![Image](../assets/images/regularchange_0_0_1020_765.png)

  
When the symmetric lane change is turned off, the vehicle stays on it's offset lane.  
That means he always drives left or right from the course.  
This ensures, that the helpers are not driving alongside each other.  
There won't be a risk of on conflict with another driver.  


![Image](../assets/images/symetricchange_0_0_1020_765.png)

  
If symmetric lane change is turned on, left and right will be exchanged (but not shown in the HUD).  
Vehicles can conflict with each other, when they drive towards each other.  
What is the advantage of symmetric lange change then ?  
If you have a look at the order of the lanes, from left to right, it will be clear:  
Without symetric change: left, right, left, right - it is almost like skipping a lane.  
With symetric change: left, right, right, left - from left to right, one lane after the other.  
In the example with the Combine it means, no Combine will have fruit left and right of its lane.  


