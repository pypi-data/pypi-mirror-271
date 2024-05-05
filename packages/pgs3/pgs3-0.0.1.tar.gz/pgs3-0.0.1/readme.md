# pgs3

A command line app that help you backup/restore postgresql to a s3 compatible file storage system.

S3 will be upload to s3://$S3_BUCKET/$S3_PATH/$DATETIME/[schema_dump|db_dump].sql
* DATETIME should be like 20240101_121212, and we use this as version name.

Usage:
    pgs3 -p [path-to-profile-config.json] help
    pgs3 -p [path-to-profile-config.json] init
    pgs3 -p [path-to-profile-config.json] backup
    pgs3 -p [path-to-profile-config.json] backup [--schema-olny/-s]
    pgs3 -p [path-to-profile-config.json] list-backup
    pgs3 -p [path-to-profile-config.json] restore [--version VERSION]
    pgs3 -p [path-to-profile-config.json] download [--version VERSION]
