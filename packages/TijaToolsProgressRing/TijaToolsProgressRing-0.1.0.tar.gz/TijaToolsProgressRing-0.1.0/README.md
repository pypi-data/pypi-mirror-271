# TijaToolsProgressRing

## Leírás

A TijaToolsProgressRing egy Python csomag, amely lehetővé teszi, hogy dinamikus és testre szabható progress ringeket jeleníts meg a terminálban. Ez ideális eszköz hosszú futású műveletek állapotának vizuális visszajelzésére.

## Telepítés

Telepítsd a csomagot a következő paranccsal:

```bash
pip install TijaToolsProgressRing

## Használat
from tijatoolsprogressring import ProgressRing

# Példányosítsd a ProgressRing osztályt
ring = ProgressRing()

# Indítsd el az animációt
ring.run_with_animation()
