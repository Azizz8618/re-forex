# src/reloc/

Каталог зарезервирован для будущих релоцируемых (позиционно-независимых)
исходников символической переписки FOREX 5.00 по плану
`docs/plan-f77-full/56-symbolic-rewrite-plan.md` (фазы F1–F3).

Предполагаемые файлы (пока НЕ созданы, в F0 добавляется только этот README):

- `FOREX_ROOT.reloc.mad` — символический корень из среза `libra211.l21:15448-15528` (F1);
- `LO_SYN.reloc.mad`, `LO_GEN.reloc.mad` — релоцируемые оверлеи (F3);
- `FXLODR.mad` — загрузчик оверлеев (F2b).

Эталонные исходники (`src/FOREX_CORE.mad`, `include/FOREX_ROOT.mad`,
`src/LO_SYN.mad`, `src/LO_GEN.mad`) и дампы `build/*.words` остаются
неизменными: базовая заморозка F0 зафиксирована в
`docs/plan-f77-full/logs/f77_30_f0_etalon_freeze.txt`.
