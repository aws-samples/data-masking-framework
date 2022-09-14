# DatamaskConfProcess Schema

```txt
undefined
```

JSON schema to the datamask-pyutil parameter file

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                              |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [datamask.schema.json](out/datamask.schema.json "open original schema") |

## DatamaskConfProcess Type

`object` ([DatamaskConfProcess](datamask.md))

# DatamaskConfProcess Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                            |
| :------------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------ |
| [Jobs](#jobs)       | `array`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs.md "undefined#/properties/Jobs")       |
| [Domains](#domains) | `array`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-domains.md "undefined#/properties/Domains") |
| [Salts](#salts)     | `object` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-salts.md "undefined#/properties/Salts")     |

## Jobs

List of Jobs

`Jobs`

*   is required

*   Type: `object[]` ([Details](datamask-properties-jobs-items.md))

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs.md "undefined#/properties/Jobs")

### Jobs Type

`object[]` ([Details](datamask-properties-jobs-items.md))

## Domains

List of data mask domains

`Domains`

*   is required

*   Type: `object[]` ([Details](datamask-properties-domains-items.md))

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains.md "undefined#/properties/Domains")

### Domains Type

`object[]` ([Details](datamask-properties-domains-items.md))

## Salts

Salt properties

`Salts`

*   is optional

*   Type: `object` ([Details](datamask-properties-salts.md))

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-salts.md "undefined#/properties/Salts")

### Salts Type

`object` ([Details](datamask-properties-salts.md))
