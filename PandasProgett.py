from sqlalchemy import create_engine
import pandas as pd

"""
Query1
"""
db_connection_str = 'mysql+pymysql://root:Pinam0nt01@127.0.0.1/ecommerce'
db_connection = create_engine(db_connection_str)
citta_statoprodotto = pd.read_sql("select ordine.uid, indirizzo.citta,stato.nome from ordine, stato, indirizzo "
                                  "where ordine.stid = stato.stid and ordine.uid = indirizzo.uid  order by indirizzo.citta asc;", db_connection)
#print(citta_statoprodotto)
citta_statoprodotto=citta_statoprodotto[['citta','nome']]
print(citta_statoprodotto)

"""
Query2
"""
time_statoprodotto = pd.read_sql("select ordine.time, stato.nome, ordine.stid from ordine, stato;", db_connection)
print(time_statoprodotto)

"""
Query3
"""
statoprodotto_tipospedizione = pd.read_sql("select stato.nome, spedizione.nome, spedizione.costo, ordine.time from stato, ordine, pasp01, spedizione "
                                           "where stato.stid=ordine.stid and ordine.paspid=pasp01.paspid", db_connection)
print(statoprodotto_tipospedizione)
"""
Query.4
"""
tipovenditore_cf = pd.read_sql("select listino.lsid, listino.nome, utente.cfisc, utente.uid from utente join listino on listino.lsid=utente.lsid", db_connection)
print(tipovenditore_cf)
"""
Query.5
"""
time_statoprodotto = pd.read_sql("select parent, child, nome, pid from prodotto, subcat "
                                 "where prodotto.cid = subcat.parent", db_connection)
print(time_statoprodotto)
"""
Query.7
"""
stato_prodotti_magazzino = pd.read_sql("select distinct categoria.nome, prodotto.quantita as magazzino, ordinato.quantita, ordinato.prezzo, prodotto.arrivo as ordini "
                                       "from categoria, prodotto, orpr01 as ordinato "
                                       "where categoria.cid=prodotto.cid and ordinato.pid=prodotto.pid order by nome;", db_connection)
print(stato_prodotti_magazzino)
"""
Query.8
"""
prodotti_per_utente = pd.read_sql("select "
                                  "prodotto.nome, orpr01.prezzo, indirizzo.via, indirizzo.numero, indirizzo.provincia, "
                                  "indirizzo.citta, indirizzo.nome, indirizzo.cognome, ordine.time, ordine.oid, ordine.uid, indirizzo.uid "
                                  "from prodotto, orpr01, ordine, indirizzo "
                                  "where prodotto.pid=orpr01.pid and orpr01.oid=ordine.oid and indirizzo.inid=ordine.inid order by ordine.oid;", db_connection)
print(prodotti_per_utente)
"""
Query.9
"""
np_pspediti_per_citta = pd.read_sql("select citta, provincia, count(indirizzo.citta), sum(prezzo) from ordine, indirizzo, "
                                    "orpr01 where indirizzo.inid=ordine.inid and ordine.oid=orpr01.oid group by indirizzo.citta "
                                    "having count(indirizzo.citta);",db_connection)
print(np_pspediti_per_citta) #numero prodotti spediti per citta
"""
Query10
"""

utente_sommapSpeso = pd.read_sql("select cfisc, utente.nome, utente.cognome, sum(quantita), sum(prezzo), citta, provincia, utente.uid "
                                 "from ordine, utente, orpr01, indirizzo where indirizzo.inid=ordine.inid and utente.uid=ordine.uid and ordine.oid=orpr01.oid "
                                 "group by utente.cfisc order by sum(prezzo) desc;", db_connection)
print(utente_sommapSpeso)