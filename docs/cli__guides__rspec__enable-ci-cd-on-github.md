# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/rspec/enable-ci-cd-on-github.html
> **Fetched**: 2026-06-06T03:10:00.351070

---

[Connector SDK](</en/developing-connectors/sdk>)

[CLI](</en/developing-connectors/sdk/cli>)

Guides

# Enabling CI/CD on GitHub [​](<#enabling-ci-cd-on-github>)

To improve deployment stability, we recommend implementing CI/CD tools into your connector development workflow. This guide will go over the process if you're using Github and Github actions. This same logic, however, can be ported over to other Git tools and CI/CD tools.

## Prerequisites [​](<#prerequisites>)

  * You have a Github repository
  * Permissions in your GitHub repository that allow you to manage Actions
  * Permissions in your Github repository to set repository secrets

## Setting up GitHub Actions [​](<#setting-up-github-actions>)

Next, you'll create a [GitHub Actions](<https://docs.github.com/en/actions>) file. This file is used to define the steps the action will execute.

In your repository's `.github/workflows` folder, create a new `ruby.yml` file. For example:

yaml
```ruby

    name: Connector Unit Test

    on: 
      pull_request:
        branches: [ main ]

    jobs:
      test:

        runs-on: ubuntu-latest
        strategy:
          matrix:
            ruby-version: ['2.4.10', '2.5', '2.7']

        steps:
        - uses: actions/checkout@v2
        - name: Set up Ruby
          uses: ruby/setup-ruby@v1
          with:
            ruby-version: ${{ matrix.ruby-version }}
            bundler-cache: true 
        - name: Run tests
          env: # Only needed if using encrypted files.
            WORKATO_CONNECTOR_MASTER_KEY: ${{ secrets.WORKATO_CONNECTOR_MASTER_KEY }} 
          run: bundle exec rspec

```

In this example, our project is using encrypted settings ([`settings.yaml.enc`](</en/developing-connectors/sdk/cli/reference/cli-project-directory-reference#settings-yaml-enc-settings-yaml>)). When using encryption, make sure to:

  * Add your project's `master.key` file to `.gitignore`, and
  * Set environment variables in your repository using [encrypted secrets](<https://docs.github.com/en/actions/reference/encrypted-secrets>). In this example, our variable is named `WORKATO_CONNECTOR_MASTER_KEY`.

## Adding other automated checks [​](<#adding-other-automated-checks>)

You may choose to add other types of checks such as [Rubocop](<https://docs.github.com/en/actions/guides/building-and-testing-ruby#linting-your-code>) which is a easy way to maintain code style.

## Automate deployment to Workato [​](<#automate-deployment-to-workato>)

Now, you might also want to automate the deployment of your connector to your DEV environment such that whenever a PR is merged, its automatically deployed to your workspace!

In your repository's `.github/workflows` folder, create a new `ruby.yml` file. For example:

yaml
```ruby

    name: Connector Unit Test & Deployment

    on: 
      push:
        branches: [ main ]

    jobs:
      test:

        runs-on: ubuntu-latest
        strategy:
          matrix:
            ruby-version: ['2.4.10', '2.5', '2.7']

        steps:
        - uses: actions/checkout@v2
        - name: Set up Ruby
          uses: ruby/setup-ruby@v1
          with:
            ruby-version: ${{ matrix.ruby-version }}
            bundler-cache: true 
        - name: Run tests
          env: # Only needed if using encrypted files.
            WORKATO_CONNECTOR_MASTER_KEY: ${{ secrets.WORKATO_CONNECTOR_MASTER_KEY }} 
          run: bundle exec rspec
        - name: Push to DEV workspace Use this to push to DEV. This can be enabled when a PR is merged.
          env: # Only needed if using encrypted files.
            WORKATO_API_TOKEN: ${{ secrets.WORKATO_DEV_ENVIRONMENT_API_TOKEN}} 
          run: bundle exec workato push -n "${{ github.event.head_commit.message }}"

```

## What's next? [​](<#what-s-next>)

  * Learn more about the [files in your connector project](</en/developing-connectors/sdk/cli/reference/cli-project-directory-reference>)

**Last updated:**
