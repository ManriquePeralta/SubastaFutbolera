import random

# === Rangos de precios por posición ===
rangos = {
    "PO": (30, 90),
    "DFC": (30, 90),
    "DFD": (25, 90),
    "DFI": (25, 90),
    "MCD": (35, 90),
    "MC": (30, 90),
    "MCO": (30, 90),
    "ED": (30, 90),
    "EI": (30, 90),
    "DC": (30, 90)
}

# === Lista base de jugadores === (usa la tuya completa)
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

# === Formaciones (mapa de cuánto pide cada formación por posición) ===
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

2
# =============================
# Aux: crear vacantes si faltan
# =============================
vacante_contadores = {}

def crear_vacante(pos):
    vacante_contadores.setdefault(pos, 0)
    vacante_contadores[pos] += 1
    nombre = f"VACANTE_{pos}_{vacante_contadores[pos]}"
    return (pos, nombre, "VACANTE")

# =============================
# Generar precios aleatorios por posición (pool principal)
# =============================
# Convertimos la lista de jugadores a dicts con precio
pool = []
for pos, nombre, nac in jugadores:
    min_p, max_p = rangos.get(pos, (30, 80))
    pool.append({
        "Posicion": pos,
        "Jugador": nombre,
        "Nacionalidad": nac,
        "Precio": random.randint(min_p, max_p)
    })


# ================================
# Ingreso de participantes
# ================================
while True:
    try:
        cant = int(input("Ingrese la cantidad de participantes (max 10): "))
        if 1 <= cant <= 10:
            break
    except:
        pass
    print("Ingrese un número válido entre 1 y 10.")

participantes = {}

# --- Registro de participantes ---
for i in range(cant):
    nombre = input(f"\nIngrese el nombre del participante #{i+1}: ")
    participantes[nombre] = {"presupuesto": 1000, "plantel": []}


# ================================
# Elección grupal de la formación
# ================================
opciones = random.sample(list(formaciones.keys()), 4)
print("\nFormaciones disponibles para esta subasta:")
for idx, f in enumerate(opciones, 1):
    print(f"{idx}. {f}")

while True:
    try:
        elec = int(input("Elijan una formación grupal (1-4): "))
        if 1 <= elec <= 4:
            formacion_elegida = opciones[elec - 1]
            break
    except:
        pass
    print("Opción inválida, elijan un número entre 1 y 4.")

print(f"\n✅ Formación grupal elegida: {formacion_elegida}")

# =============================
# Calcular cupos por posición según la formación elegida
# =============================
fm = formaciones[formacion_elegida]
cupos = {}

# Para cada posición en la formación
for pos, cantidad in fm.items():
    if cantidad > 0:
        # Por cada plaza, necesitamos (cant + 1) jugadores
        # Ejemplo: si hay 2 centrales y 3 participantes:
        # - Primera plaza de central: 4 jugadores (3+1)
        # - Segunda plaza de central: 4 jugadores (3+1)
        # Total para DFC: 8 jugadores en total
        cupos[pos] = (cant + 1) * cantidad

# Mostrar cupos calculados
print("\nCandidatos por posición:")
for pos in ["PO","DFD","DFC","DFI","MCD","MC","MCO","ED","EI","DC"]:
    if pos in fm and fm[pos] > 0:
        print(f"{pos}: {cupos.get(pos,0)} candidatos para {fm[pos]} plaza(s)")

# -------------------------
# 1) Construir subastas por plaza (slot)
# -------------------------
fm = formaciones[formacion_elegida]
pool_copy = pool.copy()
jugadores_a_subastar = []  # cada item será un dict y además incluiremos 'Slot' para identificar la plaza

# extras por slot: 1 vacante por slot (lo querías así)
extras_por_slot = 1

# Orden fijo de posiciones (para mantener la lógica futbolera de atrás hacia adelante)
orden_posiciones = ["PO",                     # Arquero
                   "DFD", "DFC", "DFI",       # Defensas
                   "MCD", "MC", "MCO",        # Mediocampistas
                   "ED", "EI", "DC"]          # Delanteros

# obtener el orden dinámico basado en la formación, respetando el orden futbolero
orden_dinamico = [pos for pos in orden_posiciones if pos in fm and fm[pos] > 0]

print("\nOrden de subasta (de arquero a delantero):")
print(" → ".join(orden_dinamico))

for pos in orden_dinamico:
    plazas = fm[pos]  # ej: 3 centrales por equipo -> 3 plazas separadas
    for slot_index in range(1, plazas + 1):
        # seleccionar hasta 'cant' candidatos distintos del pool para esta plaza
        disponibles = [j for j in pool_copy if j["Posicion"] == pos]
        random.shuffle(disponibles)

        # número de candidatos objetivo para esta plaza: cant (uno por participante) + extras_por_slot
        objetivo = cant + extras_por_slot

        # si faltan jugadores en pool, crear vacantes hasta completar objetivo
        while len(disponibles) < objetivo:
            vac = crear_vacante(pos)
            min_p, max_p = rangos.get(pos, (30, 80))
            vac_dict = {"Posicion": vac[0], "Jugador": vac[1], "Nacionalidad": vac[2], "Precio": random.randint(min_p, max_p)}
            disponibles.append(vac_dict)
            pool_copy.append(vac_dict)

        # Tomamos exactamente 'objetivo' candidatos para esta plaza
        seleccion = disponibles[:objetivo]

        # Marcamos cada candidato con metadata de la plaza para el bucle de subasta
        for cand in seleccion:
            cand_copy = cand.copy()
            cand_copy["_pos_slot"] = pos
            cand_copy["_slot_index"] = slot_index
            jugadores_a_subastar.append(cand_copy)

# Ahora jugadores_a_subastar está organizado por plaza y dentro de cada plaza contiene (cant + 1) candidatos.
# Puedes verificar conteos si querés:
print("\nTotal de items a subastar:", len(jugadores_a_subastar))
for pos in orden_dinamico:
    total_por_pos = sum(1 for j in jugadores_a_subastar if j["_pos_slot"] == pos)
    print(f"{pos}: {total_por_pos} (debería ser {fm[pos] * (cant + extras_por_slot)})")

# -------------------------
# 2) Bucle de subasta con 'paso' único por plaza
# -------------------------

print("\n=== Subasta iniciada ===\n")

# Recorremos jugadores_a_subastar agrupados por plaza
# Agrupamos por (posición, slot)
from itertools import groupby

# Ordenar primero para que groupby funcione correctamente, respetando el orden futbolero
def get_posicion_orden(pos):
    try:
        return orden_posiciones.index(pos)
    except ValueError:
        return len(orden_posiciones)  # por si acaso hay una posición no listada

jugadores_a_subastar.sort(key=lambda x: (
    get_posicion_orden(x["_pos_slot"]),  # primero por orden de posición
    x["_slot_index"]                     # luego por número de plaza
))

for (pos, slot_index), grupo in groupby(jugadores_a_subastar, key=lambda x: (x["_pos_slot"], x["_slot_index"])):
    candidatos = list(grupo)
    # Mostrar descripción específica según la posición y el número de plaza
    plaza_desc = {
        "DFC": ["primer central", "segundo central", "tercer central"],
        "MC": ["primer mediocampista", "segundo mediocampista", "tercer mediocampista"],
        "DC": ["primer delantero", "segundo delantero"],
        "PO": ["portero"],
        "DFD": ["lateral derecho"],
        "DFI": ["lateral izquierdo"],
        "MCD": ["mediocentro defensivo"],
        "MCO": ["mediapunta"],
        "ED": ["extremo derecho"],
        "EI": ["extremo izquierdo"]
    }.get(pos, [f"jugador {slot_index}"])[min(slot_index-1, 2)]

    print(f"\n🏟️ Subasta — {plaza_desc.upper()} (1 'paso' permitido en esta plaza)")
    print(f"Posición: {pos} - Plaza #{slot_index} de {fm[pos]}")
    print(f"Candidatos disponibles: {len(candidatos)} jugadores")

    paso_usado = False  # reinicia por plaza

    for jugador in candidatos:
        print(f"\n🧾 Jugador en subasta:")
        print(f" - JUGADOR SECRETO")
        print(f" - Nacionalidad: {jugador['Nacionalidad']}")
        print(f" - 💰 Precio base: {jugador['Precio']} millones")
        print(f" - Plaza: {plaza_desc}")

        while True:
            comando = input("Ingrese 'pagar <nombre> <monto>' o 'paso': ").strip()
            cmd_lower = comando.lower()

            if cmd_lower == "paso":
                if not paso_usado:
                    paso_usado = True
                    print(f"⏭️ Se usó el único 'paso' disponible para este {plaza_desc}.")
                    print(f"Los siguientes jugadores para esta posición DEBEN ser comprados.")
                    break
                else:
                    print(f"❌ Ya se usó el 'paso' para el {plaza_desc}.")
                    print(f"Alguien debe comprar a este jugador obligatoriamente.")
                    continue

            elif cmd_lower.startswith("pagar "):
                partes = comando.split()
                if len(partes) != 3:
                    print("Comando incorrecto. Formato: pagar <nombre> <monto>")
                    continue

                nombre_part = partes[1]
                try:
                    monto = int(partes[2])
                except:
                    print("Monto inválido.")
                    continue

                if nombre_part not in participantes:
                    print("Nombre de participante inválido.")
                    continue
                
                # Verificar si el participante ya compró en esta plaza
                ya_compro = any(
                    j.get("_pos_slot") == pos and j.get("_slot_index") == slot_index 
                    for j in participantes[nombre_part]["plantel"]
                )
                if ya_compro:
                    print(f"❌ {nombre_part} ya compró un jugador para esta plaza ({plaza_desc}).")
                    print("Cada participante solo puede comprar UN jugador por plaza.")
                    continue

                if monto > participantes[nombre_part]["presupuesto"]:
                    print(f"{nombre_part} no tiene suficiente presupuesto.")
                    continue

                # registrar compra
                participantes[nombre_part]["presupuesto"] -= monto
                participantes[nombre_part]["plantel"].append(jugador)
                print(f"\n✅ {nombre_part} compró a {jugador['Jugador']} ({jugador['Posicion']}) por {monto} millones.")

                # eliminar del pool_copy (para que no se repita)
                for i, x in enumerate(pool_copy):
                    if (
                        x["Posicion"] == jugador["Posicion"]
                        and x["Jugador"] == jugador["Jugador"]
                        and x["Nacionalidad"] == jugador["Nacionalidad"]
                    ):
                        pool_copy.pop(i)
                        break
                break

            else:
                print("Comando inválido. Use 'pagar <nombre> <monto>' o 'paso'")

        # mostrar balances
        print("\n=== Balance actual ===")
        for p, datos in participantes.items():
            print(f"{p}: {datos['presupuesto']} millones")

        input("\nPresione Enter para continuar...\n")

print("\n🏁 Fin de la subasta. No quedan más candidatos.\n")

# =============================
# Resumen final
# =============================
print("=== RESULTADO FINAL ===")
for p, datos in participantes.items():
    print(f"\n{p} - Presupuesto final: {datos['presupuesto']} millones")
    print("Plantel adquirido:")
    for j in datos["plantel"]:
        print(f" - {j['Jugador']} ({j['Posicion']}, {j['Nacionalidad']})")
