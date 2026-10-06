def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = []
    try:
        file = open(file_path, "r")
        prima_riga = True
        for riga in file:
            if prima_riga:
                prima_riga = False
                continue
            dati = riga.strip().split(",")
            codice = dati[0]
            titolo = dati[1]
            autore = dati[2]
            mese = int(dati[3])
            anno = int(dati[4])
            foto = [codice, titolo, autore, mese, anno]
            trovato = False
            for gruppo in album :
                if gruppo[0][4] == anno:
                    gruppo.append(foto)
                    trovato = True
            if trovato == False:
                album.append([foto])
        file.close()
        return album
    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if mese < 1 or mese > 12:
        return None
    #controllo che il codice non esista gia
    for gruppo in album:
        for foto in gruppo:
            if foto[0] == codice:
                return None
    nuova_foto = [codice, titolo, autore, mese, anno]
    trovato = False
    for gruppo in album:
        if gruppo[0][4] == anno:
            gruppo.append(nuova_foto)
            trovato = True
    if trovato == False:
        album.append([nuova_foto])
    file = open(file_path, "a")
    file.write(codice + "," +titolo + "," + autore + "," + str(mese) + "," + str(anno) + "\n")
    file.close()
    return nuova_foto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for gruppo in album :
        for foto in gruppo :
            if foto[0] == codice:
                risultato = (foto[0] + "," + foto[1] + "," + foto[2] + ", " + str(foto[3]) + ", " + str(foto[4]))
                return risultato
    return None

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    titoli = []
    for gruppo in album:
        if gruppo[0][4] == anno:
            for foto in gruppo:
                titoli.append(foto[1])
    if len(titoli) == 0:
        return None
    titoli.sort()
    return titoli


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
