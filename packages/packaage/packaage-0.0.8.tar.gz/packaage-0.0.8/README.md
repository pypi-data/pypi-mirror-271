# Packaage

Ever get this feeling that you wrote a bunch of stuff ever and ever and ever and ever and ever ...

Don't worry fam', we are here !

The AAlmighty _Advanced Analytics Team_ presents ... **The PackAAge**

A way to awesome stuff that allows you to just import a bunch of usefull function to ship your code
to the next stAAge !

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packaage.

```bash
pip install packaage
```

## Usage

### Meaning of life

The most important part of all of this. It contains all the constants you need in you life.

No less, no more.

### AWS

- `connect_to_rds` : a simple wrapper of psycopg2 to connect to an AWS RDS database by interrogating
    Secrets Manager to retreive the credentials
- `s3_to_memory` : download a file from a bucket s3 directly into memory

### NLP

- `clean_text`: simple function to deal with accentation and special characters

### Setup

- `get_git_branch`: retreive the name of the git branch you are in to be used as file key

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would
like to change.

Please make sure to update tests as appropriate.

## License

[MIT](LICENSE.txt)
