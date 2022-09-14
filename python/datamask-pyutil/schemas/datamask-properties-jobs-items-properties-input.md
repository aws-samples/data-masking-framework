# Untitled object in DatamaskConfProcess Schema

```txt
undefined#/properties/Jobs/items/properties/Input
```

Input properties

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [datamask.schema.json\*](out/datamask.schema.json "open original schema") |

## Input Type

`object` ([Details](datamask-properties-jobs-items-properties-input.md))

# Input Properties

| Property                                                      | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                    |
| :------------------------------------------------------------ | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [InputPath](#inputpath)                                       | `string`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-inputpath.md "undefined#/properties/Jobs/items/properties/Input/properties/InputPath")                                       |
| [Delete](#delete)                                             | `boolean` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-delete.md "undefined#/properties/Jobs/items/properties/Input/properties/Delete")                                             |
| [RepartitionValue](#repartitionvalue)                         | `number`  | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-repartitionvalue.md "undefined#/properties/Jobs/items/properties/Input/properties/RepartitionValue")                         |
| [ReadFormat](#readformat)                                     | `string`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-readformat.md "undefined#/properties/Jobs/items/properties/Input/properties/ReadFormat")                                     |
| [PartitionColumnTypeInference](#partitioncolumntypeinference) | `boolean` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-partitioncolumntypeinference.md "undefined#/properties/Jobs/items/properties/Input/properties/PartitionColumnTypeInference") |
| [IntPartitions](#intpartitions)                               | `array`   | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-intpartitions.md "undefined#/properties/Jobs/items/properties/Input/properties/IntPartitions")                               |
| [ReadOptions](#readoptions)                                   | `array`   | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-readoptions.md "undefined#/properties/Jobs/items/properties/Input/properties/ReadOptions")                                   |

## InputPath

The input path to be read

`InputPath`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-inputpath.md "undefined#/properties/Jobs/items/properties/Input/properties/InputPath")

### InputPath Type

`string`

## Delete

The input path to be read

`Delete`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-delete.md "undefined#/properties/Jobs/items/properties/Input/properties/Delete")

### Delete Type

`boolean`

## RepartitionValue

If set the process will try to repartition the input to better performance

`RepartitionValue`

*   is optional

*   Type: `number`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-repartitionvalue.md "undefined#/properties/Jobs/items/properties/Input/properties/RepartitionValue")

### RepartitionValue Type

`number`

## ReadFormat

The read format, Examples: parquet, csv

`ReadFormat`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-readformat.md "undefined#/properties/Jobs/items/properties/Input/properties/ReadFormat")

### ReadFormat Type

`string`

## PartitionColumnTypeInference

Disable or Enable partition name inference type on input. Default: True

`PartitionColumnTypeInference`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-partitioncolumntypeinference.md "undefined#/properties/Jobs/items/properties/Input/properties/PartitionColumnTypeInference")

### PartitionColumnTypeInference Type

`boolean`

## IntPartitions

If input has partitions keys, this is the list of int partitions

`IntPartitions`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-intpartitions.md "undefined#/properties/Jobs/items/properties/Input/properties/IntPartitions")

### IntPartitions Type

`string[]`

## ReadOptions



`ReadOptions`

*   is optional

*   Type: `object[]` ([Details](datamask-properties-jobs-items-properties-input-properties-readoptions-items.md))

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-jobs-items-properties-input-properties-readoptions.md "undefined#/properties/Jobs/items/properties/Input/properties/ReadOptions")

### ReadOptions Type

`object[]` ([Details](datamask-properties-jobs-items-properties-input-properties-readoptions-items.md))
