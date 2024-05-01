# LogKontrol

LogKontrol is a Python library designed to provide flexible and configurable logging capabilities across different modules of a Python application. It supports file and console logging, with easy customization through a YAML configuration file.

## Features

- **File logging:** with automatic file creation
- **Configurable:** logging levels and message formats
- **Versatile:** Support for logging plain messages, variable states, function calls, and JSON content
- **Debugging:** Optional console output for immediate debugging

## Installation

To install LogKontrol, run the following command:

```bash
pip install logkontrol
```

You can also clone this repository and install it directly from the source:

```bash
git clone https://github.com/voidfemme/logkontrol.git
cd logkontrol
pip install .
```

## Usage

Here's a quick example to get you started with LogKontrol:

```python
from logkontrol.file_logger import init_logging, log_message

# Initialize the logging system
init_logging()

# Log a simple message
log_message('general', 'Hello, world!')
```

## Configuration

LogKontrol is highly customizable through a simple YAML configuration file. Here's the default configuration:

```yaml
log_file_paths:
  general: 'logs/general.log'
  errors: 'logs/errors.log'
  debug: 'logs/debug.log'
log_format: '[{timestamp}] [{level}] {message}'
timestamp_format: '%Y-%m-%d %H:%M:%S'
log_level: 'INFO'
console_output: True
```

Or, specify a different configuration file during initialization:

```python
init_logging(config_file_path='path/to/your/config.yaml')
```

To add your own logging categories, simply add a new entry under 'log_file_paths' in the
YAML file. For example, to add an audit trail log, you might add:

```yaml
audit: 'logs/audit.log'
```

This allows you to tailor the logging system to suit the needs of your application with
minimal effort.

### Contributing

Contributions are welcome! Please fork the repository and open a pull request with your
improvements.

### License

LogKontrol by voidfemme is marked with CC0 1.0 Universal 💖
[LICENSE](LICENSE) file for details.

## Philosophy

LogKontrol is released into the public domain as a reflection of my belief in the principle
of "From each according to their ability, to each according to their needs." I believe that
software should be a collective effort, where individuals contribute their skills and knowledge
for the benefit of the community as a whole.

By dedicating this library to the public domain, I aim to ensure that it remains freely
available to anyone who needs it, without barriers or restrictions. I encourage users to
utilize, modify, and distribute LogKontrol according to their needs, and I welcome
contributions from those who have the ability to improve and enhance the library.

My goal is to foster a spirit of collaboration, mutual aid, and shared ownership in the
software development community. I believe that by working together and pooling our
resources, we can create tools and technologies that serve the common good and promote a more
equitable and inclusive society.
