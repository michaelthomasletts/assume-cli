elhaz
=====

**Version:** |release|

**License:** `Mozilla Public License 2.0 <https://github.com/michaelthomasletts/elhaz/blob/main/LICENSE>`_

**Author:** `Mike Letts <https://michaelthomasletts.com>`_

**Maintainers:** `61418 <https://61418.io>`_

What is elhaz?
--------------

elhaz is a CLI tool for managing and reusing temporary AWS credentials locally.

It creates one AWS session per :ref:`config <config>`, keeps it alive, refreshes temporary AWS credentials automatically, and makes those credentials available across shells, scripts, SDKs, and tools.

Instead of repeatedly assuming roles or re-running credential processes, elhaz maintains a single refreshable session per role and reuses it across your workflow.

It provides a simple interface:

- ``elhaz exec`` to run one-off commands with credentials
- ``elhaz shell`` for an interactive environment
- ``elhaz export`` for environment variables or integration with other tools
- ``elhaz whoami`` to inspect the active identity

Under the hood, elhaz runs a local daemon that caches sessions, refreshes credentials before expiration, and serves them instantly to any local consumer.

The result is a consistent, low-friction way to work with multiple assumed AWS roles.


Why this exists
---------------

Working with AWS credentials locally is often fragmented and repetitive.

- Each tool manages credentials differently
- Temporary credentials are fetched multiple times across processes
- Sessions expire unpredictably
- Switching between roles requires constant reconfiguration

AWS provides primitives for credential management, but it does not coordinate them across your local environment.

elhaz fills that gap.

It introduces a single local authority for credentials:

- One session per configuration
- Automatic refresh before expiration
- Shared across shells, scripts, and tools
- No repeated STS calls for the same role

This allows you to work with multiple IAM roles without thinking about credential lifecycles.


Design
------

elhaz consists of three components:

- **Config** — Named YAML configurations stored in ``~/.elhaz/configs/``
- **Daemon** — A local process that manages and refreshes sessions
- **CLI** — A command-line interface for interacting with configurations and credentials

The CLI communicates with the daemon over a UNIX domain socket using a simple request/response protocol.

Most users do not need to think about these components directly — they exist to make credential management reliable and transparent.

.. toctree::
   :maxdepth: 1
   :caption: Sitemap
   :name: sitemap
   :hidden:

   CLI <cli/index>
   Concepts <concepts/index>
   Installation <installation>
   Quickstart <quickstart>