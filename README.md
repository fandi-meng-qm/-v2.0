# DeadlyHotel-v2.

1. GameManager: // control the game flow
Map
Role[]
init(){
   init map, role, score
}
loop(){
   action of roles
   update the game state   
}
finish(){
}

2. Map: //  
Tile[][] 

3. Role: // 
name
position
equip[]
action(boolean){
   true: auto play
   false: wait human's command
}

4.GameState: // 
Map
Role[]
Record[]
OtherInfo // such as which agent moves in next step

5. GameGUI extends GameManager:
init(){
   super.init()
   updateGraphic()
}
loop(){
   super.loop()
   updateGraphic()
}
finish(){
   super.finish()
   updateGraphic()
}
