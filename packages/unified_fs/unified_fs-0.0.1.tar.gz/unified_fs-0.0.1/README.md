# unified_fs

A unified file system interface for Python. This package provides a unified interface for interacting with the file system, regardless of the underlying file system. This allows you to write code that works with both local and remote file systems without modification.


## Installation

```bash
pip install unified-fs
```

## Usage

```python
from file_system import FileSystem

fs = FileSystem()

# List files in a directory
files = fs.listdir('s3://my-bucket/my-folder')
print(files)

# Read a file
data = fs.read('s3://my-bucket/my-folder/my-file.txt')
print(data)

# Write a file
fs.write('s3://my-bucket/my-folder/my-file.txt', 'Hello, world!')

# Delete a file
fs.delete('s3://my-bucket/my-folder/my-file.txt')
```

## Supported File Systems

- Local file system
- Amazon S3
- Google Cloud Storage
- Azure Blob Storage
- FTP
- SFTP

```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](

## Authors

- **Balakrishna Maduru** - *Initial work* - [balakrishnamaduru@gmail.com]

```

## Run tests

```bash
poetry run pytest
```



