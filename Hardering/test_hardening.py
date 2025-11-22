from esegutore import esegui_script_remoto
pathBase="/home/giovanni/Uni/cyber/esercizi/Hardering/"
def pathFornerto(relativo: str) -> str:
    return pathBase+relativo

esegui_script_remoto(pathFornerto("creaUtente/creaUtente.sh"))

