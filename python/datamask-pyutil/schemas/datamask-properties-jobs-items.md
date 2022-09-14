# Untitled object in DatamaskConfProcess Schema

```txt
undefined#/properties/Jobs/items
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [datamask.schema.json\*](out/datamask.schema.json "open original schema") |

## items Type

`object` ([Details](datamask-properties-jobs-items.md))

# items Properties

| Property                  | Type      | Required | Nullable       | Defined by                                                                                                                              |
| :------------------------ | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| [JobName](#jobname)       | `string`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-jobname.md "undefined#/properties/Jobs/items/properties/JobName")       |
| [Active](#active)         | `boolean` | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-active.md "undefined#/properties/Jobs/items/properties/Active")         |
| [Input](#input)           | `object`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-input.md "undefined#/properties/Jobs/items/properties/Input")           |
| [Output](#output)         | `object`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-output.md "undefined#/properties/Jobs/items/properties/Output")         |
| [MaskFields](#maskfields) | `array`   | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields.md "undefined#/properties/Jobs/items/properties/MaskFields") |

## JobName

The Job name

`JobName`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-jobname.md "undefined#/properties/Jobs/items/properties/JobName")

### JobName Type

`string`

## Active

If false turn off the job processing

`Active`

*   is required

*   Type: `boolean`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-active.md "undefined#/properties/Jobs/items/properties/Active")

### Active Type

`boolean`

## Input

Input properties

`Input`

*   is required

*   Type: `object` ([Details](datamask-properties-jobs-items-properties-input.md))

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-input.md "undefined#/properties/Jobs/items/properties/Input")

### Input Type

`object` ([Details](datamask-properties-jobs-items-properties-input.md))

## Output

Output properties

`Output`

*   is required

*   Type: `object` ([Details](datamask-properties-jobs-items-properties-output.md))

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-output.md "undefined#/properties/Jobs/items/properties/Output")

### Output Type

`object` ([Details](datamask-properties-jobs-items-properties-output.md))

## MaskFields

List of Mask Field properties

`MaskFields`

*   is required

*   Type: `object[]` ([Details](datamask-properties-jobs-items-properties-maskfields-items.md))

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-maskfields.md "undefined#/properties/Jobs/items/properties/MaskFields")

### MaskFields Type

`object[]` ([Details](datamask-properties-jobs-items-properties-maskfields-items.md))
