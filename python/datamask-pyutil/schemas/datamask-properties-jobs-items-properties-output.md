# Untitled object in DatamaskConfProcess Schema

```txt
undefined#/properties/Jobs/items/properties/Output
```

Output properties

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [datamask.schema.json\*](out/datamask.schema.json "open original schema") |

## Output Type

`object` ([Details](datamask-properties-jobs-items-properties-output.md))

# Output Properties

| Property                          | Type     | Required | Nullable       | Defined by                                                                                                                                                                          |
| :-------------------------------- | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [OutputPath](#outputpath)         | `string` | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-output-properties-outputpath.md "undefined#/properties/Jobs/items/properties/Output/properties/OutputPath")         |
| [OutputTable](#outputtable)       | `string` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-output-properties-outputtable.md "undefined#/properties/Jobs/items/properties/Output/properties/OutputTable")       |
| [OutputDatabase](#outputdatabase) | `string` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-output-properties-outputdatabase.md "undefined#/properties/Jobs/items/properties/Output/properties/OutputDatabase") |
| [Coalesce](#coalesce)             | `number` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-output-properties-coalesce.md "undefined#/properties/Jobs/items/properties/Output/properties/Coalesce")             |

## OutputPath

The output path to write

`OutputPath`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-output-properties-outputpath.md "undefined#/properties/Jobs/items/properties/Output/properties/OutputPath")

### OutputPath Type

`string`

## OutputTable

If set the process will try to update the table metadata

`OutputTable`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-output-properties-outputtable.md "undefined#/properties/Jobs/items/properties/Output/properties/OutputTable")

### OutputTable Type

`string`

## OutputDatabase

If set the process will try to update the metadata, it needs to be set with  OutputTable

`OutputDatabase`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-output-properties-outputdatabase.md "undefined#/properties/Jobs/items/properties/Output/properties/OutputDatabase")

### OutputDatabase Type

`string`

## Coalesce

If set the process will coalesce partitions before write in the output. This is usually the number of files to be write in the ouput path.

`Coalesce`

*   is optional

*   Type: `number`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-output-properties-coalesce.md "undefined#/properties/Jobs/items/properties/Output/properties/Coalesce")

### Coalesce Type

`number`
