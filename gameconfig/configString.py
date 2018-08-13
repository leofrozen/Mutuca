	
# -*- coding: UTF-8 -*-

config_string = {
 "mapdir":"gameStages/maps/",
 "spritedir":"multimedia/sprites/",
 "soundtrackdir":"multimedia/soundtrack/",
 "soundeffectdir":"multimedia/soundEffects/",
	"stages":[
			
			{
			"name":"Mapa00 - TUTORIAL",
			"id":"map00",
			"mapfile":"mapa01.json",
			"type":"city",
			"npcs":[],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"welcome_home.ogg",
			"portals":["map01-02"],
			"startpoint":[50,350],
			"scriptID":1,
			"message":"DESTROY ALL ENEMIES!"
			},
			{
			"name":"Mapa01",
			"id":"map01",
			"mapfile":"mapa01.json",
			"type":"city",
			"npcs":[["npc08",490,400],["npc03",300,450],["npc05",800,600]],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"welcome_home.ogg",
			"portals":["map01-02"],
			"startpoint":[50,350],
			"scriptID":1,
			"message":"DESTROY ALL ENEMIES!"
			},
			{
			"name":"Mapa02",
			"id":"map02",
			"mapfile":"mapa02.json",
			"type":"city",
			"npcs":[["npc03",490,500],["npc06",1000,500],["npc10",1600,560]],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"welcome_home.ogg",
			"portals":["map02-01","map02-07","map02-03","map02-08"],
			"startpoint":[50,350],
			"scriptID":2,
			"message":"DESTROY ALL ENEMIES!"
			},
			{
			"name":"Mapa03",
			"id":"map03",
			"mapfile":"mapa03.json",
			"type":"city",
			"npcs":[["npc03",490,400],["npc10",900,450],["npc04",1200,600]],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"welcome_home.ogg",
			"portals":["map03-02","map03-04", "map03-09"],
			"startpoint":[50,350],
			"scriptID":3,
			"message":"DESTROY ALL ENEMIES!"
			},
			{
			"name":"Mapa04",
			"id":"map04",
			"mapfile":"mapa04.json",
			"type":"city",
			"npcs":[["npc04",490,400],["npc07",500,450],["npc08",1100,800],["npc09",1300,600]],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"welcome_home.ogg",
			"portals":["map04-03","map04-10"],
			"startpoint":[50,350],
			"scriptID":4,
			"message":"DESTROY ALL ENEMIES!"
			},
			{
			"name":"Mapa05",
			"id":"map05",
			"mapfile":"mapa05.json",
			"type":"city",
			"npcs":[["npc11",500,350]],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"welcome_home.ogg",
			"portals":["map05-06", "map05-07"],
			"startpoint":[450,550],
			"scriptID":5,
			"message":"DESTROY ALL ENEMIES!"
			},
			{
			"name":"Mapa06",
			"id":"map06",
			"mapfile":"mapa06.json",
			"type":"city",
			"npcs":[],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"DST-5thStreet.ogg",
			"portals":["map06-07", "map06-05"],
			"startpoint":[430,325],
			"scriptID":6,
			"message":"DESTROY ALL ENEMIES!"
			},
			{
			"name":"Mapa07",
			"id":"map07",
			"mapfile":"mapa07.json",
			"type":"city",
			"npcs":[],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"DST-5thStreet.ogg",
			"portals":["map07-02","map07-06","map07-05"],
			"startpoint":[320,256],
			"scriptID":7,
			"message":"DESTROY ALL ENEMIES!"
			},
			{
			"name":"Mapa08",
			"id":"map08",
			"mapfile":"mapa08.json",
			"type":"city",
			"npcs":[],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"DST-5thStreet.ogg",
			"portals":["map08-02"],
			"startpoint":[416,68],
			"scriptID":8,
			"message":"DESTROY ALL ENEMIES!"
			},
			{
			"name":"Mapa09",
			"id":"map09",
			"mapfile":"mapa09.json",
			"type":"city",
			"npcs":[],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"DST-5thStreet.ogg",
			"portals":["map09-03"],
			"startpoint":[480,672],
			"scriptID":9,
			"message":"DESTROY ALL ENEMIES!"
			},
			{
			"name":"Mapa10_Final",
			"id":"map10",
			"mapfile":"mapa10.json",
			"type":"city",
			"npcs":[],
			"enemies":[],
			"properties":"teste",
			"soundtrack":"DST-5thStreet.ogg",
			"portals":["map10-04"],
			"startpoint":[480,672],
			"scriptID":10,
			"message":"DESTROY ALL ENEMIES!"
			}
			
			
			
	],
	"entities":{
			"player":[
				{
				"name":"player",
				"sprite":"ent01",
				"id":"ent01",
				"stage":"",
				"type":"player",
				"dimensionx":32,
				"dimensiony":32,
				"weight":1,
				"spot":"",
				"dialogs":{
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"100",
						"mana":"120",
						"ad":"5",
						"ap":"5",
						"armor":"5",
						"mdef":"3",
						"aspd":"0.5",
						"movspd":"150.",
						"vision":"300"
						},
				"bag":["item01", "chest01", "helmet01"]
				}
				],
			"npc":[
				{
				"name":"npc1_old_man",
				"sprite":"ent02",
				"id":"npc01",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[490,144],
				"dialogs":{
						"begin":["Êta mosquito GRANDE da molesta!!"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"60.",
						"vision":"150"
						}
				},
				{
				"name":"npc2_old_man02",
				"sprite":"ent03",
				"id":"npc02",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[675,1200],
				"dialogs":{
						"begin":["No meu tempo não tinha isso!", "E não tinha tanto lixo na cidade!"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"60.",
						"vision":"150"
						}
				},
				{
				"name":"npc3_village_man",
				"sprite":"ent04",
				"id":"npc03",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[675,1200],
				"dialogs":{
						"begin":["Ei Frozen!", "Vai por mim!", "É melhor combater o foco do mosquito!"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"100.",
						"vision":"150"
						}
				},
				{
				"name":"npc4_village_mant2",
				"sprite":"ent05",
				"id":"npc04",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[490,144],
				"dialogs":{
						"begin":["Corre muleque!", "Que o mosquito tá vindo!"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"100.",
						"vision":"150"
						}
				},
				{
				"name":"npc5_village_mant2_02",
				"sprite":"ent06",
				"id":"npc05",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[675,1200],
				"dialogs":{
						"begin":["Matar apenas o mosquito não adianta!"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"100.",
						"vision":"150"
						}
				},
				{
				"name":"npc6_old_woman",
				"sprite":"ent07",
				"id":"npc06",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[675,1200],
				"dialogs":{
						"begin":["Oooh vizinho", "Depois dá uma passadinha lá em casa", "Fica em frente a sua"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"60.",
						"vision":"150"
						}
				},
				{
				"name":"npc7_village_woman02",
				"sprite":"ent13",
				"id":"npc07",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[675,1200],
				"dialogs":{
						"begin":["Ei Frozen!", "Obrigado por ajudar a cidade!"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"100.",
						"vision":"150"
						}
				},
				{
				"name":"npc8_sakkat_man",
				"sprite":"ent10",
				"id":"npc08",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[675,1200],
				"dialogs":{
						"begin":["Ei Frozen!!", "Pressione esc para abrir seu inventário"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"100.",
						"vision":"150"
						}
				},
				{
				"name":"npc9_village_man_02",
				"sprite":"ent11",
				"id":"npc09",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[675,1200],
				"dialogs":{
						"begin":["Caixas d'água sem tampa","e pneus abandonados são perigosos!"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"100.",
						"vision":"150"
						}
				},
				{
				"name":"npc10_sakkat_man02",
				"sprite":"ent12",
				"id":"npc10",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[675,1200],
				"dialogs":{
						"begin":["Ei rapaz", "Não deixa o Zikka virus te pegar!"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"100.",
						"vision":"150"
						}
				},
				{
				"name":"npc11_village_woman",
				"sprite":"ent08",
				"id":"npc11",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[675,1200],
				"dialogs":{
						"begin":["Meu filho...", "Cuide da nossa casa!!"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"100.",
						"vision":"150"
						}
				},
				{
				"name":"npc12_old_woman02",
				"sprite":"ent14",
				"id":"npc12",
				"stage":"",
				"type":"npc",
				"dimensionx":32,
				"dimensiony":32,
				"weight":0.5,
				"spot":[675,1200],
				"dialogs":{
						"begin":["Oooh meu jovem...", "Afasta esses mosquitos daqui!"],
						"quest":["option1", "option2"],
						"end":["Valew, falow!"] 
						
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"70",
						"mana":"20",
						"ad":"5",
						"ap":"5",
						"armor":"4",
						"mdef":"1",
						"aspd":"1",
						"movspd":"60.",
						"vision":"150"
						}
				}
				
				
				],
			"enemy":[
				
				{
				"name":"enemy_mutuca01",
				"sprite":"ent09",
				"id":"enemymutuca01",
				"stage":"",
				"type":"enemy",
				"dimensionx":28,
				"dimensiony":28,
				"weight":0.5,
				"spot":[480,1700],
				"dialogs":{
						"begin":["Vou te comer!!", "Hahaha!!"]
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"50",
						"mana":"20",
						"ap":"5",
						"ad":"6",
						"armor":"5",
						"mdef":"3",
						"aspd":"1",
						"movspd":"80.",
						"vision":"150"
						}
				},
				{
				"name":"enemy_aedes01",
				"sprite":"ent15",
				"id":"enemyaedes02",
				"stage":"",
				"type":"boss",
				"dimensionx":28,
				"dimensiony":28,
				"weight":0.5,
				"spot":[480,1700],
				"dialogs":{
						"begin":["Segura esse meu vírus!!", "Hahaha"]
						},
				"properties":
							{
							"states":[]
							},
				"status":
						{
						"life":"550",
						"mana":"620",
						"ap":"15",
						"ad":"15",
						"armor":"8",
						"mdef":"5",
						"aspd":"1.5",
						"movspd":"80.",
						"vision":"200"
						}
				}
			
				]
			
	},
	"elements":{
			"lockpass":[
					{
					"description":"chptown01 -> chpfield01",
					"id":"lck01",
					"sprite":"effportal01",
					"position":[20, 320]
					},
					{
					"description":"chptown01 -> chpfield02",
					"id":"lck02",
					"sprite":"effportal01",
					"position":[940,320]
					}
			],
			"portal":[
					{
					"description":"mapa01 -> mapa02",
					"id":"map01-02",
					"sprite":"effportal02",
					"position":[1900, 575],
					"destination":[60, 350],
					"dst_stage":"map02"
					},
					{
					"description":"mapa02 -> mapa01",
					"id":"map02-01",
					"sprite":"effportal02",
					"position":[20, 560],
					"destination":[1850, 575],
					"dst_stage":"map01"
					},
					{
					"description":"mapa02 -> mapa07",
					"id":"map02-07",
					"sprite":"effportal02",
					"position":[896, 288],
					"destination":[480, 670],
					"dst_stage":"map07"
					},
					{
					"description":"mapa05 -> mapa06",
					"id":"map05-06",
					"sprite":"effportal02",
					"position":[400, 240],
					"destination":[415, 340],
					"dst_stage":"map06"
					},
					{
					"description":"mapa06 -> mapa05",
					"id":"map06-05",
					"sprite":"effportal02",
					"position":[415, 390],
					"destination":[400, 280],
					"dst_stage":"map05"
					},
					{
					"description":"mapa06 -> mapa07",
					"id":"map06-07",
					"sprite":"effportal02",
					"position":[315, 450],
					"destination":[320, 280],
					"dst_stage":"map07"
					},
					{
					"description":"mapa07 -> mapa06",
					"id":"map07-06",
					"sprite":"effportal02",
					"position":[320, 230],
					"destination":[315, 400],
					"dst_stage":"map06"
					},
					{
					"description":"mapa07 -> mapa02",
					"id":"map07-02",
					"sprite":"effportal02",
					"position":[480, 710],
					"destination":[896, 320],
					"dst_stage":"map02"
					},
					{
					"description":"mapa07 -> mapa05",
					"id":"map07-05",
					"sprite":"effportal02",
					"position":[480, 456],
					"destination":[464, 550],
					"dst_stage":"map05"
					},
					{
					"description":"mapa05 -> mapa07",
					"id":"map05-07",
					"sprite":"effportal02",
					"position":[464, 640],
					"destination":[480, 488],
					"dst_stage":"map07"
					},
					{
					"description":"mapa02 -> mapa03",
					"id":"map02-03",
					"sprite":"effportal02",
					"position":[1900, 560],
					"destination":[60, 560],
					"dst_stage":"map03"
					},
					{
					"description":"mapa03 -> mapa02",
					"id":"map03-02",
					"sprite":"effportal02",
					"position":[30, 528],
					"destination":[1850, 560],
					"dst_stage":"map02"
					},
					{
					"description":"mapa03 -> mapa04",
					"id":"map03-04",
					"sprite":"effportal02",
					"position":[1900, 528],
					"destination":[80, 560],
					"dst_stage":"map04"
					},
					{
					"description":"mapa04 -> mapa03",
					"id":"map04-03",
					"sprite":"effportal02",
					"position":[32, 616],
					"destination":[1850, 560],
					"dst_stage":"map03"
					},
					{
					"description":"mapa02 -> mapa08",
					"id":"map02-08",
					"sprite":"effportal02",
					"position":[870, 836],
					"destination":[415, 100],
					"dst_stage":"map08"
					},
					{
					"description":"mapa08 -> mapa02",
					"id":"map08-02",
					"sprite":"effportal02",
					"position":[415, 65],
					"destination":[870, 786],
					"dst_stage":"map02"
					},
					{
					"description":"mapa03 -> mapa09",
					"id":"map03-09",
					"sprite":"effportal02",
					"position":[1312, 272],
					"destination":[545, 680],
					"dst_stage":"map09"
					},
					{
					"description":"mapa09 -> mapa03",
					"id":"map09-03",
					"sprite":"effportal02",
					"position":[510, 780],
					"destination":[1312, 340],
					"dst_stage":"map03"
					},
					{
					"description":"mapa04 -> mapa10",
					"id":"map04-10",
					"sprite":"effportal02",
					"position":[1424, 712],
					"destination":[176, 1088],
					"dst_stage":"map10"
					},
					{
					"description":"mapa10 -> mapa04",
					"id":"map10-04",
					"sprite":"effportal02",
					"position":[100, 1090],
					"destination":[1392, 712],
					"dst_stage":"map04"
					}
					
					
					],
			"attack_effect":[
					{
					"id":"effect01",
					"sprite":"effect01"
					}
					]
	
	},
	"weapons":{
			"noweapon":[
						{
						"name":"Punch",
						"description":"Descricao do item",
						"id":"nwpch01",
						"ad":"0",
						"ap":"0",
						"armor":0,
						"mdef":0,
						"movspeed":0,
						"range":"35",
						"aspd":"0",
						"sprite":"effpch01",
						"sound":"battle/sword.ogg"
						},
						{
						"name":"Kick",
						"description":"Descricao do item",
						"id":"nwkck01",
						"ad":"0",
						"ap":0,
						"armor":0,
						"mdef":0,
						"movspeed":0,
						"range":"35",
						"aspd":"0",
						"range":"35",
						"sprite":"kck01.png",
						"sound":"battle/sword.ogg"
						}
			],
			"sword":[
					{
					"name":"Wood Sword",
					"description":"Descricao do item",
					"id":"swd01",
					"ad":"8",
					"ap":0,
					"armor":0,
					"mdef":0,
					"movspeed":0,
					"range":"35",
					"aspd":"0",
					"sprite":"atk02.png",
					"sound":"battle/sword.ogg"
					}
					]
			
	},
	
	"item":[
			{
			"name":"Poção de Cura",
			"id":"item01",
			"description":"Recupera uma boa quantia de vida perdida",
			"sprite":"icon02",
			"function":"heal",
			"parameter":"50"
			},
			{
			"name":"Bateria",
			"id":"item02",
			"description":"recupera uma boa quantia de energia perdida",
			"sprite":"icon03",
			"function":"energyup",
			"parameter":"60"
			}

	],
	
	"equip":{
			"helmet":[
					{
					"name":"Bone",
					"description":"Descricao do item",
					"id":"helmet01",
					"ad":"2",
					"ap":0,
					"armor":2,
					"mdef":0,
					"movspeed":0,
					"aspd":"0",
					"sprite":"effpch01.png",
					"sound":"sword.ogg"
					}
			],
			"chest":[
					{
					"name":"Capa de Chuva",
					"description":"Descricao do item",
					"id":"chest01",
					"ad":"0",
					"ap":0,
					"armor":0,
					"mdef":0,
					"movspeed":0,
					"aspd":"0",
					"sprite":"rsunsword.png",
					"sound":"sword.ogg"
					}
			],
			"bottom":[
					{
					"name":"calcas de Chuva",
					"description":"Descricao do item",
					"id":"bottom01",
					"ad":"0",
					"ap":0,
					"armor":1,
					"mdef":2,
					"movspeed":0,
					"aspd":"0",
					"sprite":"rsunsword.png",
					"sound":"sword.ogg"
					}
			],
			"boots":[
					{
					"name":"botas de Chuva",
					"description":"Descricao do item",
					"id":"boot01",
					"ad":"0",
					"ap":0,
					"armor":0,
					"mdef":0,
					"movspeed":50,
					"aspd":"0",
					"sprite":"rsunsword.png",
					"sound":"sword.ogg"
					}
			],
			"weapon":[
					{
					"name":"Raquete01",
					"description":"Descricao do item",
					"id":"weapon01",
					"ad":"20",
					"ap":"0",
					"armor":0,
					"mdef":0,
					"bullet_speed":150,
					"movspeed":0,
					"s_range":"30",
					"e_range":"5",
					"aspd":"100",
					"energycost":0,
					"sprite":"effpch01",
					"sound":"battle/drawKnife3.ogg"
					},
					{
					"name":"picada",
					"description":"picada de mosquito",
					"id":"weapon02",
					"ad":"5",
					"ap":"0",
					"armor":0,
					"mdef":0,
					"bullet_speed":150,
					"movspeed":0,
					"s_range":"40",
					"e_range":"1",
					"aspd":"0",
					"energycost":0,
					"sprite":"effpch01",
					"sound":"battle/random4.ogg"
					},
					{
					"name":"Raquete02",
					"description":"Ataque eletrico da raquete",
					"id":"weapon03",
					"ad":"0",
					"ap":"50",
					"armor":0,
					"mdef":0,
					"bullet_speed":150,
					"movspeed":0,
					"s_range":"35",
					"e_range":"35",
					"aspd":"0",
					"energycost":10,
					"sprite":"efflightball01",
					"sound":"battle/espark01.ogg"
					},
					{
					"name":"bomba de veneno",
					"description":"Lança um poderoso veneno",
					"id":"weapon04",
					"ad":"0",
					"ap":"0",
					"armor":0,
					"mdef":0,
					"bullet_speed":200,
					"movspeed":0,
					"s_range":"35",
					"e_range":"105",
					"aspd":"0",
					"energycost":25,
					"sprite":"effveneno01",
					"sound":"misc/spell.ogg"
					},
					{
					"name":"picada_02",
					"description":"picada de mosquito forte",
					"id":"weapon05",
					"ad":"5",
					"ap":"0",
					"armor":0,
					"mdef":0,
					"bullet_speed":150,
					"movspeed":0,
					"s_range":"35",
					"e_range":"1",
					"aspd":"0",
					"energycost":0,
					"sprite":"effattack02",
					"sound":"battle/drawKnife2.ogg"
					},
					{
					"name":"picada_03",
					"description":"projetio lancado pelo mosquito",
					"id":"weapon06",
					"ad":"5",
					"ap":"60",
					"armor":0,
					"mdef":0,
					"bullet_speed":100,
					"movspeed":0,
					"s_range":"35",
					"e_range":"200",
					"aspd":"0",
					"energycost":30,
					"sprite":"effattack02",
					"sound":"battle/drawKnife2.ogg"
					}
			]
	},
	"etc":[
			{
			"name":"pocao de vida"
			}
	],
	
	
	"sprites":{
			"entities":[
					{
					"name":"player",
					"id":"ent01",
					"file":"fuleco.png",
					"lin":8,
					"col":9,
					"atk_cols":6,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"old_man",
					"id":"ent02",
					"file":"old_man.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"old_man02",
					"id":"ent03",
					"file":"old_man02.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"village_man",
					"id":"ent04",
					"file":"village_man.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"village_mant2",
					"id":"ent05",
					"file":"village_man_t2.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"village_mant2_02",
					"id":"ent06",
					"file":"village_man_t2_02.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"old_Woman",
					"id":"ent07",
					"file":"old_woman.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"Village_woman02",
					"id":"ent08",
					"file":"village_woman02.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"Mutuca01",
					"id":"ent09",
					"file":"mutuca_01.png",
					"lin":8,
					"col":5,
					"atk_cols":5,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"sakkat_man",
					"id":"ent10",
					"file":"sakkat_man.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"village_man02",
					"id":"ent11",
					"file":"village_man02.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"sakkat_man02",
					"id":"ent12",
					"file":"sakkat_man02.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"village_woman",
					"id":"ent13",
					"file":"village_woman.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"old_Woman02",
					"id":"ent14",
					"file":"old_woman02.png",
					"lin":4,
					"col":9,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"Mutuca02",
					"id":"ent15",
					"file":"mutuca02.png",
					"lin":8,
					"col":5,
					"atk_cols":5,
					"sound":"aquivo de som.mp3"
					}
					
					
			],
			"effects":[
					{
					"name":"portal",
					"id":"effportal01",
					"file":"portal01.png",
					"lin":1,
					"col":5,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"portal1",
					"id":"effportal02",
					"file":"portal02.png",
					"lin":1,
					"col":10,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"test01",
					"id":"effpch01",
					"file":"pch01.png",
					"lin":1,
					"col":6,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"explosion01",
					"id":"effexplosion01",
					"file":"explosion01.png",
					"lin":1,
					"col":10,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"explosion02",
					"id":"effexplosion02",
					"file":"explosion02.png",
					"lin":1,
					"col":10,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"lapide01",
					"id":"efflapide01",
					"file":"lapide01.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"litghtball",
					"id":"efflightball01",
					"file":"lightball01.png",
					"lin":1,
					"col":10,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"interact",
					"id":"effinteract01",
					"file":"interact.png",
					"lin":1,
					"col":10,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"gas venenoso",
					"id":"effveneno01",
					"file":"gas_veneno01.png",
					"lin":1,
					"col":10,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"Attack Effect 02",
					"id":"effattack02",
					"file":"attack_effect02.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					}
					
			],
			"icons":[
					{
					"name":"dropedBag",
					"id":"icon01",
					"file":"dropedbag.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"misc/handleCoins.ogg"
					},
					{
					"name":"Red Pot",
					"id":"icon02",
					"file":"redpot.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"misc/handleCoins.ogg"
					},
					{
					"name":"Batery",
					"id":"icon03",
					"file":"pilha.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"misc/handleCoins.ogg"
					},
					{
					"name":"MainAtack",
					"id":"icon04",
					"file":"icon_racket.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"misc/handleCoins.ogg"
					},
					{
					"name":"SecondAttack",
					"id":"icon05",
					"file":"icon_racket_on.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"misc/handleCoins.ogg"
					},
					{
					"name":"Interact",
					"id":"icon06",
					"file":"icon_interact.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"misc/handleCoins.ogg"
					},
					{
					"name":"Item Especial",
					"id":"icon07",
					"file":"icon_special_item.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"misc/handleCoins.ogg"
					}
					
			],
			"others":[
					{
					"name":"item_slot",
					"id":"other01",
					"file":"item_slot.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"misc/handleCoins.ogg"
					},
					{
					"name":"bg_nuvens",
					"id":"other02",
					"file":"bg_nuvens.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"misc/handleCoins.ogg"
					},
					{
					"name":"bg_nuvens",
					"id":"other03",
					"file":"bg_nuvens.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"misc/handleCoins.ogg"
					},
					{
					"name":"balde01",
					"id":"otherbalde01",
					"file":"balde01.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"balde02",
					"id":"otherbalde02",
					"file":"balde02.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"pneu01",
					"id":"otherpneu01",
					"file":"pneu01.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"pneu02",
					"id":"otherpneu02",
					"file":"pneu02.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"caixadagua01",
					"id":"othercaixadagua01",
					"file":"caixadagua.png",
					"lin":1,
					"col":10,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"pets01",
					"id":"otherpets01",
					"file":"garrafaspet.png",
					"lin":1,
					"col":10,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"prato_vaso",
					"id":"otherprato01",
					"file":"prato01.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"vaso01",
					"id":"othervaso01",
					"file":"vaso01.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"vaso02",
					"id":"othervaso02",
					"file":"vaso02.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"barril01",
					"id":"otherbarril01",
					"file":"barril01.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"vaso02",
					"id":"othervaso02",
					"file":"vaso02.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"lixeira01",
					"id":"otherlixeira01",
					"file":"lixeira01.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"Item Especial",
					"id":"otherspecial01",
					"file":"dropedbag_special.png",
					"lin":1,
					"col":8,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					},
					{
					"name":"Item Especial",
					"id":"otherspecial02",
					"file":"dropedbag02.png",
					"lin":1,
					"col":1,
					"atk_cols":0,
					"sound":"aquivo de som.mp3"
					}
					
			]
			
	},
	"sounds":{
			"song01":"filename",
			"song02":"filename",
			"sword01":"filename",
			"sword02":"filename",
			"misc01":"misc/handleCoins.ogg",
			"misc02":"misc/spell.ogg"
	}
}
