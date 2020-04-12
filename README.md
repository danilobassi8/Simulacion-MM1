  ![](/images/UtnLogo.png)
# Sobre el repositorio! 

En este repositorio se encuentra un algoritmo de simulación simple, el cual corresponde a un sistema M/M/1 según la notacion de Kendall.

Esto fue un trabajo practico para la cátedra de **simulación** en la **Universidad Tecnológica Nacional de Rosario**

# Integrantes del grupo:
|       Miembro         |Legajo                 |Dirección de Correo           					|
|-----------------------|-----------------------|-----------------------------------------------|
|Bassi, Danilo           |43725					|danilo-bassi@hotmail.com                       |
|Campitelli, Gabriel     |43677					|campitelligabriel@hotmail.com                  |
|Moreyra, Sebastián      |43684					|sebastian.j.moreyra@hotmail.com                |



# Esquema a resolver

Como se mencionó anteriormente, se debe resolver un sistema M/M/1 con las siguientes caracteristicas:

```mermaid
graph LR
A[Arribos <br> λ=1 cli/ut]--> B((Servidor <br> μ = 1/8 cli/ut))
B --> D[salida]
style A fill:#24ACF2
style D fill:#24ACF2
style B fill:#F0F0F0
```
