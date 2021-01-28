def decif(texto):
    n=3 #desplazamiento
    abc = "0123456789abcdefghijklmnopqrstuvwxyz"
    descifrado = ""
    for l in texto:
        pos_letra = abc.index(l)
        # Restamos para movernos a la izquierda
        nueva_pos = (pos_letra - n)
        descifrado += abc[nueva_pos]
    return descifrado

def cif(texto):
    n=3 #desplazamiento
    abc = "0123456789abcdefghijklmnopqrstuvwxyz"
    cifrado = ""
    for l in texto:
        # Si la letra esta en el abecedario se reemplaza
        if l in abc:
            pos_letra = abc.index(l)
            # Sumamos para movernos a la derecha del abc
            nueva_pos = (pos_letra + n) % len(abc)
            cifrado+= abc[nueva_pos]
        else:
            # Si no esta en el abecedario solo aniadelo
            cifrado+= l
    return cifrado