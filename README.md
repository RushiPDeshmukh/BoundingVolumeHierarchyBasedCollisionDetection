# BoundingVolumeHierarchyBasedCollisionDetection
Bounding Volume Hierarchy is used to represent the objects in a 3D euclidean space. Collision Detection between this complex detailed structures is implemented in this project. This algorithm is fast, modular and generalised. It can be used with different types of bounding volume and the premitive tests. It can be expanded to the 3D 6DoF interactions from the current 2D 2DoF version.


Working:


Run simulator.py and wait for the pygame window to pop up. This window will be titled “Haptics Simulator”. Once this window pops up, a 2D world representation can be seen. Use key w to make the avatar car travel up. Use key s to make the avatar car travel down. Use key a to make the avatar car travel left. Use key d to make the avatar car travel right. The keys can be held down to perform the same action continuously, like holding the key d down will make the avatar move right with a certain speed and it will stop only once the key is let go.
In the simulation you can interact with the world by moving towards them. If the avatar object collides with the world object then the background color changes from GREY to WHITE.



