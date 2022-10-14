import mysql.connector

"""
1. Interrogazione
unisco: 'ordine' (uid, oid, stid, time, inid, paspid) con 'stato' (stid, nome) combinando la stid 

Voglio conoscere lo stato degli ordini per ogni città quindi unisco alla tabella anche indirizzo 
(inid, uid, via, numero, provincia, citta, cap, tel, nome, cognome, principale)
grazie alla 'uid' comune sia a 'ordine' che a 'stato'.
Le ordino
"""
conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select ordine.uid, indirizzo.citta,stato.nome from ordine, stato, indirizzo where ordine.stid = stato.stid and ordine.uid = indirizzo.uid  order by indirizzo.citta asc;"
cursor.execute(sql)
result = cursor.fetchall()
for elem in result:
    print(elem[1:3])
conn.close()
print('\n')
conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select ordine.uid, indirizzo.citta,stato.nome from ordine, stato, indirizzo where ordine.stid = stato.stid and ordine.uid = indirizzo.uid  order by indirizzo.citta asc;"
print('QUERY1. STATO DEGLI ORDINI PER OGNI CITTA')
cursor.execute(sql)
result = cursor.fetchall()
print(result)
conn.close()

print('\n')
"""
2.INTERROGAZIONE
collego 'ordine'(uid, oid, stid, time, inid, paspid) con 'stato' (stid, nome) grazie a 'stid'

Ottengo la data e orario degli ordini ancora in elaborazione
"""
conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select ordine.time, stato.nome, ordine.stid from ordine, stato where nome like 'in%';"
print('QUERY2. DATA E ORARIO ORDINI ANCORA IN ELABORAZIONE')
cursor.execute(sql)
result = cursor.fetchall()
for elem in result:     #mi stampo solo la data con lo stato elaborazione in corso
    print(elem[0:2])
conn.close()

print('\n')
"""
3. INTERROGAZIONE
Cerco i motivi per i quali i prodotti non sono stati ancora spediti e quindi se è un problema di DHL o di ritiro
"""

conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select stato.nome, spedizione.nome, spedizione.costo, ordine.time from stato, ordine, pasp01, spedizione where stato.stid=ordine.stid and ordine.paspid=pasp01.paspid order by spedizione.nome;"
print('QUERY3. PRODOTTI NON CONSEGNATI DIVISI PER SPEDIZIONE:')
cursor.execute(sql)
result = cursor.fetchall()
print(result)
for elem in result:     #mi stampo solo la data con lo stato elaborazione in corso
    if elem[0] == 'in elabora-zione': #mi estraggo solo gli ordini in elaborazione
        elem = elem[0:2]
    print(elem[1])
conn.close()

print('\n')
"""
4. INTERROGAZIONE
Unisco listino con utente per conoscere ciascuna persona se ha comprato come rivenditore o per uso personale
Ho ottenuto che solo 3 sono rivenditori
"""
conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select count(listino.nome), listino.nome, listino.lsid, utente.cfisc, utente.uid from utente join listino on listino.lsid=utente.lsid group by listino.nome;"
cursor.execute(sql)
result = cursor.fetchall()
print('QUERY4. TIPOLOGIA DI ACQUIRENTI SUL SITO (RIVENDITORE, STANDARD')
for elem in result:
    elem = elem[0:2]
    print(elem)
result = result[1:3]
print(result)
conn.close()
print('\n')
"""
5. INTERROGAZIONE
Oggetti acquistati da utenti parent
"""

conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select parent, nome, pid from prodotto, subcat where prodotto.cid = subcat.parent;"
cursor.execute(sql)
result = cursor.fetchall()
print('QUERY.5 OGGETTI ACQUISTATI SUL SITO DAI GENITORI')
for elem in result:
    elem = elem[1]
    print(elem)
conn.close()
print('\n')
"""
6. INTERROGAZIONE
Oggetti acquistati da utenti child
"""

conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select child, nome, pid from prodotto, subcat where prodotto.cid = subcat.child;"
cursor.execute(sql)
result = cursor.fetchall()
print('QUERY6. OGGETTI ACQUISTATI DAI FIGLI')
for elem in result:
    elem = elem[1]
    print(elem)
conn.close()
print('\n')
"""
7. INTERROGAZIONE
collego 'categoria' (cid, nome) con prodotto (pid, nome dei singoli articoli, descr.bt, descr.lt, cid, quantita.magazzino, arrivo, impegnati, mid) 
grazie al 'cid' e 'orp01 as ordinato'(oid, pid, quantita, prezzo, lisid) con prodotto grazie al 'pid'.

Ho ordinato per nome, ottenendo, suddivisi per categorie, lo stato dei prodotti in magazzino, in base alle quantita ordinate e al prezzo dei 
prodotti (il prezzo mi ha permesso di suddividere le categorie in sottocategorie di prodotti similari, nel caso in quanto il cliente potrebbe essere interessato ad un 
prodotto compatibile)
"""

conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select distinct categoria.nome, prodotto.quantita as magazzino, ordinato.quantita, ordinato.prezzo, prodotto.arrivo as ordini from categoria, prodotto, orpr01 as ordinato where categoria.cid=prodotto.cid and ordinato.pid=prodotto.pid order by nome;"
cursor.execute(sql)
result = cursor.fetchall()
print('Query 7: Ciascun prodotto diviso per categoria, in base alla quantità presente \nin magazzino, a quella ordinata ed al prezzo, è la seguente:')
for elem in result:
    elem = elem[0:4]
    print(elem)
conn.close()
print('\n')
"""
8. INTERROGAZIONE
collego 'prodotto' con 'orpr01', 'orpr01' con 'ordine', 'ordine' con 'indirizzo' 
Ho ordinato per codice prodotto, ottenendo per ciascun prodotto, il prezzo, lo stato di spedizione, l'utente che l'ha acquistato e quindi l'indirizzo di spedizione.
"""

conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select prodotto.nome, orpr01.prezzo, indirizzo.via, indirizzo.numero, indirizzo.provincia, indirizzo.citta, indirizzo.nome, indirizzo.cognome, ordine.time, ordine.oid, ordine.uid, indirizzo.uid from prodotto, orpr01, ordine, indirizzo where prodotto.pid=orpr01.pid and orpr01.oid=ordine.oid and indirizzo.inid=ordine.inid order by ordine.oid;"
cursor.execute(sql)
result = cursor.fetchall()
print('QUERY8. ')
for elem in result:
    elem = elem[0:10]
    print(elem)
conn.close()
print('\n')
"""
9. INTERROGAZIONE
collego 'indirizzo' con 'ordine' e 'orpr01' con 'ordine' 
Ottengo il numero di ordini per citta e per prezzo
"""
conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select citta, count(indirizzo.citta), sum(prezzo), provincia from ordine, indirizzo, orpr01 where indirizzo.inid=ordine.inid and ordine.oid=orpr01.oid group by indirizzo.citta having count(indirizzo.citta);"
cursor.execute(sql)
result = cursor.fetchall()
print('QUERY9 Numero Di Ordini Per Citta')
print("citta, tot.prodottiSpediti, sommaPrezzi")
for elem in result:
    elem = elem[0:3]
    print(elem)
conn.close()

"""
10. INTERROGAZIONE
collego 'utente' con 'ordine' e 'orpr01' con 'utente' (anche indirizzo con orpr01) 
Ottengo l'acquirente che ha speso di più e al quale inviare il mio sconto premio
"""
conn = mysql.connector.connect(user='root', password='Pinam0nt01', host='127.0.0.1', database='ecommerce')
cursor = conn.cursor()
sql = "select cfisc, utente.nome, utente.cognome, sum(quantita), sum(prezzo), citta, provincia, utente.uid from ordine, utente, orpr01, indirizzo where indirizzo.inid=ordine.inid and utente.uid=ordine.uid and ordine.oid=orpr01.oid group by utente.cfisc order by sum(prezzo) desc;"
cursor.execute(sql)
result = cursor.fetchall()
print('\n')
print('QUERY10. Ottengo acquirente che ha speso di più e al quale inviare il mio sconto premio a Natale')
print("        CF    ,  nome ,    cognome,  sommaProdotti ,  sommaPrezzo")
for elem in result:
    elem = elem[0:5]
    print(elem)
conn.close()