```python
from lib.inphis.models.cult_bienes import CultBienesModel  
from lib.inphis.models.cult_bienes_picklist import CultBienesPicklistModel  
  
  
class CultBienesFactory:  
    @staticmethod  
    def create_bien(tl_nombre: str, cult_var_municipios_cd_values: list[str]):  
        cult_bien = CultBienesModel.create(tl_nombre, cult_var_municipios_cd_values)  
        cult_bien.save()  
  
        for municipio in cult_var_municipios_cd_values:  
            CultBienesPicklistModel.create(cult_bien.cd_codigo, 'MUNICIPIO', municipio).save()  
  
        return cult_bien
```
