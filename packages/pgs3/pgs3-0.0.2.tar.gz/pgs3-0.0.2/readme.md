# pgs3

```
Usage: pgs3 [OPTIONS] COMMAND [ARGS]...

  A command line app that help you backup/restore postgresql to a s3
  compatible file storage system.

  S3 will be upload to
  s3://$S3_BUCKET/$S3_PATH/$DATETIME/[schema_dump|db_dump].sql * DATETIME
  should be like 20240101_121212, and we use this as version name.

Options:
  --help  Show this message and exit.

Commands:
  backup
  download
  init
  list-backup```