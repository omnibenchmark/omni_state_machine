# iris orchestrator

https://gitlab.renkulab.io/omnibenchmark/iris_example/iris-orchestrator/-/blob/master/.gitlab-ci.yml

* This captures all the methods (closed world)
* Does the orchestrator need to be a renku module? why?


# Pipeline stages

## build

this builds a base image I assume (but why?)

```
image_build:
  stage: build
  image: docker:stable
  rules:
    - if: '$CI_PIPELINE_SOURCE == "pipeline"'
      when: never
  before_script:
    - docker login -u gitlab-ci-token -p $CI_JOB_TOKEN http://$CI_REGISTRY
  script: |
      CI_COMMIT_SHA_7=$(echo $CI_COMMIT_SHA | cut -c1-7)
      docker build --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA_7 .
      docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA_7
```

what's the rationale of this build?


# Doubts re. metrics

Afaik, this is not automatic right?

Does this mean the benchmark maintainers need to write custom metric for each method??
https://gitlab.renkulab.io/omnibenchmark/iris_example/iris-accuracy/-/blob/master/src/run_iris-accuracy.R

In this metric_res, what's the hash?
https://gitlab.renkulab.io/omnibenchmark/iris_example/irirs-summary-metrics/-/blob/master/data/iris-accuracy-pval/iris-accuracy-pval_iris_random_forest_d4afa__metric_res.json

Where is this grid generated?
https://gitlab.renkulab.io/omnibenchmark/iris_example/irirs-summary-metrics/-/blob/master/data/irirs-summary-metrics/irirs-summary-metrics.json

what other parameter logic (other than a combinatorial grid) are expected in more complicated methods?


what is the entrypoint for the summary execution?

https://gitlab.renkulab.io/omnibenchmark/iris_example/irirs-summary-metrics/-/tree/master/src
