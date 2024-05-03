# Arkindex Scrapers

Website scrapers to retrieve HTR datasets and publish them to [Arkindex][1].

## Installation

To install `arkindex-scrapers`, you can do it from [Pypi](https://pypi.org/project/arkindex-scrapers):
* Use a virtualenv (e.g. with virtualenvwrapper `mkvirtualenv -a . scrapers`)
* Install scrapers as a package (e.g. `pip install arkindex-scrapers`)

## Usage

When `arkindex-scrapers` is installed in your environment, the `scrapers` command becomes available. This command has 3 subcommands. Learn more about them using:
```shell
scrapers -h
```

### Do It Yourself History

The `diy` subcommand retrieves images and transcriptions from collections available on [the DIY History website](http://diyhistory.lib.uiowa.edu/).

Provide the ID of a collection as a positional argument and an output directory. This command will generate 1 JSON file per item. Each of these can be uploaded to [Arkindex][1] using the [`publish`](#publish-to-arkindex) subcommand.

### Europeana Transcribathon

The `eu-trans` subcommand retrieves images and transcriptions from stories available on [the Europeana Transcribathon website](https://europeana.transcribathon.eu).

By default, this command will look for stories on the whole website. You can restrict the search to a specific story using the `--story_id` argument. This command will generate 1 JSON file per story. Each of these can be uploaded to [Arkindex][1] using the [`publish`](#publish-to-arkindex) subcommand.

### Publish to Arkindex

The `publish` subcommand publishes local JSON files scraped by other subcommands to an [Arkindex][1] instance.
Any JSON file is supported, provided that they respect the following format:

```json
{
    "name": "", // Name of the element on Arkindex
    "metadata": [ // List of metadata to publish on the element
        {
            "type": "", // Arkindex type of the metadata
            "name": "", // Name of the metadata
            "value": "" // Value of the metadata
        },
        ...
    ],
    "items": [ // Elements published as children
        {
            "name": "", // Name of the element on Arkindex
            "metadata": [], // List of metadata to publish on the element
            "transcriptions": [ // List of transcriptions to publish on the element
                "", // Text of a transcription
                ...
            ],
            "iiif_url": "", // IIIF URL of the image (optional)
            "image_path": "" // Relative path towards the image file (optional)
        },
        ...
    ]
}
```

Learn more about all arguments of this subcommand using:
```shell
scrapers publish -h
```

Learn more about [Arkindex][1]'s metadata, transcription and image system in its [documentation][1].

## Contributing

### Development

For development and tests purpose it may be useful to install the project as a editable package with pip.
* Use a virtualenv (e.g. with virtualenvwrapper `mkvirtualenv -a . scrapers`)
* Install scrapers as a package (e.g. `pip install -e .`)

### Linter

Code syntax is analyzed before submitting the code.\
To run the linter tools suite you may use pre-commit.
```shell
pip install pre-commit
pre-commit run -a
```

### Run tests

Tests are executed with `tox` using [pytest](https://pytest.org).
To install `tox`,
```shell
pip install tox
tox
```

To reload the test virtual environment you can use `tox -r`

Run a single test module: `tox -- <test_path>`
Run a single test: `tox -- <test_path>::<test_function>`

--

[1]: https://doc.arkindex.org
