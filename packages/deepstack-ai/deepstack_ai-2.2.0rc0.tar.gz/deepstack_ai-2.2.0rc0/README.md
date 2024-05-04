<div align="center">
  <a href="https://deepstack.khulnasoft.com/"><img src="https://github.com/khulnasoft/deepstack/blob/main/docs/img/banner_20.png" alt="Green logo of a stylized white 'H' with the text 'Deepstack, by khulnasoft. Deepstack 2.0 is live 🎉' Abstract green and yellow diagrams in the background."></a>

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CI/CD   | [![Tests](https://github.com/khulnasoft/deepstack/actions/workflows/tests.yml/badge.svg)](https://github.com/khulnasoft/deepstack/actions/workflows/tests.yml) [![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![Coverage Status](https://coveralls.io/repos/github/khulnasoft/deepstack/badge.svg?branch=main)](https://coveralls.io/github/khulnasoft/deepstack?branch=main)                                                                                                                                                                                    |
| Docs    | [![Website](https://img.shields.io/website?label=documentation&up_message=online&url=https%3A%2F%2Fdocs.deepstack.khulnasoft.com)](https://docs.deepstack.khulnasoft.com)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Package | [![PyPI](https://img.shields.io/pypi/v/deepstack-ai)](https://pypi.org/project/deepstack-ai/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/deepstack-ai?color=blue&logo=pypi&logoColor=gold) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/deepstack-ai?logo=python&logoColor=gold) [![Conda Version](https://img.shields.io/conda/vn/conda-forge/deepstack-ai.svg)](https://anaconda.org/conda-forge/deepstack-ai) [![GitHub](https://img.shields.io/github/license/khulnasoft/deepstack?color=blue)](LICENSE) [![License Compliance](https://github.com/khulnasoft/deepstack/actions/workflows/license_compliance.yml/badge.svg)](https://github.com/khulnasoft/deepstack/actions/workflows/license_compliance.yml) |
| Meta    | [![Discord](https://img.shields.io/discord/993534733298450452?logo=discord)](https://discord.gg/deepstack) [![Twitter Follow](https://img.shields.io/twitter/follow/deepstack_ai)](https://twitter.com/khulnasoft)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
</div>

[Deepstack](https://deepstack.khulnasoft.com/) is an end-to-end LLM framework that allows you to build applications powered by
LLMs, Transformer models, vector search and more. Whether you want to perform retrieval-augmented generation (RAG),
document search, question answering or answer generation, Deepstack can orchestrate state-of-the-art embedding models
and LLMs into pipelines to build end-to-end NLP applications and solve your use case.

## Installation

The simplest way to get Deepstack is via pip:

```sh
pip install deepstack-ai
```

Deepstack supports multiple installation methods including Docker images. For a comprehensive guide please refer
to the [documentation](https://docs.deepstack.khulnasoft.com/v2.0/docs/installation).

## Documentation

If you're new to the project, check out ["What is Deepstack?"](https://deepstack.khulnasoft.com/overview/intro) then go
through the ["Get Started Guide"](https://deepstack.khulnasoft.com/overview/quick-start) and build your first LLM application
in a matter of minutes. Keep learning with the [tutorials](https://deepstack.khulnasoft.com/tutorials?v=2.0). For more advanced
use cases, or just to get some inspiration, you can browse our Deepstack recipes in the
[Cookbook](https://github.com/khulnasoft/deepstack-cookbook).

At any given point, hit the [documentation](https://docs.deepstack.khulnasoft.com/v2.0/docs/intro) to learn more about Deepstack, what can it do for you and the technology behind.

## Features

> [!IMPORTANT]
> **You are currently looking at the readme of Deepstack 2.0**. We are still maintaining Deepstack 1.x to give everyone
> enough time to migrate to 2.0. [Switch to Deepstack 1.x here](https://github.com/khulnasoft/deepstack/tree/v1.x).

- **Technology agnostic:** Allow users the flexibility to decide what vendor or technology they want and make it easy to switch out any component for another. Deepstack allows you to use and compare models available from OpenAI, Cohere and Hugging Face, as well as your own local models or models hosted on Azure, Bedrock and SageMaker.
- **Explicit:** Make it transparent how different moving parts can “talk” to each other so it's easier to fit your tech stack and use case.
- **Flexible:** Deepstack provides all tooling in one place: database access, file conversion, cleaning, splitting, training, eval, inference, and more. And whenever custom behavior is desirable, it's easy to create custom components.
- **Extensible:** Provide a uniform and easy way for the community and third parties to build their own components and foster an open ecosystem around Deepstack.

Some examples of what you can do with Deepstack:

-   Build **retrieval augmented generation (RAG)** by making use of one of the available vector databases and customizing your LLM interaction, the sky is the limit 🚀
-   Perform Question Answering **in natural language** to find granular answers in your documents.
-   Perform **semantic search** and retrieve documents according to meaning.
-   Build applications that can make complex decisions making to answer complex queries: such as systems that can resolve complex customer queries, do knowledge search on many disconnected resources and so on.
-   Scale to millions of docs using retrievers and production-scale components.
-   Use **off-the-shelf models** or **fine-tune** them to your data.
-   Use **user feedback** to evaluate, benchmark, and continuously improve your models.

> [!TIP]
><img src="https://github.com/khulnasoft/deepstack/raw/main/docs/img/khulnasoft-cloud-logo-lightblue.png"  width=30% height=30%>
>
> Are you looking for a managed solution that benefits from Deepstack? [khulnasoft Cloud](https://www.khulnasoft.com/khulnasoft-cloud?utm_campaign=developer-relations&utm_source=deepstack&utm_medium=readme) is our fully managed, end-to-end platform to integrate LLMs with your data, which uses Deepstack for the LLM pipelines architecture.

## Telemetry

Deepstack collects **anonymous** usage statistics of pipeline components. We receive an event every time these components are initialized. This way, we know which components are most relevant to our community.

Read more about telemetry in Deepstack or how you can opt out in [Deepstack docs](https://docs.deepstack.khulnasoft.com/v2.0/docs/telemetry).

## 🖖 Community

If you have a feature request or a bug report, feel free to open an [issue in Github](https://github.com/khulnasoft/deepstack/issues). We regularly check these and you can expect a quick response. If you'd like to discuss a topic, or get more general advice on how to make Deepstack work for your project, you can start a thread in [Github Discussions](https://github.com/khulnasoft/deepstack/discussions) or our [Discord channel](https://discord.gg/deepstack). We also check [𝕏 (Twitter)](https://twitter.com/khulnasoft) and [Stack Overflow](https://stackoverflow.com/questions/tagged/deepstack).

## Contributing to Deepstack

We are very open to the community's contributions - be it a quick fix of a typo, or a completely new feature! You don't need to be a Deepstack expert to provide meaningful improvements. To learn how to get started, check out our [Contributor Guidelines](https://github.com/khulnasoft/deepstack/blob/main/CONTRIBUTING.md) first.

There are several ways you can contribute to Deepstack:
- Contribute to the main Deepstack project
- Contribute an integration on [deepstack-core-integrations](https://github.com/khulnasoft/deepstack-core-integrations)

> [!TIP]
>👉 **[Check out the full list of issues that are open to contributions](https://github.com/orgs/khulnasoft/projects/14)**

## Who Uses Deepstack

Here's a list of projects and companies using Deepstack. Want to add yours? Open a PR, add it to the list and let the
world know that you use Deepstack!

-   [Airbus](https://www.airbus.com/en)
-   [Alcatel-Lucent](https://www.al-enterprise.com/)
-   [Apple](https://www.apple.com/)
-   [BetterUp](https://www.betterup.com/)
-   [Databricks](https://www.databricks.com/)
-   [Khulnasoft](https://khulnasoft.com/)
-   [Etalab](https://www.khulnasoft.com/blog/improving-on-site-search-for-government-agencies-etalab)
-   [Infineon](https://www.infineon.com/)
-   [Intel](https://github.com/intel/open-domain-question-and-answer#readme)
-   [Intelijus](https://www.intelijus.ai/)
-   [Intel Labs](https://github.com/IntelLabs/fastRAG#readme)
-   [LEGO](https://github.com/larsbaunwall/bricky#readme)
-   [Netflix](https://netflix.com)
-   [Nvidia](https://developer.nvidia.com/blog/reducing-development-time-for-intelligent-virtual-assistants-in-contact-centers/)
-   [PostHog](https://github.com/PostHog/max-ai#readme)
-   [Rakuten](https://www.rakuten.com/)
-   [Sooth.ai](https://www.khulnasoft.com/blog/advanced-neural-search-with-sooth-ai)
