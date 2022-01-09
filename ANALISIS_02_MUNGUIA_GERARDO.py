import csv

#La función "sublistar" crea una sublista de las entradas que cumplen con la condición de tener el dato "criterio" en la columna "col"
def sublistar(lista, criterio, col):
    sublista = []
    for fila in lista:
        if fila[col]== criterio:
            sublista.append(fila)
    return sublista

#La función "pon_valor" regresa una lista de cada ruta con una sublista del valor de cada entrada y un diccionario con el número de entradas de la ruta y su valor total
def pon_valor(lista, rutas):
    sublista = []
    for ruta in rutas:
        sublista2 = []
        for entrada in lista:
            if ((entrada[2], entrada[3], entrada[-3]) == ruta):
                sublista2.append(int(entrada[-1]))
        sublista.append((ruta, sublista2, len(sublista2), sum(sublista2)))
    return sublista

#La función haz_dic hace un diccionario usando la ruta como clave, y mete el valor total y la frecuencia de c/u
def haz_dic(lista):
    dicc = dict()
    dicc[lista[0]] = (lista[1], lista[2], lista[3])
    return dicc
        #dic[f"valor{ruta[0]}-{ruta[1]}"] = sum(sublista2)
        #dic[f"demanda{ruta[0]}-{ruta[1]}"] = len(sublista2)

#primero, convierto la base de datos en una lista llamada "archivo"
with open("synergy_logistics_database.csv") as database:
    archivo = list(csv.reader(database))
#luego, la divido en dos listas, "exportaciones" e "importaciones"
exportaciones = sublistar(archivo,"Exports",1)
print("Número de exportaciones: ", len(exportaciones)) # hay 15,408 exportaciones
importaciones = sublistar(archivo, "Imports", 1)
print("Número de importaciones: ", len(importaciones)) # hay 3,648 importaciones

"""
#Investigo cuántas rutas hay en general, y cuántas parejas de países
conjunto = set()
#conjunto2 = set()
for line in archivo:
    if line[2]=="origin":
        continue
    conjunto.add((line[2], line[3]))
    #conjunto2.add(frozenset((line[2], line[3])))
#print(len(conjunto)) #hay 172 rutas
#print(len(conjunto2)) #127 parejas de países
"""
#Obtengo las rutas de exportación e importación
rutas_exp, rutas_imp = set(), set()
for line in exportaciones:
    rutas_exp.add((line[2], line[3], line[-3]))
print("Rutas de exportaciones: ",len(rutas_exp)) #hay 163 rutas de exportaciones
for line in importaciones:
    rutas_imp.add((line[2], line[3], line[-3]))
print("Rutas de importaciones: ",len(rutas_imp)) #hay 52 rutas de importaciones
print("Rutas de ambas: ", len(rutas_exp.intersection(rutas_imp))) #hay 13 rutas que son de ambas
#Obtengo los medios de transporte y los paises en los que opera la empresa
medios = set()
paises = set()
for line in archivo:
    if line[1]=="direction":
        continue
    medios.add(line[-3])
    paises.add(line[2])
    paises.add(line[3])
print(f"\nHay {len(medios)} medios de transporte: ")
for medio in medios:
    print(medio)
print(f"\nLa empresa opera en {len(paises)} países")
"""
#ahora quiero comprobar si hay rutas con más de un medio de transporte
for ruta in rutas_exp:
    conj = set()
    for line in exportaciones:
        if (line[2], line[3]) == ruta:
            conj.add(line[-3])
    if len(conj) != 1:
        print(f"La ruta {ruta[0]}-{ruta[1]} tiene {len(conj)} medios de transporte")
"""
#Calculo el valor y la frecuencia de cada ruta de exportación e importación
valor_exp = pon_valor(exportaciones, rutas_exp)
valor_exp.sort(key=lambda x: x[-1], reverse=True)
exp_mas_valor = set()
print("\nLas diez rutas de exportación que generan más valor son: ")
for i in range(10):
    exp_mas_valor.add(valor_exp[i][0])
    print(f"La ruta {valor_exp[i][0][0]} - {valor_exp[i][0][1]} via {valor_exp[i][0][2]} con ${valor_exp[i][-1]}")
valor_imp = pon_valor(importaciones, rutas_imp)
valor_imp.sort(key=lambda x: x[-1], reverse=True)
imp_mas_valor = set()
print("\nLas diez rutas de importación que generan más valor son: ")
for i in range(10):
    imp_mas_valor.add(valor_imp[i][0])
    print(f"La ruta {valor_imp[i][0][0]} - {valor_imp[i][0][1]} via {valor_imp[i][0][2]} con ${valor_imp[i][-1]}")
valor_exp.sort(key=lambda x:x[-2], reverse=True)
exp_mas_demanda = set()
print("\nLas diez rutas de exportación más demandadas son: ")
for i in range(10):
    exp_mas_demanda.add(valor_exp[i][0])
    print(f"La ruta {valor_exp[i][0][0]} - {valor_exp[i][0][1]} via {valor_exp[i][0][2]} con {valor_exp[i][-2]} exportaciones")
valor_imp.sort(key=lambda x:x[-2], reverse=True)
imp_mas_demanda = set()
print("\nLas diez rutas de importación más demandadas son: ")
for i in range(10):
    imp_mas_demanda.add(valor_imp[i][0])
    print(f"La ruta {valor_imp[i][0][0]} - {valor_imp[i][0][1]} via {valor_imp[i][0][2]}  con {valor_imp[i][-2]} importaciones")
#Rutas más demandadas que están dentro de las que generan más valor: 
print("\nIntersección de rutas de exportación más demandadas y más valiosas: ", len(exp_mas_demanda.intersection(exp_mas_valor)))
print("Intersección de rutas de importación más demandadas y más valiosas", len(imp_mas_demanda.intersection(imp_mas_valor)))

#Creo un diccionario con listas de las exportaciones e importaciones de cada medio de transporte
dicc_medios = dict()
for medio in medios:
    dicc_medios[f"exp_{medio}"] = sublistar(exportaciones, medio, -3)
    dicc_medios[f"imp_{medio}"] = sublistar(importaciones, medio, -3)
#Calculo el valor de cada medio de transporte
valores_medios, valores_medios_exp, valores_medios_imp = [], [], []
for medio in medios:
    exp, imp = 0, 0
    for line in dicc_medios[f"exp_{medio}"]:
        exp+=int(line[-1])
    valores_medios_exp.append((exp, medio))
    for line in dicc_medios[f"imp_{medio}"]:
        imp+=int(line[-1])
    valores_medios_imp.append((imp, medio))
    valores_medios.append((imp+exp, medio))
#Encuentro los medios que generan mayores ganancias
valores_medios_exp.sort(reverse=True)
print("\nValor de las exportaciones por medio de transporte: ")
#total_medios_exp = 0
for valor in valores_medios_exp:
    print(f"El valor de las exportaciones por {valor[1]} es: ${valor[0]}")
    #total_medios_exp+=valor[0]
#print("Total exp: ", total_medios_exp)
valores_medios_imp.sort(reverse=True)
print("\nValor de las importaciones por medio de transporte: ")
#total_medios_imp = 0
for valor in valores_medios_imp:
    print(f"El valor de las importaciones por {valor[1]} es: ${valor[0]}")
    #total_medios_imp+=valor[0]
#print("Total imp: ", total_medios_imp)
valores_medios.sort(reverse=True)
print("\nValor de total de cada medio de transporte: ")
for valor in valores_medios:
    print(f"El valor total del medio {valor[1]} es: ${valor[0]}")

"""
#prueba para encontrar totales:
suma_exp=0
for entrada in exportaciones:
    suma_exp+=int(entrada[-1])
print("La suma de exportaciones es: ", suma_exp)
suma_imp=0
for entrada in importaciones:
    suma_imp+=int(entrada[-1])
print("La suma de importaciones es: ", suma_imp)
"""

#Encuentro los países que representan el 80% de los ingresos
#1) obtener el ingreso que representa cada país 
#2) mientras se va recorriendo, obtener el total (como se suma dos veces será el doble), y
#3) guardar en una lista estos valores, ordenarlo, luego ir metiendo en un set los países con un while
total_exp, total_imp = 0, 0
valores_pais_exp, valores_pais_imp = [], []
for pais in paises:
    total_pais_exp, total_pais_imp = 0, 0
    for entrada in exportaciones:
        if pais == entrada[2] or pais == entrada[3]:
            total_exp+=int(entrada[-1])
            total_pais_exp+=int(entrada[-1])
    valores_pais_exp.append((total_pais_exp, pais))
    for entrada in importaciones:
        if pais == entrada[2] or pais == entrada[3]:
            total_imp+=int(entrada[-1])
            total_pais_imp+=int(entrada[-1])
    valores_pais_imp.append((total_pais_exp, pais))
#print("Doble suma exportaciones: ", total_exp)
#print("Doble suma importaciones: ", total_imp)
valores_pais_exp.sort(reverse=True)
"""
for i in range(10):
    print(valores_pais_exp[i])
"""
acumulado, i = 0, 0
paises_exp_80 = set()
print("\nValor de las exportaciones por país: ")
while acumulado < total_exp*0.8:
    print(f"{valores_pais_exp[i][1]} con ${valores_pais_exp[i][0]}")
    paises_exp_80.add(valores_pais_exp[i][1])
    acumulado+=valores_pais_exp[i][0]
    i+=1
print("\nLa suma total del valor de cada pais de exportaciones es: $", total_exp)
print("El 80% de este valor es $", total_exp*0.8)
print("El valor que representan las exportaciones de estos países es: $", acumulado)
valores_pais_imp.sort(reverse=True)
acumulado, i = 0, 0
paises_imp_80 = set()
print("\nValor de las importaciones por país: ")
while acumulado < total_imp*0.8:
    print(f"{valores_pais_imp[i][1]} con ${valores_pais_imp[i][0]}")
    paises_imp_80.add(valores_pais_imp[i][1])
    acumulado+=valores_pais_imp[i][0]
    i+=1
print("\nLa suma total del valor de cada pais de importaciones es: $", total_imp)
print("El 80% de este valor es $", total_imp*0.8)
print("El valor que representan las importaciones de estos países es: $", acumulado)

#Encuentro si los paises que generan el 80% de los ingresos se encuentran en las rutas más demandadas
print("\nRutas de exportación con más valor que tienen un país top 80%")
for ruta in exp_mas_valor:
    if ruta[0] in paises_exp_80 or ruta[1] in paises_exp_80:
        print(f"La ruta {ruta[0]}-{ruta[1]} via {ruta[2]}")
print("\nRutas de importación con más valor que tienen un país top 80%")
for ruta in imp_mas_valor:
    if ruta[0] in paises_imp_80 or ruta[1] in paises_imp_80:
        print(f"La ruta {ruta[0]}-{ruta[1]} via {ruta[2]}")
"""
print("\nRutas de exportación con más valor por mar o tren: ")
for ruta in exp_mas_valor:
    if ruta[2] in {'Sea', 'Rail'}:
        print(ruta)
"""