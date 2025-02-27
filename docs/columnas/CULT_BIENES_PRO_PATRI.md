| Columna      | Descripción                                          |
|--------------|------------------------------------------------------|
| OBJECTID     | Identificador único                                  |
| CD_CODIGO    | Identificador único de [CULT_BIENES](CULT_BIENES.md) |
| CD_FIGURA    | CD_VALUE de CULT_VAR_PROT_FIGURA                     |
| CD_CATEGORIA | CD_VALUE de CULT_VAR_PROT_BICS                       |
| TL_NUMREG    | Valor de numero de regulación                        |
| CD_TIPOLOGIA | CD_VALUE de CULT_VAR_PROT_BICS                       |

CD_CATEGORIA y CD_TIPOLOGIA usan la misma tabla (CULT_VAR_PROT_BICS) para almacenar las opciones pero parecen que se separan en el
programa (i, j, m, p, q, n, r son exclusivo de de CD_TIPOLOGIA, el resto de CD_CATEGORIA)