# Sistema de Recomendación Híbrido (Colaborativo + Evolutivo + Contenido)

> Extensión del algoritmo **HP-MOEA** con una métrica de novedad ponderada por afinidad temática, para mejorar el tratamiento de ítems *newcomers* (problema de inicio frío) en sistemas de recomendación.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![pymoo](https://img.shields.io/badge/pymoo-0.6.1.3-orange)
![NumPy](https://img.shields.io/badge/NumPy-1.26.4-013243?logo=numpy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2.3-150458?logo=pandas&logoColor=white)
![status](https://img.shields.io/badge/status-TFG%20defendido-success)

Trabajo Final de Grado — Ingeniería en Informática · Facultad Politécnica, UNA · 2025
Autor: **José Luis Junior Gutiérrez Agüero** · Tutor: D.Sc. Ing. Christian von Lücken

---

## Tabla de contenidos

- [Descripción](#descripción)
- [Contribución](#contribución)
- [Cómo funciona](#cómo-funciona)
- [Resultados](#resultados)
- [Stack](#stack)
- [Instalación](#instalación)
- [Uso](#uso)
- [Dataset](#dataset)
- [Cita](#cita)

---

## Descripción

El **HP-MOEA** (*Hybrid Probabilistic Multiobjective Evolutionary Algorithm*, Wei et al.) combina filtrado colaborativo basado en usuarios con algoritmos evolutivos multiobjetivo (NSGA-II + SMS-EMOA), optimizando simultáneamente **ganancia** y **novedad** para mitigar el inicio frío.

El problema: el cálculo de novedad del enfoque original solo cuenta *cuántos* ítems nuevos hay en cada lista, sin importar si esos *newcomers* tienen relación con los gustos del usuario. Esto puede recomendar ítems nuevos irrelevantes.

Este proyecto **reemplaza ese conteo binario por una métrica ponderada por afinidad temática** (perfiles de usuario derivados de los géneros de las películas), logrando que los *newcomers* recomendados sean además coherentes con el perfil del usuario.

## Contribución

**Novedad original** — conteo de *newcomers*, sin relevancia:

```
N = Σ_u N_u
```

**Novedad ponderada (propuesta)** — incorpora la afinidad temática `Rel(u, i)`:

```
Novelty*(u) = (1/|G|) · Σ_{i ∈ L_u ∩ N} Rel(u, i)

Rel(u, i) = Σ_{g ∈ G} P_u(g) · C_i(g)
```

- `P_u(g)` — preferencia del usuario `u` por el género `g` (inferida de su historial).
- `C_i(g)` — pertenencia binaria del ítem `i` al género `g`.
- `G` — géneros disponibles · `N` — *newcomers* · `L_u` — lista de recomendación de `u`.

También se redefine el **individuo de máxima novedad** para priorizar *newcomers* relevantes por perfil, en vez de seleccionarlos de forma indiscriminada.

> La modificación toca solo el **preprocesamiento** (`O(m)`) y el **cálculo de novedad** (`O(1)`). La complejidad total se mantiene en `O(T · N · m² · L)`.

## Cómo funciona

1. **Filtrado colaborativo (User-Based CF)** — predice calificaciones faltantes vía similitud coseno y promedio ponderado sobre los `k` vecinos más similares. Los *newcomers* se excluyen aquí y se tratan en la etapa evolutiva.
2. **MOEA biobjetivo** — optimiza **ganancia esperada** (beneficio del proveedor) y **novedad** (modificada, ponderada por contenido). Ambos objetivos se normalizan a `[0, 1]`.
3. **Esquema evolutivo adaptativo** — arranca con **NSGA-II** (exploración rápida) y conmuta a **SMS-EMOA** (mejora estable del hipervolumen) cuando el HV no mejora durante `μ` generaciones.

**Representación del individuo:** matriz `|U| × L` (una fila = lista de recomendación de un usuario), sin ítems duplicados ni ya calificados.
**Operadores:** cruce uniforme guiado por probabilidad genética `λ(A, B)` según la calidad de los padres, y mutación de un punto (`P_m = 1/L`).

## Resultados

Sobre **MovieLens**, 30 ejecuciones, población = 100:

| Métrica                   | Criterio    | Original          | Modificado                 |
| -------------------------- | ----------- | ----------------- | -------------------------- |
| Hipervolumen (HV)          | mayor mejor | 0.51738 ± 0.0008 | **0.5937 ± 0.0008** |
| Generational Distance (GD) | menor mejor | 0.0010 ± 0.0005  | 0.0012 ± 0.0005           |
| Inverted GD (IGD)          | menor mejor | 0.0047 ± 0.0003  | 0.0047 ± 0.0004           |

**HV mejora ≈ 14.75%** sin deteriorar GD/IGD. Robustez confirmada en poblaciones de 50, 100, 150 y 200 (mejora consistente en todos los casos).

> La implementación base se validó contra el paper original: HV de 0.51738 vs. 0.51739 reportado (diferencia < 0.002%).

## Stack

- **Python 3.12**
- **pymoo** — NSGA-II y SMS-EMOA
- **NumPy** — estructuras de datos internas
- **pandas** — lectura/manipulación del dataset
- **matplotlib** — gráficos (frentes de Pareto, ganancia vs. novedad)

## Instalación

```bash
pip install -r requirements.txt
```

o directamente:

```bash
pip install numpy pandas pymoo matplotlib
```

## Uso

### Ejecución simple

```bash
# Modo original (default)
./run_tfg.sh

# Modo modificado
./run_tfg.sh modified
```

### Ejecución en paralelo

```bash
# ./run_parallel.sh  

# 3 instancias en modo original
./run_parallel.sh original 3

# 5 instancias en modo modified
./run_parallel.sh modified 5
```

> Las instancias se lanzan con un intervalo de 30 segundos entre cada una. Los logs se suprimen; para verlos, ejecutar `run_tfg.sh` directamente.

### Estructura del proyecto

```
proyecto/
├── run_tfg.sh
├── run_parallel.sh
└── src/
    ├── RUN_TFG.py
    └── TFG.ipynb
```

## Dataset

[**MovieLens**](https://grouplens.org/datasets/movielens/) (GroupLens, U. de Minnesota) — calificaciones explícitas usuario–película con metadatos de género. Split 80/20 para ajustar el CF; calificación binaria *like/dislike* (≥ 3 = *like*). Parámetros principales: `L=10`, `N=100`, `T=3000`, `μ=500`, `k=10`.

## Cita

```bibtex
@thesis{gutierrez2025recsys,
  author = {Gutiérrez Agüero, José Luis Junior},
  title  = {Diseño e Implementación de un Sistema de Recomendación híbrido
            basado en técnicas colaborativas, evolutivas y de contenido},
  school = {Facultad Politécnica, Universidad Nacional de Asunción},
  year   = {2025},
  type   = {Trabajo Final de Grado}
}
```
