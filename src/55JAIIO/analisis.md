# Análisis de resultados — HP-MOEA vs HP-MOEA Modificado

**Paper:** 55 JAIIO – ASAID/SIA · **Dataset:** MovieLens ml-100k
**Fuentes analizadas:** `src/metrics.ipynb`, `src/55JAIIO/statistical_analysis.ipynb`, `src/plots.ipynb`, `contenido.tex`
**Fecha del análisis:** 2026-06-25

> ⚠️ **Estado de los datos.** La fuente de verdad es el pipeline actual:
> `480 corridas → results/metrics.csv → results/statistical_results.csv`.
> Los números de `contenido.tex` (tabla `tab:hv_poblaciones`, abstract, conclusiones)
> están **desactualizados**: provienen de una validación anterior y son inconsistentes
> con el pipeline vigente. La sección 6 lista exactamente qué corregir.

---

## 1. Resumen ejecutivo

1. **La modificación mejora el hipervolumen de forma robusta y estadísticamente concluyente.** En las 4 poblaciones (N = 50/100/150/200) y en los dos modos de semilla, el modificado supera al original con **separación completa** (Â₁₂ = 0.00) y p ≪ 0.001 incluso tras corrección Holm-Bonferroni. La dirección del resultado central del paper es sólida.

2. **La magnitud de la mejora real es ~3.4 %, no 14.75 %.** Bajo una convención de HV consistente (`ref_point=[0,0]`, la del pipeline), el HV pasa de **0.5733 → 0.5928** en N=100 → **+3.40 %**. El 14.75 % del paper compara el HV modificado contra el valor base `0.51738`, que pertenece a otra convención de HV (réplica del paper original) y no se reproduce en el pipeline actual. Es una comparación de peras con manzanas.

3. **La mejora es consistente, no "más pronunciada en N pequeño".** El incremento relativo es prácticamente plano: 3.34 % (N50), 3.40 % (N100), 3.51 % (N150), 3.52 % (N200). El texto actual del paper afirma "más pronunciada en poblaciones pequeñas (N=100: +14.75 %)", lo cual es un artefacto del baseline equivocado y además contradice a sus vecinos (N50: +4.9 %, N200: +3.6 %).

4. **GD no es "idéntico": el modificado converge un poco peor, aunque la diferencia es minúscula.** GD sube de ~0.0009 (orig) a ~0.0013 (mod) en N=100, diferencia significativa en N=100/150/200. Es estadísticamente detectable (varianza ínfima + 30 corridas) pero **prácticamente despreciable** (~0.0004 en valor absoluto) frente a la ganancia en HV.

5. **IGD sí es estable.** Solo 1 de 8 pruebas resulta significativa tras Holm (N200 Wilcoxon). El frente del modificado conserva cobertura equivalente.

---

## 2. Origen de los datos

| Artefacto | Contenido | Rol |
|---|---|---|
| `results/{variante}/{seed_mode}/N{n}/*.pkl` | 480 corridas (4 variantes × 4 N × 30 rep.) | Datos crudos (frentes `F`) |
| `results/metrics.csv` | HV, GD, IGD por corrida (480 filas) | **Fuente de verdad de métricas** |
| `results/statistical_results.csv` | p-valores, Â₁₂, Holm por métrica/N/prueba | **Fuente de verdad estadística** |
| `contenido.tex` | Tabla y porcentajes del paper | **Desactualizado** — ver §6 |

Las 480 corridas están completas (30 por cada una de las 16 categorías), de modo que toda la Fase 1 del plan está ejecutada pese a que el checklist de `CLAUDE.md` siga marcado como pendiente.

---

## 3. Hipervolumen (HV) — métrica principal

### 3.1 Valores (media ± desv.)

| N | Orig. *same* | Mod. *same* | Orig. *diff* | Mod. *diff* | Mejora |
|---|---|---|---|---|---|
| 50  | 0.5644 ± 0.0040 | 0.5832 ± 0.0033 | 0.5636 ± 0.0042 | 0.5828 ± 0.0023 | **+3.34 %** |
| 100 | 0.5734 ± 0.0007 | 0.5929 ± 0.0008 | 0.5732 ± 0.0008 | 0.5926 ± 0.0010 | **+3.40 %** |
| 150 | 0.5761 ± 0.0006 | 0.5963 ± 0.0005 | 0.5761 ± 0.0005 | 0.5963 ± 0.0005 | **+3.51 %** |
| 200 | 0.5778 ± 0.0004 | 0.5981 ± 0.0008 | 0.5777 ± 0.0004 | 0.5984 ± 0.0004 | **+3.52 %** |

### 3.2 Lectura

- **Brecha absoluta casi constante (~0.0195–0.0205)** en todos los N; el incremento relativo crece levísimamente con N.
- **`same_seed` ≈ `diff_seed`** en medias → la mejora no depende del esquema de semillas; el efecto es del algoritmo, no del azar.
- **La varianza colapsa al crecer N** (σ pasa de ~0.003–0.004 en N50 a ~0.0004 en N200): poblaciones grandes estabilizan el HV.
- El HV crece con N en ambas variantes (más individuos ⇒ mejor cobertura del espacio objetivo), manteniendo el modificado siempre por encima.

---

## 4. Generational Distance (GD) — convergencia

### 4.1 Valores (media ± desv.)

| N | Orig. *same* | Mod. *same* | Orig. *diff* | Mod. *diff* |
|---|---|---|---|---|
| 50  | 0.00184 ± 0.0028 | 0.00227 ± 0.0022 | 0.00218 ± 0.0029 | 0.00212 ± 0.0014 |
| 100 | 0.00091 ± 0.0004 | 0.00129 ± 0.0006 | 0.00090 ± 0.0004 | 0.00130 ± 0.0007 |
| 150 | 0.00089 ± 0.0004 | 0.00115 ± 0.0004 | 0.00080 ± 0.0003 | 0.00116 ± 0.0003 |
| 200 | 0.00071 ± 0.0003 | 0.00121 ± 0.0005 | 0.00076 ± 0.0003 | 0.00104 ± 0.0003 |

### 4.2 Lectura

- El modificado tiene GD **sistemáticamente mayor** (peor convergencia) a partir de N=100: ~0.0013 vs ~0.0009 — un ~40 % relativo, pero **~0.0004 en absoluto**.
- Estadísticamente significativo en N=100/150/200 (ver §6 detalle); **no** significativo en N=50 (alta varianza).
- Interpretación: el frente del modificado se "estira" hacia regiones de mayor novedad ponderada; eso aumenta levemente la distancia promedio al sub-frente de referencia de su propia categoría. Es un costo marginal y esperable, no una degradación real de la búsqueda.

---

## 5. Inverted Generational Distance (IGD) — convergencia + cobertura

### 5.1 Valores (media ± desv.)

| N | Orig. *same* | Mod. *same* | Orig. *diff* | Mod. *diff* |
|---|---|---|---|---|
| 50  | 0.00957 ± 0.0018 | 0.00937 ± 0.0013 | 0.00969 ± 0.0019 | 0.00931 ± 0.0010 |
| 100 | 0.00456 ± 0.0003 | 0.00469 ± 0.0004 | 0.00468 ± 0.0004 | 0.00472 ± 0.0004 |
| 150 | 0.00316 ± 0.0002 | 0.00325 ± 0.0002 | 0.00316 ± 0.0002 | 0.00326 ± 0.0002 |
| 200 | 0.00240 ± 0.0002 | 0.00260 ± 0.0004 | 0.00241 ± 0.0002 | 0.00250 ± 0.0002 |

### 5.2 Lectura

- IGD prácticamente **idéntico** entre variantes; las diferencias caen dentro de la desviación estándar.
- Solo **1 de 8** comparaciones es significativa tras Holm (N=200, Wilcoxon). El resto: no significativo.
- Ambas variantes mejoran su IGD al crecer N (frente más denso y mejor distribuido).
- Es la métrica que **sí** respalda limpiamente la afirmación de "convergencia/cobertura estable".

---

## 6. Significancia estadística (consolidado)

Pruebas: **Wilcoxon pareado** (`same_seed`) y **Mann-Whitney U** (`diff_seed`), corregidas con **Holm-Bonferroni** por métrica. Tamaño de efecto **Vargha-Delaney Â₁₂ = P(valor_orig > valor_mod)**.

### 6.1 HV — concluyente en todos los casos

| N | Prueba | p (Holm) | Â₁₂ | ¿Sig.? |
|---|---|---|---|---|
| 50–200 | Wilcoxon | < 1e-8 | 0.00 | ✓ |
| 50–200 | Mann-Whitney | < 1e-9 | 0.00 | ✓ |

**Â₁₂ = 0.00 ⇒ separación completa:** *toda* corrida modificada supera a *toda* corrida original. Efecto "grande" en el máximo posible. Este es el hallazgo más fuerte del trabajo y es independiente del error de magnitud del §1.2.

### 6.2 GD — favorece levemente al **original** donde es significativo

| N | Prueba | p (Holm) | Â₁₂ | ¿Sig.? |
|---|---|---|---|---|
| 50  | Wilcoxon | 0.0556 | 0.36 | ✗ |
| 50  | Mann-Whitney | 0.5011 | 0.45 | ✗ |
| 100 | Wilcoxon | 0.0348 | 0.28 | ✓ |
| 100 | Mann-Whitney | 0.0108 | 0.27 | ✓ |
| 150 | Wilcoxon | 0.0556 | 0.28 | ✗ |
| 150 | Mann-Whitney | 0.0002 | 0.18 | ✓ |
| 200 | Wilcoxon | < 0.001 | 0.15 | ✓ |
| 200 | Mann-Whitney | 0.0008 | 0.21 | ✓ |

Â₁₂ < 0.5 ⇒ el GD del original tiende a ser menor (mejor). Significativo en 5 de 8 celdas. Efecto de tamaño medio-grande, pero magnitud absoluta despreciable.

### 6.3 IGD — estable (solo 1 significativa tras Holm)

| N | Prueba | p (Holm) | Â₁₂ | ¿Sig.? |
|---|---|---|---|---|
| 50  | Wilcoxon | 1.000 | 0.53 | ✗ |
| 50  | Mann-Whitney | 1.000 | 0.56 | ✗ |
| 100 | Wilcoxon | 0.293 | 0.37 | ✗ |
| 100 | Mann-Whitney | 1.000 | 0.49 | ✗ |
| 150 | Wilcoxon | 0.227 | 0.37 | ✗ |
| 150 | Mann-Whitney | 0.097 | 0.31 | ✗ |
| 200 | Wilcoxon | 0.0127 | 0.27 | ✓ |
| 200 | Mann-Whitney | 0.227 | 0.34 | ✗ |

---

## 7. Discrepancias a corregir en `contenido.tex`

El `.tex` está desactualizado respecto al pipeline. Correcciones concretas:

| Ubicación en `.tex` | Dice (stale) | Debe decir (pipeline actual) |
|---|---|---|
| Abstract (l. 33-35) | "incremento del **14.75 %** en hipervolumen" | **~3.4 %** (consistente en todos los N) |
| Implementación (l. 244-246) | base 0.51738 vs 0.51739 (réplica) | Mantener **solo como validación de la réplica**; no usarla como baseline de la mejora |
| Resultados (l. 274-281) | "0.5937 … +14.75 % respecto al original (0.51738)" | "0.5928 vs **0.5733** (HV original N=100, misma convención) → **+3.40 %**" |
| Tabla `tab:hv_poblaciones` (l. 299-302) | ver abajo | ver abajo |
| Texto post-tabla (l. 309-317) | "más pronunciada en pequeñas (N=100: +14.75 %)" | "consistente (~3.3–3.5 %) en todos los N" |
| Conclusiones (l. 330-336) | "14.75 % (de 0.5174 a 0.5937)" | "~3.4 % (de 0.5733 a 0.5928)" |

### 7.1 Tabla `tab:hv_poblaciones` corregida (medias del pipeline)

| Población | HV Orig. *diff* | HV Mod. *diff* | HV Orig. *same* | HV Mod. *same* |
|---|---|---|---|---|
| 50  | 0.5636 ± 0.0042 | 0.5828 ± 0.0023 | 0.5644 ± 0.0040 | 0.5832 ± 0.0033 |
| 100 | 0.5732 ± 0.0008 | 0.5926 ± 0.0010 | 0.5734 ± 0.0007 | 0.5929 ± 0.0008 |
| 150 | 0.5761 ± 0.0005 | 0.5963 ± 0.0005 | 0.5761 ± 0.0006 | 0.5963 ± 0.0005 |
| 200 | 0.5777 ± 0.0004 | 0.5984 ± 0.0004 | 0.5778 ± 0.0004 | 0.5981 ± 0.0008 |

Errores específicos de la tabla vieja:
- **Orig. N=100 = 0.5174** → es el valor base de la réplica (0.51738) mal insertado; debe ser **~0.5733**. Esta celda es la que alimenta el falso 14.75 %.
- **Fila `same_seed` N=100 estaba vacía ("---")** → ya disponible: 0.5734 / 0.5929.
- **Mod. N=50 = 0.5938** estaba inflado → real **~0.5828–0.5832**.
- Mod. N=150/200 ligeramente desfasados respecto al pipeline.

> El **único** valor de HV del paper que era aproximadamente correcto es el del modificado N=100 (~0.5937 vs 0.5928). El baseline original es el que estaba mal, y por eso el porcentaje se disparó.

---

## 8. Observaciones metodológicas

1. **Mezcla de convenciones de HV.** El `0.51738` (réplica del HP-MOEA original) y el `0.5928` (pipeline, `ref_point=[0,0]`) son magnitudes calculadas bajo convenciones distintas. `0.51738` no aparece en ningún notebook ni script del pipeline (solo en el `.tex`) → no es reproducible desde el flujo actual. Para cualquier afirmación de mejora, comparar **siempre** original vs modificado dentro de `metrics.csv`.

2. **Tamaño del frente de referencia.** El original genera uniones no-dominadas **más grandes** que el modificado (p. ej. N=200 same_seed: 1739 vs 1393 puntos). Sugiere que el modificado produce un frente más "estirado" pero algo menos denso — coherente con el leve aumento de GD. Vale la pena mencionarlo al discutir GD.

3. **Significancia ≠ relevancia práctica en GD.** Con σ ~0.0003 y 30 corridas, diferencias de ~0.0004 se vuelven significativas. Conviene reportar GD con su magnitud absoluta y enmarcarlo como "costo despreciable", no esconderlo como "idéntico".

4. **Verificar `config.json`.** El config actual tiene `user_based_cf.K = 20` y `cf_config.K = 25`, mientras el paper afirma haber seleccionado **k = 10** por MSE. Confirmar cuál corresponde a las corridas finales y unificar el reporte.

---

## 9. Recomendaciones

**Para el paper (prioridad alta):**
- [ ] Sustituir **14.75 % → ~3.4 %** en abstract, resultados y conclusiones.
- [ ] Reemplazar la tabla `tab:hv_poblaciones` por §7.1 (incluye fila N=100 same_seed).
- [ ] Corregir la narrativa: la mejora es **consistente y robusta**, no "más pronunciada en N pequeño".
- [ ] Reformular la afirmación sobre GD/IGD: IGD estable; GD con incremento marginal (~0.0004) estadísticamente detectable pero práctico-despreciable.
- [ ] Apoyarse en el argumento más fuerte: **separación completa en HV (Â₁₂ = 0)** en todos los N y modos de semilla.

**Para el pipeline (prioridad media):**
- [ ] Actualizar el checklist de Fase 1 en `CLAUDE.md` (las 480 corridas ya están).
- [ ] Regenerar la Fase 5 (figura del paper, N=100 mediana) y confirmar que el caption refleje la mejora real (~3.4 %).

**Conclusión de fondo:** el aporte del trabajo **se sostiene** — la ponderación por contenido mejora el HV de forma robusta y estadísticamente concluyente, sin degradar la cobertura (IGD) y con un costo de convergencia (GD) despreciable. Lo único que falla es la **magnitud reportada** (14.75 %), producto de comparar contra un baseline de otra convención. Corregida a ~3.4 %, la historia es más modesta pero mucho más creíble y defendible.
