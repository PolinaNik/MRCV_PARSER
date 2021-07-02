# Парсер логов с метео сервера

Скрипт находит расхождение в сообщениях по времени более 1 мин и создает файл, в который заносятся ошибки.
Всего 3 скрипта для каждого типа сообщения:
1) parser_mrcv_KRUM.py
2) parser_mrcv_METAR.py
3) parser_mrcv_SIGMET.py
На каждый лог свой отдельный файл с ошибками, если ошибок нет, то файл не создается.
Результат обработки будет находиться в созданных скриптом папках:
result_KRUM, result_METAR, result_SIGMET.

# Инструкция

В папке, где лежит скрипт, создать папку files и в нее поместить все mrcv логи.
Запустить нужный скрипт, либо поочередно: parser_mrcv_KRUM.py, parser_mrcv_METAR.py, parser_mrcv_SIGMET.py

_Результат обработки будет находиться в созданных скриптом папках:
result_KRUM, result_METAR, result_SIGMET._
