import bpy
import os
import mysql.connector
import requests
import json
import sys
from datetime import datetime

carModeltable = "randomcarmodel1"
carBodyNumber =  "CarBody11"
LIMIT = "100"




obj = bpy.data.collections["Carrozzeria"].objects["Carrozzeria"]

# Clear all nodes in a mat
def clear_material( material ):
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()


materialToDelete = bpy.data.materials.get("Current")


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

mydb.database = "carscryptonovusracing"
mycursor = mydb.cursor()

dest = "C:\\Users\\500\\Desktop\\Render"

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

#TOP SPEED FOR THE CAR MODEL
mycursor.execute("SELECT power FROM carbodytype WHERE partNameAndNumber=\"" + carBodyNumber + "\" ")
result_set = mycursor.fetchall()
for row in result_set:
    list_InterfaceTopSpeed["TopSpeed"+str(row[0])].hide_render = False
    print(str(row[0]))
    
mycursor.execute("SELECT Livery, Wheel, Spoiler, Bumper FROM " + carModeltable + " LIMIT "+str(LIMIT))
result_set = mycursor.fetchall()

#VARIABLES FOR DB
wheelName=""
wheelPower=""
skinName=""
spoilerName=""
spoilerPower=""
bumperName=""
bumperPower=""
carBodyName=""
carBodyPower=""

i=1

#fileRipresaRender = open("C:\\Users\\500\\Desktop\\fileRipresaRender.txt", "a")

for row in result_set:
    try:
        print (row[0], row[1], row[2], row[3])
        #abilita al render gli oggetti presi dalla riga del database corrente
        
        #WHEELS
        list_wheels[row[1]+"f"].hide_render = False
        list_wheels[row[1]+"b"].hide_render = False
        list_InterfaceAccelleration["Acceleration" + row[1].replace("Wheel","")].hide_render = False
        list_InterfaceWheel["Car"+row[1]].hide_render = False
        #SPOILERS
        list_spoilers[row[2]].hide_render = False
        list_InterfaceBreakPower["BreakPower"+row[2].replace("Alettone","")].hide_render = False
        list_InterfaceSpoiler["CarSpoiler"+row[2].replace("Alettone","")].hide_render = False
        #BUMPERS
        list_bumpers[row[3]].hide_render = False
        list_InterfaceHandling["Handling"+row[3].replace("Front","")].hide_render = False
        list_InterfaceBumper["CarBumper"+row[3].replace("Front","")].hide_render = False
        
        #APPLY AND SHOW LIVERY
        # We clear it as we'll define it completely
        clear_material( materialToDelete )
        obj.data.materials.clear()
        obj.data.materials.append(bpy.data.materials.get("Current"))
        mat = bpy.data.materials.get("Current")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")

        texImage = mat.node_tree.nodes.new("ShaderNodeTexImage")
        texImage.image = bpy.data.images.load("C:\\Users\\500\\Desktop\\Auto\\CarLivree\\"+row[0]+".png",check_existing=True)
        mat.node_tree.links.new(bsdf.inputs["Base Color"], texImage.outputs["Color"])

        output = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
        mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

        list_InterfaceLivery["Car"+row[0]].hide_render = False

        #inserisci il path del render finale
        bpy.data.scenes[0].render.filepath = os.path.join(dest, str(i)+".mp4")
        #fai il render
        bpy.ops.render.render(animation=True)

        #disabilita ciò che hai usato

        #WHEELS
        list_wheels[row[1]+"f"].hide_render = True
        list_wheels[row[1]+"b"].hide_render = True
        list_InterfaceAccelleration["Acceleration" + row[1].replace("Wheel","")].hide_render = True
        list_InterfaceWheel["Car"+row[1]].hide_render = True
        #SPOILERS
        list_spoilers[row[2]].hide_render = True
        list_InterfaceBreakPower["BreakPower"+row[2].replace("Alettone","")].hide_render = True
        list_InterfaceSpoiler["CarSpoiler"+row[2].replace("Alettone","")].hide_render = True
        #BUMPERS
        list_bumpers[row[3]].hide_render = True
        list_InterfaceHandling["Handling"+row[3].replace("Front","")].hide_render = True
        list_InterfaceBumper["CarBumper"+row[3].replace("Front","")].hide_render = True
        #LIVERY
        list_InterfaceLivery["Car" + row[0]].hide_render = True
        
        #################CARICAMENTO SU DB DOPO IPFS#############################
        #this _file should be the full built car img OR 3dModel
        fileOutputRender = open("C:\\Users\\500\\Desktop\\Render\\" + str(i) + ".mp4",'rb')
        _file = {
          'file': fileOutputRender
        }
        response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files = _file)
        p = response.json()
        #link all' ipfs della car
        _hash = p['Hash']
        print(_hash)
        #GET WHEELS DATA
        mycursor.execute("SELECT name,power FROM wheeltype WHERE partNameAndNumber=\"" + row[1] + "\"")
        result_set = mycursor.fetchall()
        for row2 in result_set:
          wheelName = row2[0]
          wheelPower = row2[1]
        #GET SPOILER DATA
        mycursor.execute("SELECT name,power FROM spoilertype WHERE partNameAndNumber=\"" + row[2] + "\"")
        result_set = mycursor.fetchall()
        for row2 in result_set:
          spoilerName = row2[0]
          spoilerPower = row2[1]
        #GET BUMPER DATA
        mycursor.execute("SELECT name,power FROM bumpertype WHERE partNameAndNumber=\"" + row[3] + "\"")
        result_set = mycursor.fetchall()
        for row2 in result_set:
          bumperName = row2[0]
          bumperPower = row2[1]
        #GET SKIN DATA
        mycursor.execute("SELECT name FROM skintype WHERE partNameAndNumber=\"" + row[0] + "\"")
        result_set = mycursor.fetchall()
        for row2 in result_set:
          skinName = row2[0]
        #GET CARBODY DATA
        mycursor.execute("SELECT name,power FROM carbodytype WHERE partNameAndNumber=\"" + str(carBodyNumber) + "\"")
        result_set = mycursor.fetchall()
        for row2 in result_set:
          carBodyName = row2[0]
          carBodyPower = row2[1]
        #INSERT INTO TABLE OUR RENDERED CAR
        mycursor.execute("INSERT INTO `renderedcars` (`wheelName`, `wheelPower`, `spoilerName`, `spoilerPower`, `bumperName`, `bumperPower`, `carBodyName`, `carBodyPower`, `skinName`, `ipfsURI`) VALUES ('" + wheelName+ "', '" + str(wheelPower) + "', '" + spoilerName+ "', '" + str(spoilerPower) + "', '" + bumperName + "', '" + str(bumperPower) + "', '" +carBodyName + "', '"+ str(carBodyPower)+ "', '" + skinName+ "', '" + "https://ipfs.infura.io/ipfs/"+_hash + "')")
        mydb.commit()

        # datetime object containing current date and time
        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        fileRipresaRender.write("Render#"+str(i)+" ore: " + dt_string)

        print("Render e caricamento numero " + str(i) + " finito")
        fileOutputRender.close()
        os.remove("C:\\Users\\500\\Desktop\\Render\\"+str(i)+".mp4")

        i=i+1
    except:
        print("ECCEZIONE")