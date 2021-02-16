# Zápočtový program 1.roč. BC, ZS 2020/21, NPRG030 - Gabriela Závodská
Verzia hry Minesweeper (míny) s AI schopnou dávať rady o štvorčekoch, ktoré sú bezpečné na kliknutie.
# Dokumentácia
## Používanie
### Spustenie programu:
Na spustenie hry je potrebné spustiť súbor *main.py*, spúšťa sa level _easy_.

### Ovládanie hry:
- RMB
  * Kliknutím pravým tlačítkom myši na prázdne (čierne) políčko sa naň vyznačí vlajka,kliknuím na políčko s vlajkou sa vlajka vymaže.
  * Pri kliknutí na ľubovolné iné políčko sa nebude diať nič.
- LMB
  * Kliknutím ľavým tlačítkom myši na prázdne políčko sa dané políčko odokryje. Viac o význame odokrytých políčok [tu](https://github.com/GabiZavod/Zapoctak-ZS1BC#v%C3%BDznam-pol%C3%AD%C4%8Dok).
  * Kliknutím na iné políčko (odokryté alebo označené vlajočkou) sa nič nestane. Pri kiknutí na tlačítko `GIVE HINT` sa vyžiada rada od AI. Viac o jej fungovaní [tu](https://github.com/GabiZavod/Zapoctak-ZS1BC#hinty-rady).
- SPACE
  * Stlačením medzerníku sa spustí nová hra, úroveň sa zachová.
- Kláves E
  * Stlačením klávesu E sa nastaví úroveň hry na *easy*.
- Kláves M
  * Stlačením klávesu M sa nastaví úroveň hry na *medium*.
- Kláves H
  * Stlačením klávesu H sa nastaví úroveň hry na *hard*.
##### Poznámka:
Úroveň hry je možné meniť len keď hráč danú hru vyhrá alebo prehrá, počas rozohratej hry nie je možné meniť úroveň. Novú hru vrámci tej istej úrovni je možné spustiť hocikedy.

### Pravidlá hry:
#### Cieľ hry
Cieľom hry je správne označiť všetky míny. Ak sa toto splní, hra končí výťazstvom, čo indikuje text "YOU WON" na hornej lište. Na tejto lište je viditeľný aj počet mín (MINES) a počet zatiaľ označených mín (FLAGS).
#### Prehra
Prehra nastane v prípade, že hráč klikne na políčko s mínou, túto situáciu indikuje text "GAME OVER" na hornej lište a zobrzenie všetkých umiestnených mín.
#### Úrovne hry
Úroveň hry je určená tromi faktormi: počtom mín, veľkosťou hracej plochy a pomerom políčok s mínami ku všetkým políčkam (v percentách).
- **Easy**: V úrovni easy sa na hracej ploche veľkosti 8 x 10 (riadky x stĺpce) nachádza 10 mín, čiže 12,5% políčok tvoria míny.
- **Medium**: V úrovni medium sa na hracej ploche veľkosti 14 x 18 (riadky x stĺpce) nachádza 40 mín, čiže zaokrúhlene 15,87% políčok tvoria míny.
- **Hard**: V úrovni hard sa na hracej ploche veľkosti 20 x 24 (riadky x stĺpce) nachádza 99 mín, čiže 20,625% políčok tvoria míny.
#### Význam políčok
- **Čierne políčko**: značí zatiaľ neodkryté políčko, môže sa pod ním skrývať čokoľvek
- **Sivé políčko**: značí odokryté políčko, ktoré nemá ani jedného suseda obsahujúceho mínu
- **Políčko s číslicou N**: značí odokryté políčko, ktoré má presne N susedných políčok obsahujúcich mínu. Rôzne číslice majú rôzne farby.
- **Červené políčko s čiernym kruhom uprostred**: značí odokryté políčko s mínou. Pri zobrazení takéhoto políčka sa zároveň zobrazia všetky políčka obsahujúce mínu a nastáva prehra.
- **Políčko s vlajočkou**: hráč môže ľubovolné políčko označiť vlajočkou, primárne však slúži na označenie políčok, o ktorých sa domnieva, že obsahujú mínu. Na dosiahnutie výhry je potrebné, aby sa počet vlajočiek a počet mín rovnal a zároveň aby boli vlajočky umiestnené na políčkach s mínami.

### Hinty (rady):
Hráč si kliknutím na tlačítko `GIVE HINT` môže vyžiadať radu od AI, ktorá pracuje len s viditeľnými informáciami (odokrytými políčkami a políčkami označenými vlajočkou) a na základe nich nafarbí na žlto políčko, ktoré nebude obsahovať mínu a hráč naňho môže kliknúť (LMB). Samozrejme, ak hráč niekde spravil chybu, môže po kliknutí na vyznačené políčko naraziť na mínu - to ale nie je chyba programu, ale hráča. Ak AI na základe viditeľných informácií nenájde políčko, na ktoré je bezpečné kliknúť, pod talčítkom `GIVE HINT` sa objaví informácia "No hints". Potom by mal hráč porozmýšlať, či nie je na ploche políčko, ktoré môže označiť ako mínu, alebo musí kliknutie (LMB) na ďalšie políčko voliť náhodne.

## Popis programu

