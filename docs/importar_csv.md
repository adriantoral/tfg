# Manual para importar desde un CSV

## Pasos para importar desde un CSV

Primero es importante conocer la estructura del CSV.

Un CSV corresponde únicamente a 1 sola tabla, no se pueden mezclar datos dos tablas diferentes en un mismo CSV.
El formato de un CSV es el siguiente:

```
columna1,columna2,columna3
dato1,dato2,dato3
dato4,dato5,dato6
```

Donde la primera fila corresponde a los nombres de las columnas y las siguientes filas a los datos.
Los nombres de las columnas se pueden ver en la documentación que se adjunte en un correo pasado, pero aquí te dejo un
ejemplo de la tabla de bienes que es la más importante.

Los datos dentro de IGNORE no se deberian de poner en el CSV, ya se gestionan internamente por access.

```python
IGNORE = [
	'objectid',
	'shape',
	'shape_length',
	'shape_area'
]


@dataclass
class CultBienesModel( IModels ):
	objectid: int = None
	shape: bytearray = None
	cd_codigo: str = None
	tl_nombre: str = None
	tl_dircalle: str = None
	nm_dirnum: int = None
	tl_localidad: str = None
	tl_otros_nombres: str = None
	cd_cod_ant: str = None
	nm_utm_x: float = None
	nm_utm_y: float = None
	tl_geo_lon: str = None
	tl_geo_lat: str = None
	nm_altitud: int = None
	nm_extension: int = None
	cl_accesos: str = None
	cl_des_general: str = None
	nm_cronologia_inicio: int = None
	nm_cronologia_fin: int = None
	cl_just_atribucion: str = None
	cl_des_bien: str = None
	cl_des_muebles: str = None
	cl_fuentes_escritas: str = None
	cl_fuentes_carto: str = None
	cl_fuentes_icono: str = None
	cl_fuentes_orales: str = None
	cl_uso_estado: str = None
	tl_estado_porc_extraido: str = None
	tl_figura2: str = None
	tl_figura3: str = None
	tl_figura4: str = None
	tl_figura5: str = None
	cl_observaciones: str = None
	tl_autor: str = None
	tl_supervisor: str = None
	fc_autor_fecha_cumplimenta: datetime.datetime = None
	fc_super_fecha_cumplimenta: datetime.datetime = None
	geometry1_sk: str = None
	tl_adjunto: str = None
	id_referencia: int = None
	tl_fecha_referencia: str = None
	cd_yac_referencia: str = None
	cd_catalogo_regional: str = None
	cd_catalogo_urbanistico: str = None
	fc_inscripcion_catalogo: datetime.datetime = None
	tl_proteccion_arq_regional: str = None
	tl_dir_postal: str = None
	tl_dir_poligono: str = None
	tl_referencia_catastral: str = None
	cl_historia_bien: str = None
	cl_obras_usos: str = None
	tl_arca: str = None
	cl_otros_codigos: str = None
	fc_fecha_modificacion: datetime.datetime = None
	shape_length: float = None
	shape_area: float = None
	geometry_bk: str = None
	geometry_x_bk: float = None
	geometry_y_bk: float = None
	geometry_area_bk: float = None
```

Por cierto, al importar el CSV, el programa intentara convertir el dato de entrada al tipo correspondiente en su clase,
por ejemplo, si el tipo de la columna es un int, el programa intentara convertir el dato a un int, si no puede, lanzara
un error.

Un ejemplo de un CSV final sería el siguiente:

```csv
cd_codigo;tl_nombre;tl_dircalle;nm_dirnum
004-001;Casa de la Cultura;Av. 9 de Octubre;505
001-002-003-004;Calle 1;Av. 9 de Octubre;508
```

La cosa más importante de la tabla de bienes es como se genera su cd_codigo, este codigo corresponde a un id unico de un
bien, y se genera basado en los CD_VALUES de la tabla CULT_VAR_MUNICIPIOS. SIEMPRE debera haber al menos un cd_codigo.

Por lo que se deberán separar los CD_VALUES por un guion como se ve en el ejemplo, el programa se encargara de generar
el codigo correcto. Si solo hay un CD_VALUE no hace falta poner el guion.


