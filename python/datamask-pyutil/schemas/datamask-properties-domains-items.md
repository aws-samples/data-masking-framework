# Untitled object in DatamaskConfProcess Schema

```txt
undefined#/properties/Domains/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [datamask.schema.json\*](out/datamask.schema.json "open original schema") |

## items Type

`object` ([Details](datamask-properties-domains-items.md))

# items Properties

| Property                          | Type     | Required | Nullable       | Defined by                                                                                                                                            |
| :-------------------------------- | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [DomainName](#domainname)         | `string` | Required | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-domainname.md "undefined#/properties/Domains/items/properties/DomainName")         |
| [SaltName](#saltname)             | `string` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-saltname.md "undefined#/properties/Domains/items/properties/SaltName")             |
| [Layout](#layout)                 | `string` | Required | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-layout.md "undefined#/properties/Domains/items/properties/Layout")                 |
| [MaskType](#masktype)             | `string` | Required | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-masktype.md "undefined#/properties/Domains/items/properties/MaskType")             |
| [EncryptKey](#encryptkey)         | `string` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-encryptkey.md "undefined#/properties/Domains/items/properties/EncryptKey")         |
| [FieldAlias](#fieldalias)         | `string` | Required | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-fieldalias.md "undefined#/properties/Domains/items/properties/FieldAlias")         |
| [MaskFieldAlias](#maskfieldalias) | `string` | Required | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-maskfieldalias.md "undefined#/properties/Domains/items/properties/MaskFieldAlias") |
| [ReverseDataset](#reversedataset) | `object` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset.md "undefined#/properties/Domains/items/properties/ReverseDataset") |

## DomainName

Domain name

`DomainName`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-domainname.md "undefined#/properties/Domains/items/properties/DomainName")

### DomainName Type

`string`

## SaltName

The sal name to be searched inside the sal file

`SaltName`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-saltname.md "undefined#/properties/Domains/items/properties/SaltName")

### SaltName Type

`string`

## Layout

Layout to be used to replace the salt and field. $SALT will be replaced by the sal value and $VALUE will be replaced by the field value

`Layout`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-layout.md "undefined#/properties/Domains/items/properties/Layout")

### Layout Type

`string`

## MaskType

Algorithm type to mask the field

`MaskType`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-masktype.md "undefined#/properties/Domains/items/properties/MaskType")

### MaskType Type

`string`

## EncryptKey

Encryption key for Algorithm, only when you use aes\_ctr and fte

`EncryptKey`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-encryptkey.md "undefined#/properties/Domains/items/properties/EncryptKey")

### EncryptKey Type

`string`

## FieldAlias

Field alias to be used in the Reverse dataset

`FieldAlias`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-fieldalias.md "undefined#/properties/Domains/items/properties/FieldAlias")

### FieldAlias Type

`string`

## MaskFieldAlias

Mask field alias to be used in the reverse dataset

`MaskFieldAlias`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-maskfieldalias.md "undefined#/properties/Domains/items/properties/MaskFieldAlias")

### MaskFieldAlias Type

`string`

## ReverseDataset



`ReverseDataset`

*   is optional

*   Type: `object` ([Details](datamask-properties-domains-items-properties-reversedataset.md))

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset.md "undefined#/properties/Domains/items/properties/ReverseDataset")

### ReverseDataset Type

`object` ([Details](datamask-properties-domains-items-properties-reversedataset.md))
