# Группы ресурсов (Resource Group)

## Описание

При большом числе разнообразных сущностей в системе требуется механизм их группировки. В НОКе таковой называется **Ресурсная группа** (`Resource Group`). Под ресурсом, в данном случае, подразумевается некая сущность системы, с поддержкой назначения групп - на текущий момент это реализовано:

| Сущность       | Модель             | Название    |
| ---            | ---                | ---         |
| `ManagedObject`| `sa.ManagedObject` | Устройство  |
| `Address`      | `ip.Address`       | IP адрес    | 
| `Prefix`       | `ip.Prefix`        | IP Prefix   |
| `Phone Number` |  `phone.PhoneNumber`    | Телефонный номер |
| `Interface`    | `inv.Interface`    | Интерфейс   |
| `Service`      | `sa.Service`       | Сервис      |


По способу присвоения выделяют:

* **Динамические** (`Dynamic`) - присвоенени происходит на основе описанных в группе правил
* **Статические** (`Static`) - назначение происходит в интерфейсе системы, либо через внешний механизм `ETL`

Объединение Статическиx (`Static`) и Динамических (`Dynamic`) даёт **Действующие** (`Effective`) группы. Именно по ним происходит проверка групп в системе.

```
Обновление `Действующих групп` происходит при сохранении.
```

Группы поддерживают иерархию - т.е. при указании родительское группы в неё попадают все вложенные.


Помимо задач группировки `Ресурсные группы` позволяют описывать отношения (связи) между различными сущностями системы через модель `Поставщик-Потребитель`. В качестве примера можно привести следующие задачи:

* Указать, что некое устройство является терминатором `IPoE` сессий для группы устройств
* Указать, что устройство является шлюзом для `IP` подсетей
* Телефонный номер обслуживается на определённой АТС

Тип связи задаётся используемоей [Технологией](../technology/index.md) (`Technology`). В ней описываются:

* Какой ресурс **предоставляет** участники группы (`Client model`)
* Какой ресурс **потребляется**  (`Service model`) участниками группы
* Условие при котором ресурсу может быть назначена **только одна группы этой технологии**

Первый два пункта, условно, можно описать как:
> Набор `service_model` делает `name` для набора `client_model`
> 

Последний пункти позволяет использовать группы для обозначения различных *плавающих* ресурсов и кластеров. Когда клиент в отдельный момент времени может быть зарегистрирован только на одном из узлов кластера (или может быть активен только один IP адрес). При его выставлении, если у ресурса появляется несколько групп одной технологии, то в **Действующие** попадёт только последняя.

Если потребляемый ресурс (`Client model`) не задан, мы получаем простую группировку сущностей, указанных в `Service Model`.


## Работа с Группами

### Управление группами

Справочник Групп расположены в меню `Учёт объектов` (`Inventory`) -> Ресурсные группы (`Resource Group`). Для создания группы достаточно указать её имя (`Name`) и Технологию (`Technology`) по которой она будет работать. Доступны следующие настройки:

* Имя (`Name`) - название группы
* Родительская группа (`Parent Group`) - родительская группа
* Технология (`Technology`) - технология
* Описание (`Description`) - текстовое описание
* Метки (`Labels`) - назначенные метки
* Динамические Сервисные метки (`Dynamic Service Labels`) - список меток для автоматической привязки указанных ресурсов. На метки в пределах одной группы (строки) действует правило **И** а между группами - **ИЛИ**
* Динамические Клиентские метки (`Dynamic Client Labels`) - список меток для динамической привязки указанных ресурсов. На метки в пределах одной группы (строки) действует правило **И** а между группами - **ИЛИ**
* Блок интеграции с внешними система
    * Внешняя система (`Remote System`) - внешняя система, из которой получена метка
    * Идентификатор во внешней системе (`Remote ID`) - идентификатор метки во внешней системе

### Динамические группы

Динамической назначение групп осуществляется на основе заданных условий. Условий два:
1) Совпадение типа ресурса с указанной в [технологии](../technology/index.md)
2) Совпадение с одним из заданных в настройках группы наборов [меток](../label/index.md)

На группы меток действует правило **ИЛИ** - т.е. для назначения группы достаточно чтобы метки хотя бы одной группы **целиком** присутствовали в `действующих метках` типа ресурса, указанного в `Технологии`. Соответственно,  при совпадении `Dynamic Service Labels` группа добавляется в Сервисные (`Service Group`) а `Dynamic Clients Labels` в клиентские (`Client Groups`).

```
При изменении набора динамических меток добавление групп происходит через задержку, это необходимо учитывать при проверке правильности добавления
```


### Присвоение групп

На форме каждого из поддерживаемых типов ресурсво присутствует панель групп. Выглядит она следующим образом:

На ней отображается список статических и `Действующих` групп.
