# Lane switch

  
Lane switching is used on multitool courses and tells the helper, in which lane he should drive after the turn.  
With lane switch active, the vehicle changes the side after each turn.  
This is a bit hard to understand so let's have a look at two examples.  


![Image](../assets/images/regularchange_0_0_1020_765.png)

  
If switching lanes is turned off, the vehicle stays on the same side during the entire course where it was started.  
If it started on the leftmost lane, it will always stay in the leftmost lane. This avoids conflicts with other drivers,  
but vehicles on the inside of the turn (leftmost for left turns, rightmost for right turns) will have to make tighter  
turns as they continue on the adjacent lane.  


![Image](../assets/images/symetricchange_0_0_1020_765.png)

  
If switching lanes is active, for example for two vehicles, vehicle A left and vehicle B right, after then turn the lanes are switched.  
That means A is then on the right and B is then on the left.  
The advantage is that all vehicles have the same turn width and therefore the same distance to drive.  
For combines this setting is important, as it makes sure the pipe stays out of the fruit and won't reach in another lane.  
Disadvantage is that vehicles have a chance to collide with each other when they drive towards each other on nearby lanes.  
  
If you have a look at the order of the lanes, from left to right, it will be clear:  
Without symmetric change: left, right, left, right - it is almost like skipping a lane.  
With symmetric change: left, right, right, left - from left to right, one lane after the other.  
In the example with the Combine it means, no Combine will have fruit left and right of its lane.  


