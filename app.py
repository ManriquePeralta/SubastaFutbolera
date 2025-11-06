from flask import Flask, request, jsonify, render_template, send_from_directory
import random
from itertools import groupby

app = Flask(__name__, static_folder="static", template_folder="templates")

# ---------- Aquí está la lógica adaptada desde tu script (rangos, jugadores, formaciones) ----------
rangos = {
    "PO": (30, 90), "DFC": (30, 90), "DFD": (25, 90), "DFI": (25, 90),
    "MCD": (35, 90), "MC": (30, 90), "MCO": (30, 90), "ED": (30, 90),
    "EI": (30, 90), "DC": (30, 90)
}

# (Usé la lista resumida; reemplazala con la tuya completa si querés)
jugadores = [
    ("PO", "LUCAS CHEVALIER", "FRANCIA"), ("PO", "DIOGO COSTA", "PORTUGAL"),
    ("PO", "GIANLUIGI DONNARUMMA", "ITALIA"), ("PO", "DAVID RAYA", "ESPAÑA"),
    ("PO", "GREGOR KOBEL", "SUIZA"), ("PO", "JAN OBLAK", "ESLOVENIA"),
    ("PO", "ANDRE ONANA", "CAMERUN"), ("PO", "YANN SOMMER", "SUIZA"),
    ("PO", "MIKE MAIGNAN", "FRANCIA"), ("PO", "EMILIANO MARTINEZ", "ARGENTINA"),
    ("PO", "ALEX REMIRO", "ESPAÑA"), ("PO", "ALPHONSE AREOLA", "FRANCIA"),
    ("PO", "UNAI SIMON", "ESPAÑA"), ("PO", "GONZALO CICCARELI", "ARGENTINA"),
    ("PO", "LEV YASHIN PRIME", "RUSIA"), ("PO", "OLIVER KHAN", "ALEMANIA"),
    ("PO", "VICTOR VALDES PRIME", "ESPAÑA"), ("PO", "EDERSON MORAES", "BRASIL"),
    ("PO", "ALLISON BECKER", "BRASIL"), ("PO", "GUILLERMO OCHOA", "MEXICO"),
    ("PO", "SERGIO CHIQUITO ROMERO", "ARGENTINA"), ("PO", "FRANCO ARMANI", "ARGENTINA"),
    ("PO", "CLAUDIO BRAVO", "CHILE"), ("PO", "VICTOR VALDES ACTUAL", "ESPAÑA"),
    ("PO", "MANUEL NEUER", "ALEMANIA"), ("PO", "MARC ANDRE TER STEGEN", "ALEMANIA"),
    ("PO", "THIBAUT COURTOIS", "BELGICA"), ("PO", "DAVID DE GEA", "ESPAÑA"),
    ("PO", "KEYLOR NAVAS", "COSTA RICA"), ("PO", "YASSINE BOUNOU", "MARRUECOS"),
    ("PO", "WOJCIECH SZCZESNY", "POLONIA"), ("PO", "IKER CASILLAS PRIME", "ESPAÑA"),
    ("PO", "GIANLUIGI BUFFON", "ITALIA"), ("PO", "PETR CECH", "REPUBLICA CHECA"),
    ("PO", "JULIO CESAR", "BRASIL"),

    ("DFC", "PAU CUBARSI", "ESPAÑA"), ("DFC", "WILLIAM SALIBA", "FRANCIA"),
    ("DFC", "DEAN HUIJSEN", "ESPAÑA"), ("DFC", "WILLIAM PACHO", "ECUADOR"),
    ("DFC", "CRISTIAN ROMERO", "ARGENTINA"), ("DFC", "PIERO HINCAPIE", "ECUADOR"),
    ("DFC", "MARQUINHOS", "BRASIL"), ("DFC", "RONALD ARAUJO", "URUGUAY"),
    ("DFC", "EDER MILITAO", "BRASIL"), ("DFC", "DAVID HANCKO", "ESLOVENIA"),
    ("DFC", "NATHAN AKE", "HOLANDA"), ("DFC", "ANTONIO RUDIGER", "ALEMANIA"),
    ("DFC", "JOHN STONES", "INGLATERRA"),("DFC", "VIRGIL VAN DIJK", "HOLANDA"),
    ("DFC", "MARCOS ROJO", "ARGENTINA"), ("DFC", "MATTHIJS DE LIGTH", "HOLANDA"),
    ("DFC", "PEPE EXPULSADO", "PORTUGAL"),("DFC", "CHIQUI MAFIA", "ARGENTINA"), 
    ("DFC", "PIQUE PRESI DE LA KINGS LEAGUE", "ESPAÑA"), ("DFC", "HARRY MAGUIRE", "INGLATERRA"),
    ("DFC", "FUNES MORI", "ARGENTINA"), ("DFC", "ALAN BARASSI", "ARGENTINA"), 
    ("DFC", "AYMERIC LAPORTE", "ESPAÑA"), ("DFC", "SERGIO RAMOS MEXICANO", "ESPAÑA"),
    ("DFC", "SERGIO RAMOS PRIME", "ESPAÑA"), ("DFC", "CARLOS PUYOL", "ESPAÑA"), 
    ("DFC", "GERARD PIQUE PRIME", "ESPAÑA"), ("DFC", "PAOLO MANDINI", "ITALIA"),
    ("DFC", "FABIO CANNAVARO", "ITALIA"), ("DFC", "THIAGO SILVA PSG", "BRASIL"),
    ("DFC", "DIEGO GODIN", "URUGUAY"), ("DFC", "NICOLAS OTAMENDI", "ARGENTINA"),
    ("DFC", "YERRY MINA", "COLOMBIA"), ("DFC", "SAMUEL UMTITI", "FRANCIA"),
    ("DFC", "SERGIO RAMOS EXPULSADO", "ESPAÑA"), ("DFC", "JEROME BOATENG", "ALEMANIA"),
    
    
    ("DFD", "ACHRAF HAKIMI", "MARRUECOS"), ("DFD", "TRENT ALEXANDER ARNOLD", "INGLATERRA"),
    ("DFD", "PEDRO PORRO", "ESPAÑA"),("DFD", "BEN WHITE", "INGLATERRA"),
    ("DFD", "DIOGO DALOT", "PORTUGAL"), ("DFD", "AARON WAN BISSAKA", "INGLATERRA"),
    ("DFD", "MARCOS LLORENTE", "ESPAÑA"), ("DFD", "SERGIÑO DEST", "ESTADOS UNIDOS"),
    ("DFD", "NAHUEL MOLINA", " ARGENTINA"), ("DFD", "JOAO CANCELO", "PORTUGAL"),
    ("DFD", "FACUNDO LACIVITA", "ARGENTINA"),("DFD", "JULES KOUNDE", "FRANCIA"), 
    ("DFD", "BENJAMIN PAVARD", "FRANCIA"), ("DFD", "DANI CARVAJAL", "ESPAÑA"),
    ("DFD", "MALO GUSTO", "FRANCIA"), ("DFD", "MILTON CASCO", "ARGENTINA"),
    ("DFD", "JUAN FOYTH", "ARGENTINA"), ("DFD", "JEREMIE FRIMPONG", "HOLANDA"),
    ("DFD", "DENZEL DUMFRIES", "HOLANDA"), ("DFD", "CAFU PRIME", "BRASIL"),
    ("DFD", "DANI ALVES PRESO", "BRASIL"), ("DFD", "JAVIER ZANETTI", "ARGENTINA"),
    ("DFD", "DANI ALVES PRIME", "BRASIL"), ("DFD", "PABLO ZABALETA", "ARGENTINA"),
    ("DFD", "PHILIPP LAHM", "ALEMANIA"), ("DFD", "NELSON SEMEDO", "PORTUGAL"),
    ("DFD", "DANILO", "BRASIL"),
    
    ("DFI", "NUNO MENDES", "PORTUGAL"), ("DFI", "MILOS KERKEZ", "HUNGRIA"),("DFI", "MARC CUCURELLA", "ESPAÑA"),
    ("DFI", "ALEJANDRO BALDE", "ESPAÑA"), ("DFI", "THEO HERNANDEZ", "FRANCIA"),
    ("DFI", "ALEJANDRO GRIMALDO", "ESPAÑA"),
    ("DFI", "OLEKSANDR ZINCHENKO", "UKRANIA"),("DFI", "ANGELIÑO", "ESPAÑA"),
    ("DFI", "LUCAS HERNANDES", "FRANCIA"), ("DFI", "ROBERTO CARLOS", "BRASIL"),
    ("DFI", "NICOLAS TAGLIAFICO", "ARGENTINO"),("DFI", "MARCOS ACUÑA", "ACUÑA"),
    
    ("MCD", "RODRI", "ESPAÑA"),("MCD", "CASEMIRO", "BRASIL"),("MCD", "DECLAN RICE", "INGLAGERRA"),
    ("MCD", "NGOLO KANTE PRIME", "FRANCIA"), ("MCD", "NGOLO KANTE ARABE", "FRANCIA"),
    ("MCD", "AURELIEN TCHOUAMENI", "FRANCIA"), ("MCD", "BRUNO GUIMARAES", "BRASIL"),
    ("MCD", "SERGIO BUSQUETS", "ESPAÑA"), ("MCD", "PATRICK VIEIRA", "FRANCIA"),
    ("MCD", "XABI ALONSO DT", "ESPAÑA"), ("MCD", "XABI ALONSO PRIME", "ESPAÑA"),
    ("MCD", "LOTHAR MATTHAUS", "ALEMANIA"), ("MCD", "JAVIER MASCHERANO PRIME", "ARGENTINA"),
    ("MCD", "JAVIER MASCHERANO DT MIAMI", "ARGENTINA"), ("MCD", "ENZO FERNANDEZ", "ARGENTINA"),

    ("MC", "PEDRI", "ESPAÑA"), ("MC", "FEDERICO VALVERDE", "URUGUAY"),
    ("MC", "ALEXIS MAC ALLISTER", "ARGENTINA"), ("MC", "FRANK LAMPARD", "INGLATERRA"),
    ("MC", "EDUARDO CAMAVINGA", "FRANCIA"), ("MC", "GAVI", "ESPAÑA"),
    ("MC", "RODRIGO BENTANCUR", "URUGUAY"), ("MC", "ANDRES INIESTA PRIME", "ESPAÑA"),
    ("MC", "WARREN ZAIRE-EMERY", "FRANCIA"), ("MC", "FRANKIE DE JONG", "HOLANDA"),
    ("MC", "PAUL POGBA DOPING POSITIVO", "FRANCIA"), ("MC", "ANDREA PIRLO", "ITALIA"),
    ("MC", "RODRIGO DE PAUL", "ARGENTINA"),("MC", "JUAN ROMAN RIQUELME PRESI", "ARGENTINA"),
    ("MC", "SANDRO TONALI SUSPENDIDO POR TIMBA", "ITALIA"), ("MC", "SOCRATES", "BRASIL"),
    ("MC", "NESTOR ORTIGOZA", "PARAGUAY"), ("MC", "FELIPE CHAME", "ARGENTINO"),
    ("MC", "TIJJIANI REJINDERS", "HOLANDA"), ("MC", "TONI KROOS", "ALEMANIA"),
    ("MC", "FABIAN RUIZ", "ESPAÑA"), ("MC", "LUKA MODRIC", "CROACIA"), ("MC", "ARTURO VIDAL", "CHILE"),
    ("MC", "XAVI HERNANDEZ DT", "ESPAÑA"), ("MC", "XAVI HERNANDEZ PRIME", "ESPAÑA"),
    ("MC", "JOBE BELLINGHAM", "INGLATERRA"), ("MC", "ANDRES INIESTA CHINO", "ESPAÑA"),
    ("MC", "BASTIAN SCHWEINSTEIGER", "ALEMANIA"), ("MC", "DAVID SILVA", "ESPAÑA"),
    ("MC", "PAUL SCHOLES", "INGLATERRA"),


    ("MCO", "JUDE BELLINGHAM", "INGLATERRA"), ("MCO", "FLORIAN WIRTZ", "ALEMANIA"),
    ("MCO", "JAMAL MUSIALA SIN TOBILLO", "ALEMANIA"), ("MCO", "KAI HAVERTZ", "ALEMANIA"),
    ("MCO", "MARTIN ODEGAARD", "NORUEGA"),("MCO", "XAVI SIMMONS", "HOLANDA"),
    ("MCO", "ARDA GULLER", "TURQUIA"), ("MCO", "NICO PAZ", "ARGENTINO"), 
    ("MCO", "BRUNO FERNANDEZ", "PORTUGAL"), ("MCO", "PAULO DYBALA", "ARGENTINA"),
    ("MCO", "COLE PALMER", "INGLATERRA"),("MCO", "LUCAS PAQUETA", "BRASIL"), 
    ("MCO", "NICOLAS MICHININI", "ARGENTINA"),("MCO", "MARCO REUS", "ALEMANIA"),
    ("MCO", "DOMINIK SZOBOSZLAI", "HUNGRIA"), ("MCO", "DANI OLMO", "ESPAÑA"),
    ("MCO", "JULIAN BRANDT", "ALEMANIA"), ("MCO", "RONALDINHO", "BRASIL"),
    ("MCO", "MASON MOUNT", "INGLATERRA"), ("MCO", "MESUT OZIL", "ALEMANIA"),
    ("MCO", "DIEGO MARADONA", "ARGENTINA"), ("MCO", "ALESSANDRO DEL PIERO", "ITALIA"),
    ("MCO", "RICARDO KAKA", "BRASIL"), ("MCO", "ZINEDINE ZIDANE", "FRANCIA"),
    ("MCO", "JOAO FELIX", "PORTUGAL"),

    ("ED", "LIONEL MESSI", "ARGENTINA"), ("ED", "OUSMANE DEMBELE", "FRANCIA"),
    ("ED", "GARETH BALE", "GALES"), ("ED", "FEDERICO CHIESA", "ITALIA"),
    ("ED", "ANSU FATI", "ESPAÑA"), ("ED", "MICHAEL OLISE", "FRANCIA"), 
    ("ED", "BRYAN MBEUMO", "CAMERUN"), ("ED", "LEROY SANE", "ALEMANIA"),
    ("ED", "KARIM ADEYEMI", "ALEMANIA"), ("ED", "CHRISTIAN PULISIC", "ESTADOS UNIDOS"), 
    ("ED", "FRANCO MASTANTUONO", "ARGENTINA"), ("ED", "JADON SANCHO", "INGLATERRA"),
    ("ED", "LAMINE YAMAL", "ESPAÑA"), ("ED", "PHIL FODEN", "INGLATERRA"),
    ("ED", "MOHAMED SALAH", "EGIPTO"), ("ED", "TAKEFUSA KUBO", "JAPON"),
    ("ED", "MATIAS SOULE", "ARGENTINA"),("ED", "ANTHONY", "BRASIL"), 
    ("ED", "LUCAS MANRIQUE", "ARGENTINA"), 
    ("ED", "ARJEN ROBBEN", "HOLANDA"),
    ("ED", "LUIS FIGO", "PORTUGAL"), ("ED", "DAVID BECKHAM PRESI INTER DE MIAMI", "INGLATERRA"),
    ("ED", "DAVID BECKHAM PRIME", "INGLATERRA"), ("ED", "FRANCK RIBERY", "FRANCIA"),
    ("ED", "SHAQUIRI", "SUIZA"), ("ED", "NANI", "PORTUGAL"),

    ("EI", "VINICIUS JR", "BRASIL"), ("EI", "RAPHINHA", "BRASIL"),
    ("EI", "NICO WILLIAMS", "ESPAÑA"), ("EI", "RAFAEL LEAO", "PORTUGAL"),
    ("EI", "LUIS DIAZ", "COLOMBIA"), ("EI", "ALEJANDRO GARNACHO", "ARGENTINA"),
    ("EI", "THIAGO ALMADA", "ARGENTINA"), ("EI", "BRADLEY BARCOLA", "FRANCIA"), 
    ("EI", "CODY GAKPO", "HOLANDA"), ("EI", "RODRYGO", "BRASIL"),
    ("EI", "NICO GONZALEZ", "ARGENTINA"), ("EI", "GABRIEL MARTINELLI", "BRASIL"), 
    ("EI", "MARCUS RASHFORD", "INGLATERRA"), ("EI", "CRISTIANO RONALDO ARABE", "PORTUGAL"),
    ("EI", "SERGE GNABRY", "ALEMANIA"), ("EI", "CRISTIANO RONALDO PRIME", "PORTUGAL"),
    ("EI", "JACK GREALISH", "INGLATERRA"), ("EI", "EDEN HAZARD MADRID", "BELGICA"),
    ("EI", "KINGLEY COMAN", "FRANCIA"), ("EI", "EDEN HAZARD CHELSEA", "BELGICA"),
    ("EI", "ANGEL DI MARIA PRIME", "ARGENTINA"), ("EI", "ANGEL DI MARIA ROSARIO", "ARGENTINA"),

    ("DC", "ERLING HAALAND", "NORUEGA"), ("DC", "JULIAN ALVAREZ", "ARGENTINA"),
    ("DC", "LAUTARO MARTINEZ", "ARGENTINA"), ("DC", "HARRY KANE", "INGLATERRA"),
    ("DC", "DARWIN NUÑEZ", "URUGUAY"), ("DC", "ENDRICK", "BRASIL"),
    ("DC", "OMAR MARMOUSH", "EGIPTO"), ("DC", "CARLOS TEVEZ", "ARGENTINA"),
    ("DC", "BENJAMIN SESKO", "ESLOVENIA"), ("DC", "OLIVER GIROUD", "FRANCIA"),
    ("DC", "VIKTOR GYOKERES", "SUECIA"), ("DC", "VICTOR OSIMEH", "NIGERIA"), 
    ("DC", "MOISE KEAN", "FRANCIA"), ("DC", "ALVARO MORATA", "ESPAÑA"),
    ("DC", "TOMAS GONZALEZ", "ARGENTINA"), ("DC", "ROMELU LUKAKU", "BELGICA"),
    ("DC", "RONALDO NAZARIO", "BRASIL"), ("DC", "DIDIER DROGBA", "COSTA DE MARFIL"),
    ("DC", "ZLATAN IBRAHIMOVICH ESTADOS UNIDOS", "SUECIA"), ("DC", "KARIM BENZEMA ARABE", "FRANCIA"),
    ("DC", "ZLATAN IBRAIMOVICH PRIME", "SUECIA"), ("DC", "SAMUEL ETO´O", "CAMERUN"),
    ("DC", "KARIM BENZEMA PRIME", "FRANCIA"), ("DC", "ROBERT LEWANDOWSKI", "POLONIA"),
    ("DC", "WAYNE ROONEY", "INGLATERRA"), ("DC", "MIROSLAV KLOSE", "ALEMANIA"),
    ("DC", "SERGIO KUN AGUERO HOSPITALIZADO", "ARGENTINA"), ("DC", "SERGIO KUN AGUERO PRIME", "ARGENTINA"),
    ("DC", "ROBIN VAN PERSIE", "HOLANDA"),
]

formaciones = {
   "4-3-3 defensivo": {"PO": 1, "DFD": 1, "DFC": 2, "DFI": 1, "MCD": 1, "MC": 2, "MCO": 0, "ED": 1, "EI": 1, "DC": 1},

    "4-3-3 ofensivo": {"PO": 1, "DFD": 1, "DFC": 2, "DFI": 1, "MCD": 0, "MC": 2, "MCO": 1, "ED": 1, "EI": 1, "DC": 1},

    "4-4-2 clásico": {"PO": 1, "DFD": 1, "DFC": 2, "DFI": 1, "MCD": 0, "MC": 2, "MCO": 0, "ED": 1, "EI": 1, "DC": 2},

    "4-2-3-1 moderno": {"PO": 1, "DFD": 1, "DFC": 2, "DFI": 1, "MCD": 2, "MC": 0, "MCO": 1, "ED": 1, "EI": 1, "DC": 1},

    "4-1-4-1 equilibrado": {"PO": 1, "DFD": 1, "DFC": 2, "DFI": 1, "MCD": 1, "MC": 2, "MCO": 0, "ED": 1, "EI": 1, "DC": 1},

    "4-5-1 cerrado": {"PO": 1, "DFD": 1, "DFC": 2, "DFI": 1, "MCD": 1, "MC": 2, "MCO": 0, "ED": 1, "EI": 1, "DC": 1},

    "4-2-2-2": {"PO": 1, "DFD": 1, "DFC": 2, "DFI": 1, "MCD": 0, "MC": 2, "MCO": 0, "ED": 1, "EI": 1, "DC": 2},

    "4-1-2-1-2 rombo": {"PO": 1, "DFD": 1, "DFC": 2, "DFI": 1, "MCD": 1, "MC": 2, "MCO": 1, "ED": 0, "EI": 0, "DC": 2},

    "5-3-2 clásico": {"PO": 1, "DFD": 1, "DFC": 3, "DFI": 1, "MCD": 0, "MC": 3, "MCO": 0, "ED": 0, "EI": 0, "DC": 2},

    "3-5-2 ofensivo": {"PO": 1, "DFD": 0, "DFC": 3, "DFI": 0, "MCD": 0, "MC": 2, "MCO": 1, "ED": 1, "EI": 1, "DC": 2}
}

# ---------- Estado de la subasta en memoria ----------
AUCTION = {
    "started": False,
    "participants": {},      # nombre -> {"presupuesto": int, "plantel": []}
    "fm": None,              # formación elegida (mapa posiciones)
    "pool": [],              # lista de dicts {Posicion, Jugador, Nacionalidad, Precio}
    "pool_copy": [],         # copia mutable
    "jugadores_a_subastar": [],  # lista de candidatos con metadata
    "order_positions": ["PO","DFD","DFC","DFI","MCD","MC","MCO","ED","EI","DC"],
    "current_index": 0,
    "paso_flags": {},        # (pos,slot_index) -> bool (si ya se usó paso)
    "slot_buyers": {},       # (pos,slot_index) -> set(participant_names) para evitar comprar 2 veces en la misma plaza
    "extras_por_slot": 1
}

# ---------- Auxiliares ----------
vacante_contadores = {}
def crear_vacante(pos):
    vacante_contadores.setdefault(pos, 0)
    vacante_contadores[pos] += 1
    nombre = f"VACANTE_{pos}_{vacante_contadores[pos]}"
    return (pos, nombre, "VACANTE")

def build_pool():
    pool = []
    for pos, nombre, nac in jugadores:
        min_p, max_p = rangos.get(pos,(30,80))
        pool.append({"Posicion":pos,"Jugador":nombre,"Nacionalidad":nac,"Precio":random.randint(min_p,max_p)})
    return pool

def plaza_description(pos, slot_index, fm):
    desc = {
        "DFC": ["primer central","segundo central","tercer central"],
        "MC": ["primer mediocampista","segundo mediocampista","tercer mediocampista"],
        "DC": ["primer delantero","segundo delantero"],
        "PO":["portero"], "DFD":["lateral derecho"], "DFI":["lateral izquierdo"],
        "MCD":["mediocentro defensivo"], "MCO":["mediapunta"], "ED":["extremo derecho"], "EI":["extremo izquierdo"]
    }
    return desc.get(pos,[f"jugador {slot_index}"])[min(slot_index-1,2)]

# ---------- Endpoint: página principal ----------
@app.route("/")
def index():
    return render_template("index.html")

# ---------- Endpoint: iniciar subasta ----------
# recibe JSON: { "participants": ["A","B"], "formation": "4-3-3 ofensivo" }
@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    parts = data.get("participants", [])
    formation = data.get("formation")
    if not parts or not formation or formation not in formaciones:
        return jsonify({"ok":False, "error":"participants list and valid formation required"}), 400

    # reset auction
    AUCTION["participants"] = {p:{"presupuesto":1000,"plantel":[]} for p in parts}
    AUCTION["fm"] = formaciones[formation]
    AUCTION["pool"] = build_pool()
    AUCTION["pool_copy"] = AUCTION["pool"].copy()
    AUCTION["jugadores_a_subastar"] = []
    AUCTION["current_index"] = 0
    AUCTION["paso_flags"] = {}
    AUCTION["slot_buyers"] = {}
    AUCTION["total_slots"] = 0
    AUCTION["started"] = True

    # construir candidatos por plaza (igual que tu lógica)
    orden_dinamico = [pos for pos in AUCTION["order_positions"] if pos in AUCTION["fm"] and AUCTION["fm"][pos] > 0]
    global_slot = 1
    for pos in orden_dinamico:
        plazas = AUCTION["fm"][pos]
        for slot_index in range(1, plazas+1):
            disponibles = [j for j in AUCTION["pool_copy"] if j["Posicion"] == pos]
            random.shuffle(disponibles)
            objetivo = len(parts) + AUCTION["extras_por_slot"]
            while len(disponibles) < objetivo:
                vac = crear_vacante(pos)
                min_p, max_p = rangos.get(pos,(30,80))
                vac_dict = {"Posicion":vac[0],"Jugador":vac[1],"Nacionalidad":vac[2],"Precio":random.randint(min_p,max_p)}
                disponibles.append(vac_dict)
                AUCTION["pool_copy"].append(vac_dict)
            seleccion = disponibles[:objetivo]
            for cand in seleccion:
                cand_copy = cand.copy()
                cand_copy["_pos_slot"] = pos
                cand_copy["_slot_index"] = slot_index
                cand_copy["_global_slot"] = global_slot
                AUCTION["jugadores_a_subastar"].append(cand_copy)

            # init paso flag and buyers
            AUCTION["paso_flags"][(pos,slot_index)] = False
            AUCTION["slot_buyers"][(pos,slot_index)] = set()
            global_slot += 1

    AUCTION["total_slots"] = global_slot - 1

    return jsonify({"ok":True, "total_items": len(AUCTION["jugadores_a_subastar"])})

# ---------- Endpoint: obtener candidato actual ----------
@app.route("/candidate", methods=["GET"])
def candidate():
    if not AUCTION["started"]:
        return jsonify({"ok":False,"error":"Subasta no iniciada"}), 400
    if AUCTION["current_index"] >= len(AUCTION["jugadores_a_subastar"]):
        return jsonify({"ok":False,"finished":True})
    cand = AUCTION["jugadores_a_subastar"][AUCTION["current_index"]]
    pos = cand["_pos_slot"]; slot_index = cand["_slot_index"]
    # no mostramos el nombre real: "JUGADOR MISTERIOSO"
    response = {
        "ok": True,
        "Jugador": "JUGADOR MISTERIOSO",
        "Nacionalidad": cand["Nacionalidad"],
        "Posicion": pos,
        "Precio": cand["Precio"],
        "plaza_desc": plaza_description(pos, slot_index, AUCTION["fm"]),
        "slot_index": slot_index,
        "index": AUCTION["current_index"],
        "remaining": len(AUCTION["jugadores_a_subastar"]) - AUCTION["current_index"],
        "global_slot": cand.get("_global_slot")
    }
    return jsonify(response)

# ---------- Endpoint: acción (pagar/paso) ----------
# POST JSON: {"action":"paso"}  OR {"action":"pagar","participant":"Nombre","monto":123}
@app.route("/action", methods=["POST"])
def action():
    if not AUCTION["started"]:
        return jsonify({"ok":False,"error":"Subasta no iniciada"}), 400
    data = request.get_json()
    act = data.get("action")
    if act not in ("paso","pagar"):
        return jsonify({"ok":False,"error":"action must be 'paso' or 'pagar'"}), 400

    if AUCTION["current_index"] >= len(AUCTION["jugadores_a_subastar"]):
        return jsonify({"ok":False,"error":"No candidates left","finished":True})

    cand = AUCTION["jugadores_a_subastar"][AUCTION["current_index"]]
    pos = cand["_pos_slot"]; slot_index = cand["_slot_index"]

    if act == "paso":
        if AUCTION["paso_flags"].get((pos,slot_index),False):
            return jsonify({"ok":False,"error":"El 'paso' ya fue usado para esta plaza."}), 400
        # usar paso: avanzamos al siguiente candidato, y marcamos flag
        AUCTION["paso_flags"][(pos,slot_index)] = True
        AUCTION["current_index"] += 1
        # reveal the real player that was passed
        return jsonify({"ok":True,"msg":"Se usó paso.", "Jugador": cand.get("Jugador"), "global_slot": cand.get("_global_slot")})

    # pagar
    participante = data.get("participant")
    monto = data.get("monto")
    if participante not in AUCTION["participants"]:
        return jsonify({"ok":False,"error":"Participante inválido"}), 400
    try:
        monto = int(monto)
    except:
        return jsonify({"ok":False,"error":"Monto inválido"}), 400

    # check if participant already bought in this slot
    if participante in AUCTION["slot_buyers"][(pos,slot_index)]:
        return jsonify({"ok":False,"error":f"{participante} ya compró en esta plaza."}), 400
    if monto > AUCTION["participants"][participante]["presupuesto"]:
        return jsonify({"ok":False,"error":"Fondos insuficientes"}), 400

    # registrar compra
    AUCTION["participants"][participante]["presupuesto"] -= monto
    # guardar la compra con el nombre real del jugador
    bought = cand.copy()
    AUCTION["participants"][participante]["plantel"].append(bought)
    # marcar buyer para esta plaza (para evitar múltiples compras por mismo participante)
    AUCTION["slot_buyers"][(pos,slot_index)].add(participante)

    # eliminar del pool_copy (para que no aparezca de nuevo)
    for i,x in enumerate(AUCTION["pool_copy"]):
        if x["Posicion"] == cand["Posicion"] and x["Jugador"] == cand["Jugador"] and x["Nacionalidad"] == cand["Nacionalidad"]:
            AUCTION["pool_copy"].pop(i)
            break

    AUCTION["current_index"] += 1
    return jsonify({"ok":True, "msg":f"{participante} compró {cand['Jugador']} por {monto}."})

# ---------- Endpoint: estado (balances y planteles) ----------
@app.route("/status", methods=["GET"])
def status():
    if not AUCTION["started"]:
        return jsonify({"ok":False,"error":"Subasta no iniciada"}), 400
    participants = {p:{"presupuesto":d["presupuesto"], "plantel":[{"Jugador":j["Jugador"], "Posicion":j["Posicion"]} for j in d["plantel"]]} for p,d in AUCTION["participants"].items()}
    return jsonify({"ok":True, "participants":participants, "remaining": len(AUCTION["jugadores_a_subastar"]) - AUCTION["current_index"]})

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True, port=5000)

