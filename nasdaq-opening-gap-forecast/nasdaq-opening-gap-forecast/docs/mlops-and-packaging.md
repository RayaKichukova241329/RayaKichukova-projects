# MLOps and packaging

The team turned the notebook work into a modular, tested and documented Python project. I verified this part of the work. The packaged project lives in the team's university repository and is not part of this repository.

## Layout

```
final_project1/
  src/
    app/app.py                  Streamlit dashboard
    config/config.py            settings
    preprocessing/
      data_loader.py            reads the index files
      data_cleaning.py          missing dates and values
      feature_engineering.py    percentage moves, shocks, weighted features
      pipeline.py               runs the steps end to end
      main.py, utils.py
    models/
      ml_models.py              the model types
      model_selection.py        model selection
      evaluation.py             ROC-AUC and classification metrics
      metrics.py, model.py
  tests/                        one test module per main component
  pyproject.toml, poetry.lock   environment and dependencies (Poetry)
  docs/                         documentation
```

## Practices

- **Environment:** Poetry for dependencies and packaging, with a built wheel and source archive.
- **Code quality:** logging, formatting with black and linting with flake8, and refactoring of the original notebook code into modules.
- **Testing:** unit tests for gap labelling, missing data and the shape of predictions, with a coverage report.
- **Documentation:** project and code documentation in the repository.
- **Collaboration:** every member committed to the shared repository.
- **Application:** the dashboard calls the backend modules with the trained model and the label encoder.

## Test coverage

Overall **82%** (230 statements, 42 not covered), from the coverage report of 19 June 2025.

| Module | Statements | Not covered | Coverage |
|---|---|---|---|
| `models/evaluation.py` | 27 | 0 | 100% |
| `models/ml_models.py` | 61 | 0 | 100% |
| `models/model_selection.py` | 13 | 0 | 100% |
| `models/model.py` | 7 | 0 | 100% |
| `models/metrics.py` | 3 | 3 | 0% |
| `preprocessing/feature_engineering.py` | 14 | 0 | 100% |
| `preprocessing/pipeline.py` | 46 | 2 | 96% |
| `preprocessing/data_loader.py` | 14 | 1 | 93% |
| `preprocessing/data_cleaning.py` | 10 | 1 | 90% |
| `preprocessing/main.py` | 24 | 24 | 0% |
| `preprocessing/utils.py` | 11 | 11 | 0% |

The three modules with no coverage are an entry point, a utility file and a small metrics file. The core pipeline and models are well covered.

Back to the [project README](../README.md).
