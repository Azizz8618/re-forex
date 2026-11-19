# Эталонные образы (read-only)

Каталог содержит **неизменяемые** копии входных эталонов, используемых
регрессионными сценариями из [`tests/`](../tests/README.md). Файлы копируются «как есть»;
нормализация (даты/заголовки) выполняется только в временных каталогах сценариев.

Три разные сборки ФОРЭКС не смешиваются:

| Эталон | Версия | Источник |
|---|---|---|
| `forex.b6` + `output.gold.txt` | 2.02 от 15.07.80 | dispak, решето Эратосфена |
| `expect_forex.txt` | 4.13 от 11.09.85 | dubna-tests |
| `expect_library21.txt`, `expect_whatis_monsys.txt` | LIBREFER / monsys (FOREX 412) | dubna-tests |

## Происхождение и контрольные суммы

| Файл | Происхождение | SHA256 |
|---|---|---|
| `forex.b6` | `/home/azizz/Yandex.Disk/dispak/tests/forex/forex.b6` | `3aea9f44bcf12d0080995516094f7a894c869ce8fbabe2978a79c1ca2c99fd07` |
| `options.txt` | `/home/azizz/Yandex.Disk/dispak/tests/forex/options.txt` (содержит `forex.b6`) | `02ad8c79e443526bbdf180ec24ccb85c75087047d69dfe2e3a072fd6d782424b` |
| `output.gold.txt` | `/home/azizz/Yandex.Disk/dispak/tests/forex/output.txt` (эталон с wildcard `##.##.##` в строке даты) | `a97f595863ea70417fc2a71c43e0104b22182a2ff678006ee7a287e1ce028f28` |
| `expect_forex.txt` | `/home/azizz/Yandex.Disk/besm6-new/dubna/tests/expect_forex.txt` | `8b0b9c10c1861b5bb55a0fee9367b26a8162bc161b2a8ad0d1f8a6a409676221` |
| `expect_library21.txt` | `/home/azizz/Yandex.Disk/besm6-new/dubna/tests/expect_library21.txt` | `b70ae9e8852f08f53afa2971f9947ab69d429afa148b6f13839b724d34910577` |
| `expect_whatis_monsys.txt` | `/home/azizz/Yandex.Disk/besm6-new/dubna/tests/expect_whatis_monsys.txt` | `67610d33c97f1371b18f7ddf8472fea305ba1f0866d81a3d66cfe676cc9690d8` |
| `libra211.forex.inc` | `libra211.l21`, строки 15448–15528 (MOD `FOREX*`, ENTRY `INITFOR*`, `LOREX`, `RMON`, `STOP/`) | `d18f35494a2b5007145dc7c272be564c29ba1e89fa4935f69133dad665455a24` |
| `libra211.givpg.inc` | `libra211.l21`, строки 16780–16836 (MOD `GIV/PG`, `TAK/PG`) | `f06adebd9d2c6870c67068ee47e3cb8fc41614a0d1fe1afd0e9a38b0a7f9decd` |

`libra211.l21` = `/home/azizz/besm6.github.io/sources/dubna/besml21/libra211.l21`
(SHA256 `b98b7e8f47d2bec17591f1f28fe6d647facb9997db02208b6f895a4491bc7250`);
полный файл в репозиторий не копируется — сохранены только две вырезки.

## Внешние артефакты (в репозиторий НЕ копируются)

- Лента `/home/azizz/Yandex.Disk/besm6-new/besm6.net/tapes/monsys.9` (1 769 472
  байт) — оверлеи выгружаются `dd bs=6 skip=$((8#241500 / 277500)) count=1024`
  сценарием `tests/verify-dumps.sh`; полная копия ленты не сохраняется.
- Бинарник `/home/azizz/Yandex.Disk/dispak/build/dispak/dispak` — вызывается
  сценарием `tests/run-forex.sh` (путь переопределяется через `DISPAK_BIN`).

## Проверка целостности

```sh
cd reference
sha256sum forex.b6 options.txt output.gold.txt expect_*.txt libra211.*.inc
```
