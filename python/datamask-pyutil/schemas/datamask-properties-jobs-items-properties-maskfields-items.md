# Untitled object in DatamaskConfProcess Schema

```txt
undefined#/properties/Jobs/items/properties/MaskFields/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [datamask.schema.json\*](out/datamask.schema.json "open original schema") |

## items Type

`object` ([Details](datamask-properties-jobs-items-properties-maskfields-items.md))

# items Properties

| Property                        | Type      | Required | Nullable       | Defined by                                                                                                                                                                                            |
| :------------------------------ | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Active](#active)               | `boolean` | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-active.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/Active")               |
| [MaskFieldName](#maskfieldname) | `string`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-maskfieldname.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/MaskFieldName") |
| [FieldName](#fieldname)         | `string`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-fieldname.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/FieldName")         |
| [FormatRE](#formatre)           | `string`  | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-formatre.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/FormatRE")           |
| [DomainName](#domainname)       | `string`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-domainname.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/DomainName")       |
| [KeepMaskName](#keepmaskname)   | `boolean` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-keepmaskname.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/KeepMaskName")   |

## Active

If false turn off the mask field

`Active`

*   is required

*   Type: `boolean`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-active.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/Active")

### Active Type

`boolean`

## MaskFieldName

Mask field name

`MaskFieldName`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-maskfieldname.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/MaskFieldName")

### MaskFieldName Type

`string`

## FieldName

Filed Name

`FieldName`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-fieldname.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/FieldName")

### FieldName Type

`string`

## FormatRE

Regular expression RE to be procced. Use this expression to use just a field part

`FormatRE`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-formatre.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/FormatRE")

### FormatRE Type

`string`

## DomainName

Domain name to get mask configurations

`DomainName`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-domainname.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/DomainName")

### DomainName Type

`string`

## KeepMaskName

If True process will keep the mask name, otherwise the mask field will renamed to the original field name

`KeepMaskName`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields-items-properties-keepmaskname.md "undefined#/properties/Jobs/items/properties/MaskFields/items/properties/KeepMaskName")

### KeepMaskName Type

`boolean`
