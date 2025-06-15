### Rada

AutomotiveRada is a smart part-matching app that helps businesses manage and cross-reference OE part numbers across automotive, motorcycle, heavy equipment, and industrial systems. It streamlines compatibility checks, supersessions, and aftermarket mapping for precise inventory and service operations.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app rada
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/rada
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
