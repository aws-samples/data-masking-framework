# Untitled object in DatamaskConfProcess Schema

```txt
undefined#/properties/Domains/items/properties/ReverseDataset
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [datamask.schema.json\*](out/datamask.schema.json "open original schema") |

## ReverseDataset Type

`object` ([Details](datamask-properties-domains-items-properties-reversedataset.md))

# ReverseDataset Properties

| Property                                                      | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                            |
| :------------------------------------------------------------ | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Active](#active)                                             | `boolean` | Required | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-active.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/Active")                                             |
| [DatasetPath](#datasetpath)                                   | `string`  | Required | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-datasetpath.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/DatasetPath")                                   |
| [BackupDatasetPath](#backupdatasetpath)                       | `string`  | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-backupdatasetpath.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/BackupDatasetPath")                       |
| [BackupDatasetPartitionLabels](#backupdatasetpartitionlabels) | `object`  | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-backupdatasetpartitionlabels.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/BackupDatasetPartitionLabels") |
| [BackupCoalesce](#backupcoalesce)                             | `number`  | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-backupcoalesce.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/BackupCoalesce")                             |
| [Coalesce](#coalesce)                                         | `number`  | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-coalesce.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/Coalesce")                                         |
| [KeepOnlyBackup](#keeponlybackup)                             | `boolean` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-keeponlybackup.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/KeepOnlyBackup")                             |
| [JobNamePartition](#jobnamepartition)                         | `boolean` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-jobnamepartition.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/JobNamePartition")                         |
| [JobNamePartitionFieldName](#jobnamepartitionfieldname)       | `string`  | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-jobnamepartitionfieldname.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/JobNamePartitionFieldName")       |
| [HashBucketing](#hashbucketing)                               | `boolean` | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-hashbucketing.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/HashBucketing")                               |
| [ReverseTable](#reversetable)                                 | `string`  | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-reversetable.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/ReverseTable")                                 |
| [ReverseDatabase](#reversedatabase)                           | `string`  | Optional | cannot be null | [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-reversedatabase.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/ReverseDatabase")                           |

## Active

If false tur off the creation of the reverse dataset

`Active`

*   is required

*   Type: `boolean`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-active.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/Active")

### Active Type

`boolean`

## DatasetPath

Reverse dataset path

`DatasetPath`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-datasetpath.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/DatasetPath")

### DatasetPath Type

`string`

## BackupDatasetPath

Reverse backup dataset path

`BackupDatasetPath`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-backupdatasetpath.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/BackupDatasetPath")

### BackupDatasetPath Type

`string`

## BackupDatasetPartitionLabels

Backup Dataset Partition Labels

`BackupDatasetPartitionLabels`

*   is optional

*   Type: `object` ([Details](datamask-properties-domains-items-properties-reversedataset-properties-backupdatasetpartitionlabels.md))

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-backupdatasetpartitionlabels.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/BackupDatasetPartitionLabels")

### BackupDatasetPartitionLabels Type

`object` ([Details](datamask-properties-domains-items-properties-reversedataset-properties-backupdatasetpartitionlabels.md))

## BackupCoalesce

If set the process will coalesce partitions before write in the reverse dataset. This is usually the number of files to be write in the ouput path

`BackupCoalesce`

*   is optional

*   Type: `number`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-backupcoalesce.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/BackupCoalesce")

### BackupCoalesce Type

`number`

## Coalesce

If set the process will coalesce partitions before write in the reverse dataset. This is usually the number of files to be write in the ouput path

`Coalesce`

*   is optional

*   Type: `number`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-coalesce.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/Coalesce")

### Coalesce Type

`number`

## KeepOnlyBackup

If True only the backup table will be avaiable, Dafault false

`KeepOnlyBackup`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-keeponlybackup.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/KeepOnlyBackup")

### KeepOnlyBackup Type

`boolean`

## JobNamePartition

If set it will enable TableName Partition, Default false

`JobNamePartition`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-jobnamepartition.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/JobNamePartition")

### JobNamePartition Type

`boolean`

## JobNamePartitionFieldName

Change the default field Name, Default 'JobName'

`JobNamePartitionFieldName`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-jobnamepartitionfieldname.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/JobNamePartitionFieldName")

### JobNamePartitionFieldName Type

`string`

## HashBucketing

If set the process will create bucketing in partitions

`HashBucketing`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-hashbucketing.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/HashBucketing")

### HashBucketing Type

`boolean`

## ReverseTable

If set the process will try to update the table metadata

`ReverseTable`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-reversetable.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/ReverseTable")

### ReverseTable Type

`string`

## ReverseDatabase

If set the process will try to update the metadata, it needs to be set with  ReverseTable

`ReverseDatabase`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [DatamaskConfProcess](datamask-properties-domains-items-properties-reversedataset-properties-reversedatabase.md "undefined#/properties/Domains/items/properties/ReverseDataset/properties/ReverseDatabase")

### ReverseDatabase Type

`string`
