# 🔐 Utenti Attivi - Licenze

**Software per il monitoraggio degli utenti attivi sulle licenze ADAMS e ANSYS**, sviluppato dal **Team IT** per conto di **Salvatore Alessi**.

---

## 📌 Funzionalità

- Interfaccia grafica basata su **Tkinter**
- Connessione automatica al **server licenze**
- Visualizzazione degli utenti connessi con:
  - Tipo di licenza (ADAMS o ANSYS)
  - Nome utente
  - Host
  - Data e ora
- Filtro per tipo di licenza
- Controllo MAC Address (autorizzazione all'uso)
- Finestra informativa con crediti e condizioni d'uso
- Cifratura dei dati host tramite algoritmo XOR
- Compatibile con **PyInstaller** per la generazione di eseguibili standalone

---

## 🛠️ Requisiti

- Python 3.8+
- Moduli richiesti:
  ```bash
  pip install ttkthemes
