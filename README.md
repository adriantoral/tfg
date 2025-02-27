Los bienes en la base de datos de INPHIS se guardan en la tabla [CULT_BIENES](columnas/CULT_BIENES.md).
Esta tabla es la que guarda todos los datos de los bienes, sin embargo, para que el programa INPHIS pueda indexar estos bienes,
hay que crear una referencia en la tabla [CULT_BIENES_PICKLIST](columnas/CULT_BIENES_PICKLIST.md) con un CD_TIPO de valor 'MUNICIPIO',
de esta forma nos aseguramos de que el programa pueda indexar nuestros bienes.

> Los CD_CODIGO de la tabla [CULT_BIENES](columnas/CULT_BIENES.md) no son únicos, pueden estar repetidos, en ese caso la aplicación de
> INPHIS usará la última referencia para hacer cambio, sin embargo, nosotros podemos tratarlos independientemente.

Para crear en nuestro programa un bien, podemos llamar a la factoría de [CULT_BIENES_FACTORY](lib/inphis/factory/CULT_BIENES.md).
Esta se encarga de crear las referencias en las tablas, tanto en [CULT_BIENES](columnas/CULT_BIENES.md) como
en [CULT_BIENES_PICKLIST](columnas/CULT_BIENES_PICKLIST.md).
La factoría devuelve un objeto como si fuese un ODM, entonces para editar los valores de nuestro objeto simplemente deberemos editar sus
atributos y llamar al método .save(), aquí te dejo un ejemplo:

```python
mi_bien = CultBienesFactory.create_bien('MI_BIEN', ["001"])
mi_bien.tl_dircalle = 'Calle Nueva'
mi_bien.save()

# Este es el estado del bien antes de editar sus atributos
# ---------------------------------------------------------
# CultBienesModel(objectid=3, shape=None, cd_codigo='CM/001/0002', tl_nombre='MI_BIEN', tl_dircalle=None, nm_dirnum=None, tl_localidad=None, tl_otros_nombres=None, cd_cod_ant=None, nm_utm_x=None, nm_utm_y=None, tl_geo_lon=None, tl_geo_lat=None, nm_altitud=None, nm_extension=None, cl_accesos=None, cl_des_general=None, nm_cronologia_inicio=None, nm_cronologia_fin=None, cl_just_atribucion=None, cl_des_bien=None, cl_des_muebles=None, cl_fuentes_escritas=None, cl_fuentes_carto=None, cl_fuentes_icono=None, cl_fuentes_orales=None, cl_uso_estado=None, tl_estado_porc_extraido=None, tl_figura2=None, tl_figura3=None, tl_figura4=None, tl_figura5=None, cl_observaciones=None, tl_autor=None, tl_supervisor=None, fc_autor_fecha_cumplimenta=None, fc_super_fecha_cumplimenta=None, geometry1_sk=None, tl_adjunto=None, id_referencia=None, tl_fecha_referencia=None, cd_yac_referencia=None, cd_catalogo_regional=None, cd_catalogo_urbanistico=None, fc_inscripcion_catalogo=None, tl_proteccion_arq_regional=None, tl_dir_postal=None, tl_dir_poligono=None, tl_referencia_catastral=None, cl_historia_bien=None, cl_obras_usos=None, tl_arca=None, cl_otros_codigos=None, fc_fecha_modificacion=None, shape_length=None, shape_area=None, geometry_bk=None, geometry_x_bk=None, geometry_y_bk=None, geometry_area_bk=None)
# ---------------------------------------------------------
# CultBienesModel(objectid=3, shape=None, cd_codigo='CM/001/0002', tl_nombre='MI_BIEN', tl_dircalle='Calle Nueva', nm_dirnum=None, tl_localidad=None, tl_otros_nombres=None, cd_cod_ant=None, nm_utm_x=None, nm_utm_y=None, tl_geo_lon=None, tl_geo_lat=None, nm_altitud=None, nm_extension=None, cl_accesos=None, cl_des_general=None, nm_cronologia_inicio=None, nm_cronologia_fin=None, cl_just_atribucion=None, cl_des_bien=None, cl_des_muebles=None, cl_fuentes_escritas=None, cl_fuentes_carto=None, cl_fuentes_icono=None, cl_fuentes_orales=None, cl_uso_estado=None, tl_estado_porc_extraido=None, tl_figura2=None, tl_figura3=None, tl_figura4=None, tl_figura5=None, cl_observaciones=None, tl_autor=None, tl_supervisor=None, fc_autor_fecha_cumplimenta=None, fc_super_fecha_cumplimenta=None, geometry1_sk=None, tl_adjunto=None, id_referencia=None, tl_fecha_referencia=None, cd_yac_referencia=None, cd_catalogo_regional=None, cd_catalogo_urbanistico=None, fc_inscripcion_catalogo=None, tl_proteccion_arq_regional=None, tl_dir_postal=None, tl_dir_poligono=None, tl_referencia_catastral=None, cl_historia_bien=None, cl_obras_usos=None, tl_arca=None, cl_otros_codigos=None, fc_fecha_modificacion=None, shape_length=None, shape_area=None, geometry_bk=None, geometry_x_bk=None, geometry_y_bk=None, geometry_area_bk=None)
```

Al crear un nuevo bien, así quedaría nuestra base de datos:

```json
{
  // Todos los valores estan a None porque asi los hemos declarado
  "CULT_BIENES": [
    "(2, None, 'CM/001/0001', 'MI_BIEN', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)"
  ],
  "CULT_BIENES_PICKLIST": [
    "(9, 'CM/001/0001', 'MUNICIPIO', 1, '001')"
  ]
}
```

En cuanto a importar muchos bienes de una vez, usaremos el formato de fichero CSV, donde se tendrán que cumplir las siguientes reglas:

- El primer valor tienen que ser los CD_VALUES de los municipios separados por un guion, si es solo un valor, no se incluirá guion.
- A partir del segundo valor ya serán los datos de nuestra tabla [CULT_BIENES](columnas/CULT_BIENES.md) empezando a partir de CD_CODIGO, si
  se quiere evitar un valor se deberá poner 'None' en su valor. Es importante que estén presentes los 57 campos de la tabla. Las columnas de
  la tabla [CULT_BIENES](columnas/CULT_BIENES.md) cuya descripción sea 'None', se deberá dejar en 'None' porque todavía no le he encontrado
  utilidad en la base de datos de INPHIS.

Un ejemplo de CSV:

```csv
001-002-003;cd_codigo;tl_nombre;tl_dircalle;nm_dirnum;tl_localidad;tl_otros_nombres;cd_cod_ant;nm_utm_x;nm_utm_y;tl_geo_lon;tl_geo_lat;nm_altitud;nm_extension;cl_accesos;cl_des_general;nm_cronologia_inicio;nm_cronologia_fin;cl_just_atribucion;cl_des_bien;cl_des_muebles;cl_fuentes_escritas;cl_fuentes_carto;cl_fuentes_icono;cl_fuentes_orales;cl_uso_estado;tl_estado_porc_extraido;tl_figura2;tl_figura3;tl_figura4;tl_figura5;cl_observaciones;tl_autor;tl_supervisor;fc_autor_fecha_cumplimenta;fc_super_fecha_cumplimenta;geometry1_sk;tl_adjunto;id_referencia;tl_fecha_referencia;cd_yac_referencia;cd_catalogo_regional;cd_catalogo_urbanistico;fc_inscripcion_catalogo;tl_proteccion_arq_regional;tl_dir_postal;tl_dir_poligono;tl_referencia_catastral;cl_historia_bien;cl_obras_usos;tl_arca;cl_otros_codigos;fc_fecha_modificacion;shape_length;shape_area;geometry_bk;geometry_x_bk;geometry_y_bk;geometry_area_bk
004;cd_codigo;tl_nombre;tl_dircalle;nm_dirnum;tl_localidad;tl_otros_nombres;cd_cod_ant;nm_utm_x;nm_utm_y;tl_geo_lon;tl_geo_lat;nm_altitud;nm_extension;cl_accesos;cl_des_general;nm_cronologia_inicio;nm_cronologia_fin;cl_just_atribucion;cl_des_bien;cl_des_muebles;cl_fuentes_escritas;cl_fuentes_carto;cl_fuentes_icono;cl_fuentes_orales;cl_uso_estado;tl_estado_porc_extraido;tl_figura2;tl_figura3;tl_figura4;tl_figura5;cl_observaciones;tl_autor;tl_supervisor;fc_autor_fecha_cumplimenta;fc_super_fecha_cumplimenta;geometry1_sk;tl_adjunto;id_referencia;tl_fecha_referencia;cd_yac_referencia;cd_catalogo_regional;cd_catalogo_urbanistico;fc_inscripcion_catalogo;tl_proteccion_arq_regional;tl_dir_postal;tl_dir_poligono;tl_referencia_catastral;cl_historia_bien;cl_obras_usos;tl_arca;cl_otros_codigos;fc_fecha_modificacion;shape_length;shape_area;geometry_bk;geometry_x_bk;geometry_y_bk;geometry_area_bk
```
