#####################   TEMPLATE   ##################### 
import bpy
import os
    
    
list_spoiler = bpy.data.collections['Alettoni'].objects
dest = "C:/Users/500/Desktop/Render/"

bpy.data.scenes[0].render.resolution_x = 1920 #1280
bpy.data.scenes[0].render.resolution_y = 1080 #720
bpy.context.scene.render.film_transparent = True
bpy.context.scene.render.image_settings.color_mode = 'RGBA'

# hide everything in list_spoiler
for obj in list_spoiler:
    obj.hide_render = True
    
i = 1

# unhide and render one at a time
for obj in list_spoiler:
    obj.hide_render = False
    bpy.data.scenes[0].render.filepath = os.path.join(dest, str(i) + '.png')
    bpy.ops.render.render(write_still=True)
    obj.hide_render = True
    i=i+1





#####################   COMPLETO   ##################### 
import bpy
import os
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)
mydb.database = "carscryptonovusracing"
mycursor = mydb.cursor()

dest = "C:/Users/500/Desktop/Render/"
#fileSalvataggio = open("C:/Users/500/Desktop/Render/fileSalvataggioCarModel1.txt","w")


list_wheels = bpy.data.collections['Wheels'].objects
list_spoilers = bpy.data.collections['Alettoni'].objects
list_bumpers = bpy.data.collections['Front'].objects
list_InterfaceTopSpeed = bpy.data.collections['InterfaceTopSpeed'].objects
list_InterfaceHandling = bpy.data.collections['InterfaceHandling'].objects
list_InterfaceAccelleration = bpy.data.collections['InterfaceAcceleration'].objects
list_InterfaceBreakPower = bpy.data.collections['InterfaceBreakPower'].objects
list_InterfaceBumper = bpy.data.collections['InterfaceBumper'].objects
list_InterfaceSpoiler = bpy.data.collections['InterfaceSpoiler'].objects
list_InterfaceWheel = bpy.data.collections['InterfaceWheel'].objects
list_InterfaceLivery = bpy.data.collections['InterfaceLivery'].objects



bpy.data.scenes[0].render.resolution_x = 1920 #1280
bpy.data.scenes[0].render.resolution_y = 1080 #720
bpy.context.scene.render.film_transparent = True
#bpy.context.scene.render.image_settings.color_mode = 'RGBA'

# hide everything in list_wheels
for obj in list_wheels:
    obj.hide_render = True
# hide everything in list_spoiler
for obj in list_spoilers:
    obj.hide_render = True
# hide everything in list_bumpers
for obj in list_bumpers:
    obj.hide_render = True
# hide everything in list_InterfaceTopSpeed
for obj in list_InterfaceTopSpeed:
    obj.hide_render = True
# hide everything in list_InterfaceHandling
for obj in list_InterfaceHandling:
    obj.hide_render = True
# hide everything in list_InterfaceAccelleration
for obj in list_InterfaceAccelleration:
    obj.hide_render = True
# hide everything in list_InterfaceBreakPower
for obj in list_InterfaceBreakPower:
    obj.hide_render = True
# hide everything in list_InterfaceBumper
for obj in list_InterfaceBumper:
    obj.hide_render = True
# hide everything in list_InterfaceSpoiler
for obj in list_InterfaceSpoiler:
    obj.hide_render = True
# hide everything in list_InterfaceWheel
for obj in list_InterfaceWheel:
    obj.hide_render = True
# hide everything in list_InterfaceLivery
for obj in list_InterfaceLivery:
    obj.hide_render = True

"""
i = 1


# unhide and render
for objWheels in list_wheels:
    #abilita wheels al render
    bpy.data.collections['Wheels'].objects['Wheel' + str(i) + 'b'].hide_render = False
    bpy.data.collections['Wheels'].objects['Wheel' + str(i) + 'f'].hide_render = False
    #obj.hide_render = False
    
    for objSpoiler in list_spoilers:
        #abilita objSpoiler al render
        objSpoiler.hide_render = False
        
        for objBumper in list_bumpers:
            #abilita objBumper al render
            objBumper.hide_render = False
            
            for objITopSpeed in list_InterfaceTopSpeed:
                #abilita objITopSpeed al render
                objITopSpeed.hide_render = False
                
                for objIHandling in list_InterfaceHandling:
                    #abilita objIHandling al render
                    objIHandling.hide_render = False
                    
                    for objIAccelleration in list_InterfaceAccelleration:
                        #abilita objIAccelleration al render
                        objIAccelleration.hide_render = False
                        
                        for objIBreakPower in list_InterfaceBreakPower:
                            #abilita objIBreakPower al render
                            objIBreakPower.hide_render = False
                            
                            for objIBumper in list_InterfaceBumper:
                                #abilita objIBumper al render
                                objIBumper.hide_render = False
                                
                                for objISpoiler in list_InterfaceSpoiler:
                                    #abilita objISpoiler al render
                                    objISpoiler.hide_render = False
                                    
                                    for objIWheel in list_InterfaceWheel:
                                        #abilita objIWheel al render
                                        objIWheel.hide_render = False
                                        
                                        for objILivery in list_InterfaceLivery:
                                            #abilita objILivery al render
                                            objILivery.hide_render = False
                                            
                                            #FAI ORA CHE HAI ATTIVO LA ROBA GIUSTA IL RENDER!!!!
                                            
                                            #fai il render / salva sul database(?)
                                            #bpy.data.scenes[0].render.filepath = os.path.join(dest, str(i) + '.mkv')
                                            #bpy.ops.render.render(animation=True, write_still=True)
                                            
                                            print(i)
                                            
                                            fileSalvataggio.write(
                                             'Wheel' + str(i) + 'b' + ";" + 
                                             'Wheel' + str(i) + 'f' + ";" + 
                                             objSpoiler.name + ";" +
                                             objBumper.name + ";" +
                                             objITopSpeed.name + ";" +
                                             objIHandling.name + ";" +
                                             objIAccelleration.name + ";" +
                                             objIBreakPower.name + ";" +
                                             objIBumper.name + ";" +
                                             objISpoiler.name + ";" +
                                             objIWheel.name + ";" +
                                             objILivery.name + ";" +
                                             '\n'
                                             )
                                            
                                            i=i+1
                                            
                                            objILivery.hide_render = True
                                        
                                        objIWheel.hide_render = False
                                    
                                    objISpoiler.hide_render = False
                                
                                objIBumper.hide_render = False
                            
                            objIBreakPower.hide_render = True
                        
                        objIAccelleration.hide_render = True
                    
                    objIHandling.hide_render = True
                
                objITopSpeed.hide_render = True
            
            objBumper.hide_render = True
            
        objSpoiler.hide_render = True
    
    #Disabilita tutto per il render
    #obj.hide_render = True
    bpy.data.collections['Wheels'].objects['Wheel' + i + 'b'].hide_render = True
    bpy.data.collections['Wheels'].objects['Wheel' + i + 'f'].hide_render = True
"""
k = 1
nr_wheel = 1

# TXT FILE SAVING ALGORITHM
for objLiveryFake in list_InterfaceLivery:
    for objWheels in list_wheels:
        #non fare due volte la stessa ruota
        if(str("Wheel"+str(k)+"f") == str(objWheels.name)): continue
        for objSpoiler in list_spoilers:
            for objBumper in list_bumpers:       
                #fai il render / salva sul database(?)
                print(k)
                """
                fileSalvataggio.write(
                 objLiveryFake.name + ";" +
                 'Wheel' + str(k) + 'b' + ";" + 
                 'Wheel' + str(k) + 'f' + ";" + 
                 objSpoiler.name + ";" +
                 objBumper.name + ";" +
                 '\n'
                 )
                 """
                mycursor.execute("INSERT INTO carmodel1 (Livery, Wheel, Spoiler, Bumper) VALUES (\"" + str(objLiveryFake.name) + "\", \"Wheel" + str(nr_wheel) + "\", \"" + str(objSpoiler.name) + "\", \"" + objBumper.name + "\");")
                k=k+1
                nr_wheel=nr_wheel+1
                if(nr_wheel==21): nr_wheel=1
mydb.commit()
#fileSalvataggio.close()